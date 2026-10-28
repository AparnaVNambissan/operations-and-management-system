from django.urls import path
from . import views

urlpatterns = [
    # Core navigation
    path('', views.dashboard_view, name='dashboard'),
    path('login/', views.custom_login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('employee-dashboard/', views.employee_dashboard, name='employee_dashboard'),

    # Department Management
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.add_department, name='add_department'),
    path('departments/<int:dept_id>/', views.department_detail, name='department_detail'),
    path('departments/<int:dept_id>/edit/', views.edit_department, name='edit_department'),
    path('departments/<int:dept_id>/delete/', views.delete_department, name='delete_department'),

    # Asset Management & Availability
    path('assets/', views.asset_list, name='asset_list'),
    path('admin/asset/add/', views.add_asset, name='add_asset'),
    path('admin/asset/<int:asset_id>/edit/', views.edit_asset, name='edit_asset'),
    path('admin/asset/<int:asset_id>/delete/', views.delete_asset, name='delete_asset'),
    path('admin/categories/', views.category_list, name='category_list'),
    path('admin/category/<int:cat_id>/delete/', views.delete_category, name='delete_category'),
    path('admin/category/add/api/', views.add_category_api, name='add_category_api'),

    # Asset Requests, Approvals & Returns
    path('requests/', views.request_list, name='request_list'),
    path('request-asset/<int:asset_id>/', views.request_asset, name='request_asset'),
    path('admin/request/<int:request_id>/approve/', views.approve_request, name='approve_request'),
    path('admin/request/<int:request_id>/reject/', views.reject_request, name='reject_request'),
    path('request/<int:request_id>/return/', views.return_asset, name='return_asset'),

    # Complaints & Issues
    path('issues/', views.issue_list, name='issue_list'),
    path('report-issue/', views.report_issue, name='report_issue'),
    path('create-dept-issue/', views.create_dept_issue, name='create_dept_issue'),
    path('issues/maintenance/<int:issue_id>/update/', views.update_maintenance_issue, name='update_maintenance_issue'),
    path('issues/department/<int:issue_id>/update/', views.update_dept_issue, name='update_dept_issue'),
    path('issues/<str:issue_type>/<int:issue_id>/delete/', views.delete_issue, name='delete_issue'),

    # Task and Subtask Management
    path('tasks/', views.task_list, name='task_list'),
    path('admin/task/create/', views.create_task, name='create_task'),
    path('admin/task/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('admin/task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('subtask/<int:subtask_id>/update/', views.update_subtask_status, name='update_subtask_status'),

    # Awards and Badges Management
    path('awards/', views.award_list, name='award_list'),
    path('admin/award/grant/', views.grant_award, name='grant_award'),
    path('admin/award/<int:award_id>/delete/', views.delete_award, name='delete_award'),

    # Team & User Management (Admin)
    path('admin/employees/', views.employee_list, name='employee_list'),
    path('admin/employees/<int:user_id>/update/', views.update_user_department, name='update_user_department'),

    # Reports
    path('admin/report/pdf/', views.generate_pdf_report, name='generate_pdf_report'),
    path('admin/report/excel/', views.generate_excel_report, name='generate_excel_report'),
]
