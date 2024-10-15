from rest_framework import permissions

class IsTeacherOrAdmin(permissions.BasePermission):
    """
    Cho phép truy cập chỉ cho giáo viên hoặc quản trị viên.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_teacher or request.user.is_admin)
