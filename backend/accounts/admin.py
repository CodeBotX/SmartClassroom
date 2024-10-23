from django.contrib import admin
from .models import CustomUser, Teacher, Admin, Parent, Student

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'email', 'is_teacher', 'is_student', 'is_parent', 'is_admin', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'user_id')
    list_filter = ('is_teacher', 'is_student', 'is_parent', 'is_admin', 'is_active','is_superuser')
    ordering = ('username',)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'sex', 'day_of_birth', 'active_status')
    search_fields = ('full_name', 'user__username', 'user__email')
    list_filter = ('active_status',)

class AdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'sex', 'day_of_birth', 'active_status')
    search_fields = ('full_name', 'user__username', 'user__email')
    list_filter = ('active_status',)

class ParentAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'address')
    search_fields = ('full_name', 'user__username', 'user__email')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'sex', 'day_of_birth','active_status')
    search_fields = ('full_name', 'user__username', 'user__email')
    list_filter = ('active_status',)

# Register your models here
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Admin, AdminAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(Student, StudentAdmin)
