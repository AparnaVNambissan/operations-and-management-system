from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Skill, Category, Asset, AssetRequest, Department, Task, SubTask, Award, MaintenanceIssue, DepartmentIssue

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Organization', {'fields': ('role', 'department', 'skills')}),
    )
    list_display = ('username', 'email', 'role', 'department', 'is_staff')
    list_filter = ('role', 'department', 'is_staff')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Skill)
admin.site.register(Category)
admin.site.register(Asset)
admin.site.register(AssetRequest)
admin.site.register(Department)
admin.site.register(Task)
admin.site.register(SubTask)
admin.site.register(Award)
admin.site.register(MaintenanceIssue)
admin.site.register(DepartmentIssue)
