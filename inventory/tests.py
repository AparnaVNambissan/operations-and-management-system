from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import (
    User, Department, Category, Asset, AssetRequest, 
    Task, SubTask, Skill, Award, MaintenanceIssue, DepartmentIssue
)

class InventorySystemTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create department
        self.dept_it = Department.objects.create(name='IT Engineering', description='Information Technology')
        self.dept_hr = Department.objects.create(name='Human Resources', description='HR and Talent')
        
        # Create skill
        self.skill_python = Skill.objects.create(name='Python')
        
        # Create users
        self.admin_user = User.objects.create_user(
            username='admin_test',
            password='Password123!',
            role='ADMIN',
            email='admin@test.com'
        )
        self.employee_user = User.objects.create_user(
            username='emp_test',
            password='Password123!',
            role='EMPLOYEE',
            department=self.dept_it,
            email='emp@test.com'
        )
        self.employee_user.skills.add(self.skill_python)
        
        # Create category & asset
        self.category = Category.objects.create(name='Hardware', description='Laptops and Desktops')
        self.asset = Asset.objects.create(
            name='ThinkPad X1 Carbon',
            category=self.category,
            department=self.dept_it,
            total_quantity=10,
            available_quantity=10,
            low_stock_threshold=3,
            description='Core i7 16GB'
        )

    def test_login_and_role_redirect(self):
        # Admin login
        response = self.client.post(reverse('login'), {
            'username': 'admin_test',
            'password': 'Password123!'
        })
        self.assertRedirects(response, reverse('dashboard'), target_status_code=302)
        # Dashboard redirect to admin_dashboard
        dash_resp = self.client.get(reverse('dashboard'))
        self.assertRedirects(dash_resp, reverse('admin_dashboard'))

        # Employee login
        self.client.logout()
        response = self.client.post(reverse('login'), {
            'username': 'emp_test',
            'password': 'Password123!'
        })
        self.assertRedirects(response, reverse('dashboard'), target_status_code=302)
        dash_resp = self.client.get(reverse('dashboard'))
        self.assertRedirects(dash_resp, reverse('employee_dashboard'))

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'new_emp',
            'email': 'new_emp@test.com',
            'first_name': 'New',
            'last_name': 'Employee',
            'role': 'EMPLOYEE',
            'department': self.dept_hr.id,
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!'
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='new_emp').exists())

    def test_department_management_crud(self):
        self.client.login(username='admin_test', password='Password123!')
        
        # Department list
        resp = self.client.get(reverse('department_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'IT Engineering')
        
        # Add department
        resp = self.client.post(reverse('add_department'), {
            'name': 'Marketing Team',
            'description': 'Marketing and Sales'
        })
        self.assertRedirects(resp, reverse('department_list'))
        marketing = Department.objects.get(name='Marketing Team')
        
        # Edit department
        resp = self.client.post(reverse('edit_department', args=[marketing.id]), {
            'name': 'Global Marketing',
            'description': 'Updated description'
        })
        self.assertRedirects(resp, reverse('department_list'))
        marketing.refresh_from_db()
        self.assertEqual(marketing.name, 'Global Marketing')
        
        # Department detail
        resp = self.client.get(reverse('department_detail', args=[marketing.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Global Marketing')
        
        # Delete department
        resp = self.client.post(reverse('delete_department', args=[marketing.id]))
        self.assertRedirects(resp, reverse('department_list'))
        self.assertFalse(Department.objects.filter(id=marketing.id).exists())

    def test_asset_management_and_availability(self):
        self.client.login(username='admin_test', password='Password123!')
        
        # Asset list & availability view
        resp = self.client.get(reverse('asset_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'ThinkPad X1 Carbon')
        
        # Add asset
        resp = self.client.post(reverse('add_asset'), {
            'name': 'Dell UltraSharp Monitor',
            'category': self.category.id,
            'department': self.dept_it.id,
            'total_quantity': 5,
            'available_quantity': 5,
            'low_stock_threshold': 2,
            'description': '27-inch 4K'
        })
        self.assertRedirects(resp, reverse('asset_list'))
        self.assertTrue(Asset.objects.filter(name='Dell UltraSharp Monitor').exists())
        
        # Edit asset
        dell = Asset.objects.get(name='Dell UltraSharp Monitor')
        resp = self.client.post(reverse('edit_asset', args=[dell.id]), {
            'name': 'Dell UltraSharp Monitor 4K',
            'category': self.category.id,
            'department': self.dept_it.id,
            'total_quantity': 5,
            'available_quantity': 1, # Trigger low stock
            'low_stock_threshold': 2,
            'description': '27-inch 4K Updated'
        })
        self.assertRedirects(resp, reverse('asset_list'))
        dell.refresh_from_db()
        self.assertTrue(dell.is_low_stock)
        self.assertEqual(dell.stock_status, 'LOW_STOCK')

    def test_asset_request_approval_and_return_cycle(self):
        # Employee requests asset
        self.client.login(username='emp_test', password='Password123!')
        resp = self.client.post(reverse('request_asset', args=[self.asset.id]), {
            'quantity': 2,
            'notes': 'Need laptop for client deployment'
        })
        self.assertEqual(AssetRequest.objects.count(), 1)
        req = AssetRequest.objects.first()
        self.assertEqual(req.status, 'PENDING')
        self.assertEqual(req.quantity, 2)
        
        # Admin approves request
        self.client.logout()
        self.client.login(username='admin_test', password='Password123!')
        resp = self.client.post(reverse('approve_request', args=[req.id]))
        req.refresh_from_db()
        self.assertEqual(req.status, 'APPROVED')
        self.asset.refresh_from_db()
        self.assertEqual(self.asset.available_quantity, 8) # 10 - 2 = 8
        
        # Employee returns asset
        self.client.logout()
        self.client.login(username='emp_test', password='Password123!')
        resp = self.client.post(reverse('return_asset', args=[req.id]))
        req.refresh_from_db()
        self.assertEqual(req.status, 'RETURNED')
        self.asset.refresh_from_db()
        self.assertEqual(self.asset.available_quantity, 10) # Restored back to 10

    def test_asset_request_rejection(self):
        # Employee requests asset
        self.client.login(username='emp_test', password='Password123!')
        self.client.post(reverse('request_asset', args=[self.asset.id]), {
            'quantity': 1,
            'notes': 'Extra spare'
        })
        req = AssetRequest.objects.first()
        
        # Admin rejects
        self.client.logout()
        self.client.login(username='admin_test', password='Password123!')
        resp = self.client.post(reverse('reject_request', args=[req.id]), {
            'admin_notes': 'Stock currently reserved for operations.'
        })
        req.refresh_from_db()
        self.assertEqual(req.status, 'REJECTED')
        self.assertEqual(req.admin_notes, 'Stock currently reserved for operations.')

    def test_complaints_and_issue_management(self):
        self.client.login(username='emp_test', password='Password123!')
        
        # Report maintenance defect
        resp = self.client.post(reverse('report_issue'), {
            'asset_id': self.asset.id,
            'description': 'Keyboard spacebar sticking and trackpad loose',
            'is_damaged': 'on',
            'priority': 'HIGH'
        })
        self.assertEqual(MaintenanceIssue.objects.count(), 1)
        m_issue = MaintenanceIssue.objects.first()
        self.assertEqual(m_issue.priority, 'HIGH')
        self.assertTrue(m_issue.is_damaged)
        
        # Create department ticket
        resp = self.client.post(reverse('create_dept_issue'), {
            'target_department': self.dept_hr.id,
            'title': 'New hire onboarding kit required',
            'description': 'Need access badge and welcome guide for upcoming developer',
            'priority': 'MEDIUM'
        })
        self.assertEqual(DepartmentIssue.objects.count(), 1)
        d_issue = DepartmentIssue.objects.first()
        self.assertEqual(d_issue.title, 'New hire onboarding kit required')
        
        # Update maintenance issue status
        self.client.logout()
        self.client.login(username='admin_test', password='Password123!')
        resp = self.client.post(reverse('update_maintenance_issue', args=[m_issue.id]), {
            'status': 'RESOLVED',
            'priority': 'MEDIUM',
            'resolution_notes': 'Keyboard cleaned and trackpad re-seated.'
        })
        m_issue.refresh_from_db()
        self.assertEqual(m_issue.status, 'RESOLVED')
        self.assertIsNotNone(m_issue.resolved_at)

    def test_task_subtask_and_gamification_awards(self):
        self.client.login(username='admin_test', password='Password123!')
        
        # Create task with auto-assign and subtasks
        future_deadline = timezone.now() + timedelta(days=2)
        resp = self.client.post(reverse('create_task'), {
            'title': 'Deploy Database Migration',
            'description': 'Run production migrations safely',
            'required_skill': self.skill_python.id,
            'workload_hours': 3,
            'priority': 'HIGH',
            'deadline': future_deadline.strftime('%Y-%m-%dT%H:%M'),
            'auto_assign': '1',
            'subtasks': ['Backup database', 'Run migrate script', 'Verify integrity']
        })
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertEqual(task.assigned_to, self.employee_user) # Auto-assigned based on python skill
        self.assertEqual(task.subtasks.count(), 3)
        self.assertEqual(task.progress_percentage, 0)
        
        # Employee toggles subtasks
        self.client.logout()
        self.client.login(username='emp_test', password='Password123!')
        
        subtasks = list(task.subtasks.all())
        # Toggle subtask 1
        self.client.post(reverse('update_subtask_status', args=[subtasks[0].id]), {'is_completed': 'on'})
        task.refresh_from_db()
        self.assertEqual(task.status, 'IN_PROGRESS')
        self.assertEqual(task.progress_percentage, 33)
        
        # Toggle subtask 2 & 3
        self.client.post(reverse('update_subtask_status', args=[subtasks[1].id]), {'is_completed': 'on'})
        self.client.post(reverse('update_subtask_status', args=[subtasks[2].id]), {'is_completed': 'on'})
        
        task.refresh_from_db()
        self.assertEqual(task.status, 'COMPLETED')
        self.assertEqual(task.progress_percentage, 100)
        
        # Award should be auto-created for on-time completion
        self.assertTrue(Award.objects.filter(employee=self.employee_user).exists())

    def test_custom_award_grant(self):
        self.client.login(username='admin_test', password='Password123!')
        resp = self.client.post(reverse('grant_award'), {
            'employee': self.employee_user.id,
            'badge_icon': '⭐',
            'name': 'Excellence in Service',
            'description': 'Consistently high response rates'
        })
        self.assertRedirects(resp, reverse('award_list'))
        self.assertTrue(Award.objects.filter(name='Excellence in Service').exists())
