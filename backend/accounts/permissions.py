from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Chỉ cho phép người dùng có vai trò admin truy cập.
    """
    def has_permission(self, request, view):
        # Kiểm tra nếu người dùng đã được xác thực và có vai trò 'admin'
        return request.user and request.user.is_authenticated and request.user.is_admin
