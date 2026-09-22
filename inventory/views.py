from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Asset, AssetRequest, Category, Task, SubTask, Skill, Award, User
from django.utils import timezone
from django.db.models import Sum, Q
from django import forms

# Temporary Forms
class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'category', 'description', 'total_quantity', 'available_quantity', 'low_stock_threshold']

@login_required
def dashboard_view(request):
    if request.user.is_admin_role:
        return redirect('admin_dashboard')
    return redirect('employee_dashboard')

@login_required
def admin_dashboard(request):
    if not request.user.is_admin_role:
        return redirect('employee_dashboard')
    
    assets = Asset.objects.all()
    low_stock_assets = [a for a in assets if a.is_low_stock]
    pending_requests = AssetRequest.objects.filter(status='PENDING')
    tasks = Task.objects.all().order_by('assigned_to__username', '-created_at')
    unassigned_tasks = Task.objects.filter(assigned_to__isnull=True).order_by('-created_at')
    awards = Award.objects.all().order_by('employee__username', '-awarded_at')
    employees = User.objects.filter(role='EMPLOYEE').prefetch_related('tasks', 'awards').order_by('username')
    
    context = {
        'assets': assets,
        'low_stock_assets': low_stock_assets,
        'pending_requests': pending_requests,
        'tasks': tasks,
        'unassigned_tasks': unassigned_tasks,
        'awards': awards,
        'employees': employees,
    }
    return render(request, 'inventory/admin_dashboard.html', context)

@login_required
def add_asset(request):
    if not request.user.is_admin_role:
        return redirect('employee_dashboard')
        
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asset added successfully.')
            return redirect('admin_dashboard')
    else:
        form = AssetForm()
    
    return render(request, 'inventory/asset_form.html', {'form': form, 'title': 'Add Asset'})

@login_required
def edit_asset(request, asset_id):
    if not request.user.is_admin_role:
        return redirect('employee_dashboard')
        
    asset = get_object_or_404(Asset, id=asset_id)
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asset updated successfully.')
            return redirect('admin_dashboard')
    else:
        form = AssetForm(instance=asset)
    
    return render(request, 'inventory/asset_form.html', {'form': form, 'title': 'Edit Asset'})

@login_required
def approve_request(request, request_id):
    if not request.user.is_admin_role:
        return redirect('employee_dashboard')
        
    asset_req = get_object_or_404(AssetRequest, id=request_id)
    if asset_req.status == 'PENDING':
        if asset_req.asset.available_quantity >= asset_req.quantity:
            asset_req.asset.available_quantity -= asset_req.quantity
            asset_req.asset.save()
            asset_req.status = 'APPROVED'
            asset_req.save()
            messages.success(request, 'Request approved successfully.')
        else:
            messages.error(request, 'Not enough quantity available.')
    return redirect('admin_dashboard')

@login_required
def reject_request(request, request_id):
    if not request.user.is_admin_role:
        return redirect('employee_dashboard')
        
    asset_req = get_object_or_404(AssetRequest, id=request_id)
    if asset_req.status == 'PENDING':
        asset_req.status = 'REJECTED'
        asset_req.save()
        messages.success(request, 'Request rejected.')
    return redirect('admin_dashboard')

@login_required
def employee_dashboard(request):
    assets = Asset.objects.all()
    my_requests = AssetRequest.objects.filter(employee=request.user).order_by('-request_date')
    my_tasks = Task.objects.filter(assigned_to=request.user).order_by('-created_at')
    my_awards = Award.objects.filter(employee=request.user).order_by('-awarded_at')
    
    return render(request, 'inventory/employee_dashboard.html', {
        'assets': assets, 
        'my_requests': my_requests,
        'my_tasks': my_tasks,
        'my_awards': my_awards,
    })

@login_required
def request_asset(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            AssetRequest.objects.create(
                employee=request.user,
                asset=asset,
                quantity=quantity
            )
            messages.success(request, 'Asset requested successfully.')
        else:
            messages.error(request, 'Invalid quantity.')
    return redirect('employee_dashboard')

@login_required
def generate_pdf_report(request):
    if not request.user.is_admin_role:
        return redirect('employee_dashboard')
    import io
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from django.http import FileResponse
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, "SecureCorp Inventory Report")
    
    assets = Asset.objects.all()
    y = 700
    for asset in assets:
        p.drawString(100, y, f"{asset.name} - Total: {asset.total_quantity} - Available: {asset.available_quantity}")
        y -= 20
        if y < 50:
            p.showPage()
            y = 750
            
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='inventory_report.pdf')

@login_required
def generate_excel_report(request):
    if not request.user.is_admin_role:
        return redirect('employee_dashboard')
    import openpyxl
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=inventory_report.xlsx'
    
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Inventory'
    
    columns = ['ID', 'Name', 'Category', 'Total Quantity', 'Available Quantity']
    worksheet.append(columns)
    
    for asset in Asset.objects.all():
        worksheet.append([asset.id, asset.name, asset.category.name if asset.category else '', asset.total_quantity, asset.available_quantity])
        
    workbook.save(response)
    return response

# Task Forms
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'required_skill', 'deadline', 'workload_hours']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

@login_required
def create_task(request):
    if not request.user.is_admin_role:
        return redirect('employee_dashboard')

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            
            # Auto-assign logic
            if 'auto_assign' in request.POST and task.required_skill:
                eligible_employees = User.objects.filter(role='EMPLOYEE', skills=task.required_skill)
                if eligible_employees.exists():
                    eligible_employees = eligible_employees.annotate(
                        current_workload=Sum('tasks__workload_hours', filter=Q(tasks__status__in=['PENDING', 'IN_PROGRESS']))
                    )
                    
                    best_employee = None
                    lowest_workload = float('inf')
                    
                    for emp in eligible_employees:
                        wl = emp.current_workload or 0
                        if wl < lowest_workload:
                            lowest_workload = wl
                            best_employee = emp
                            
                    if best_employee:
                        task.assigned_to = best_employee
                        messages.success(request, f'Task auto-assigned to {best_employee.username}.')
                    else:
                        messages.warning(request, 'No eligible employee found for auto-assignment.')
                else:
                    messages.warning(request, 'No employee found with the required skill.')
            
            task.save()
            
            # Create subtasks if provided
            subtask_titles = request.POST.getlist('subtasks')
            for st_title in subtask_titles:
                if st_title.strip():
                    SubTask.objects.create(task=task, title=st_title.strip())
                    
            messages.success(request, 'Task created successfully.')
            return redirect('admin_dashboard')
    else:
        initial = {}
        employee_id = request.GET.get('employee')
        if employee_id:
            initial['assigned_to'] = employee_id
        form = TaskForm(initial=initial)
    
    return render(request, 'inventory/task_form.html', {'form': form, 'title': 'Create Task'})

@login_required
def update_subtask_status(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id)
    task = subtask.task
    
    if request.user != task.assigned_to and not request.user.is_admin_role:
        return redirect('employee_dashboard')
        
    if request.method == 'POST':
        is_completed = request.POST.get('is_completed') == 'on'
        subtask.is_completed = is_completed
        subtask.save()
        
        all_completed = all(st.is_completed for st in task.subtasks.all())
        if all_completed and task.status != 'COMPLETED':
            task.status = 'COMPLETED'
            task.completed_at = timezone.now()
            task.save()
            
            if task.completed_at <= task.deadline:
                Award.objects.create(
                    employee=task.assigned_to,
                    name=f"Timely Completion: {task.title}",
                    description="Completed task before the deadline."
                )
                messages.success(request, f"Congratulations! You earned an award for completing '{task.title}' on time!")
            else:
                messages.success(request, f"Task '{task.title}' marked as completed.")
        elif not all_completed and task.status == 'COMPLETED':
            task.status = 'IN_PROGRESS'
            task.completed_at = None
            task.save()
            
    return redirect('employee_dashboard' if not request.user.is_admin_role else 'admin_dashboard')

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class EmployeeRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', )

def register(request):
    if request.method == 'POST':
        form = EmployeeRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'EMPLOYEE'
            user.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    else:
        form = EmployeeRegisterForm()
    
    return render(request, 'inventory/register.html', {'form': form, 'title': 'Register Employee'})

from django.http import JsonResponse
import json

@login_required
def add_category_api(request):
    if not request.user.is_admin_role:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            description = data.get('description', '')
            if name:
                category = Category.objects.create(name=name, description=description)
                return JsonResponse({'id': category.id, 'name': category.name})
            return JsonResponse({'error': 'Name is required'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

class AwardForm(forms.ModelForm):
    class Meta:
        model = Award
        fields = ['employee', 'name', 'description']
        
    def __init__(self, *args, **kwargs):
        super(AwardForm, self).__init__(*args, **kwargs)
        self.fields['employee'].queryset = User.objects.filter(role='EMPLOYEE')

@login_required
def grant_award(request):
    if not request.user.is_admin_role:
        return redirect('employee_dashboard')

    if request.method == 'POST':
        form = AwardForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Award granted successfully!')
            return redirect('admin_dashboard')
    else:
        form = AwardForm()
        
    return render(request, 'inventory/award_form.html', {'form': form, 'title': 'Grant Custom Award'})
