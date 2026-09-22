from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Admin routes
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/asset/add/', views.add_asset, name='add_asset'),
    path('admin/category/add/api/', views.add_category_api, name='add_category_api'),
    path('admin/asset/<int:asset_id>/edit/', views.edit_asset, name='edit_asset'),
    path('admin/request/<int:request_id>/approve/', views.approve_request, name='approve_request'),
    path('admin/request/<int:request_id>/reject/', views.reject_request, name='reject_request'),
    path('admin/report/pdf/', views.generate_pdf_report, name='generate_pdf_report'),
    path('admin/report/excel/', views.generate_excel_report, name='generate_excel_report'),
    path('admin/task/create/', views.create_task, name='create_task'),
    path('admin/award/grant/', views.grant_award, name='grant_award'),

    # Employee routes
    path('employee-dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('request-asset/<int:asset_id>/', views.request_asset, name='request_asset'),
    path('subtask/<int:subtask_id>/update/', views.update_subtask_status, name='update_subtask_status'),
]
