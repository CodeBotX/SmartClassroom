from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = CustomUser

    # Các trường hiển thị trong trang chỉnh sửa
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('full_name', 'email', 'phone_number', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),  # Để hiển thị trường không thể chỉnh sửa
    )
    readonly_fields = ('date_joined', 'last_login')  # Đặt các trường không thể chỉnh sửa vào readonly_fields

    # Các trường hiển thị trong trang thêm người dùng mới
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'full_name', 'email', 'phone_number', 'role', 'password1', 'password2'),
        }),
    )

    # Cấu hình các trường hiển thị trong trang danh sách
    list_display = ('username', 'full_name', 'email', 'role', 'is_active', 'is_staff')
    search_fields = ('username', 'full_name', 'email')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
