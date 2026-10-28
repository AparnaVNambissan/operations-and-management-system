from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('EMPLOYEE', 'Employee'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='EMPLOYEE')
    skills = models.ManyToManyField(Skill, blank=True, related_name='employees')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')

    @property
    def is_admin_role(self):
        return self.role == 'ADMIN' or self.is_superuser or self.is_staff

    @property
    def full_name_or_username(self):
        full = self.get_full_name()
        return full if full else self.username

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Asset(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='assets')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets')
    description = models.TextField(blank=True)
    total_quantity = models.PositiveIntegerField(default=0)
    available_quantity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.name
    
    @property
    def is_low_stock(self):
        return self.available_quantity <= self.low_stock_threshold

    @property
    def stock_status(self):
        if self.available_quantity == 0:
            return 'OUT_OF_STOCK'
        elif self.available_quantity <= self.low_stock_threshold:
            return 'LOW_STOCK'
        return 'IN_STOCK'

    @property
    def availability_percent(self):
        if self.total_quantity > 0:
            return int((self.available_quantity / self.total_quantity) * 100)
        return 0

class AssetRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('RETURNED', 'Returned'),
    )
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='requests')
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True, default='')
    admin_notes = models.TextField(blank=True, default='')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    request_date = models.DateTimeField(auto_now_add=True)
    response_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.username} - {self.asset.name} ({self.status})"

class Task(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    )
    PRIORITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    required_skill = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, blank=True)
    deadline = models.DateTimeField()
    workload_hours = models.PositiveIntegerField(default=1)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        if self.status != 'COMPLETED' and self.deadline:
            return timezone.now() > self.deadline
        return False

    @property
    def progress_percentage(self):
        total = self.subtasks.count()
        if total == 0:
            return 100 if self.status == 'COMPLETED' else 0
        done = self.subtasks.filter(is_completed=True).count()
        return int((done / total) * 100)

class SubTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Award(models.Model):
    BADGE_CHOICES = (
        ('⭐', 'Star Performer (⭐)'),
        ('🏆', 'Champion (🏆)'),
        ('⚡', 'Rapid Resolver (⚡)'),
        ('🎯', 'Task Master (🎯)'),
        ('🛡️', 'Asset Guardian (🛡️)'),
        ('💡', 'Innovator (💡)'),
        ('🏅', 'Excellence Medal (🏅)'),
        ('🔥', 'Hard Worker (🔥)'),
    )
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='awards')
    badge_icon = models.CharField(max_length=50, choices=BADGE_CHOICES, default='⭐')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    awarded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.badge_icon} {self.name} - {self.employee.username}"

class MaintenanceIssue(models.Model):
    STATUS_CHOICES = (
        ('REPORTED', 'Reported'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    )
    PRIORITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    )
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='maintenance_issues')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='maintenance_issues', null=True, blank=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_issues')
    description = models.TextField()
    is_damaged = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REPORTED')
    resolution_notes = models.TextField(blank=True, default='')
    reported_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        dept_name = self.department.name if self.department else 'General'
        return f"Issue on {self.asset.name} in {dept_name} - {self.status}"

class DepartmentIssue(models.Model):
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    )
    PRIORITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    target_department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='received_dept_issues')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_dept_issues')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    resolution_notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} for {self.target_department.name}"
