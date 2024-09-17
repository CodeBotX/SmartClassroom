from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'user_id', 'role', 'phone_number','email', 'date_of_birth')
    search_fields = ('full_name', 'username', 'user_id', 'phone_number')
    list_filter = ('role',)
    ordering = ('-date_of_birth',)

    # Tùy chỉnh các trường hiển thị trong form tạo/sửa
    fields = ('full_name', 'username', 'user_id', 'role','phone_number','email', 'date_of_birth')
    readonly_fields = ('user_id',)

    # Tùy chỉnh giao diện admin nếu cần
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Nếu là sửa đổi đối tượng hiện có
            return self.readonly_fields + ('user_id',)
        return self.readonly_fields