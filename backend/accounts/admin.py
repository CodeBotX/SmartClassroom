from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, Teacher, Admin as AdminModel, Parent, Student

# Tùy chỉnh hiển thị cho CustomUser
class CustomUserAdmin(BaseUserAdmin):
    # Các trường hiển thị trong danh sách
    list_display = ('user_id', 'full_name', 'email', 'phone_number', 'is_active', 'is_staff', 'is_superuser')
    
    # Các trường có thể tìm kiếm
    search_fields = ('username', 'full_name', 'email', 'phone_number')
    
    # Sắp xếp
    ordering = ('username',)
    # Các trường chỉ đọc
    readonly_fields = ('date_joined', 'last_login')
    
    # Tùy chỉnh form hiển thị khi chỉnh sửa user
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('full_name', 'email', 'phone_number', 'day_of_birth', 'sex', 'nation')}),
        ('Roles', {'fields': ('is_parent', 'is_student', 'is_teacher', 'is_admin')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Trường hiển thị khi thêm user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'full_name','phone_number', 'password1', 'password2'),
        }),
    )

# Đăng ký Teacher model
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user_full_name', 'user_id', 'active_status', 'contract_types', 'expertise_levels', 'subjects')
    search_fields = ('user__full_name', 'user__username', 'active_status')


    def user_full_name(self, obj):
        return obj.user.full_name  # Hiển thị full_name từ CustomUser


# Đăng ký Admin model
class AdminModelAdmin(admin.ModelAdmin):
    list_display = ('user_full_name', 'user_id', 'active_status', 'contract_types', 'expertise_levels', 'description')
    search_fields = ('user__full_name', 'user__username', 'active_status')

    def user_full_name(self, obj):
        return obj.user.full_name  # Hiển thị full_name từ CustomUser


# Đăng ký Parent model
class ParentAdmin(admin.ModelAdmin):
    list_display = ('user_full_name', 'user_id', 'phone_number')
    search_fields = ('user__full_name', 'user__username')
    readonly_fields = ('linked_students',)

    def user_full_name(self, obj):
        return obj.user.full_name  # Hiển thị full_name từ CustomUser
    def phone_number(self, obj):
        return obj.user.phone_number  # Hiển thị phone_number từ CustomUser

    def linked_students(self, obj):
        return ", ".join([student.user.full_name for student in obj.students.all()])  # Hiển thị danh sách học sinh liên kết



# Đăng ký Student model
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_id',  'room', 'active_status')
    search_fields = (
        'user__username',       # Tìm kiếm theo username
        'user__user_id', 
        'user__full_name'
    )
    def parent_full_name(self, obj):
        return obj.parent.user.full_name if obj.parent else 'Chưa có phụ huynh'  # Hiển thị tên phụ huynh liên kết (nếu có)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(AdminModel, AdminModelAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(Student, StudentAdmin)
