from django_filters import rest_framework as filters
from .models import Teacher, Admin, Parent, Student

class TeacherFilter(filters.FilterSet):
    user_id = filters.CharFilter(field_name='user__user_id', lookup_expr='icontains')
    full_name = filters.CharFilter(lookup_expr='icontains')
    active_status = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Teacher
        fields = ['user_id', 'full_name', 'active_status']

class AdminFilter(filters.FilterSet):
    user_id = filters.CharFilter(field_name='user__user_id', lookup_expr='icontains')
    full_name = filters.CharFilter(lookup_expr='icontains')
    active_status = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Admin
        fields = ['user_id', 'full_name', 'active_status']

class ParentFilter(filters.FilterSet):
    user_id = filters.CharFilter(field_name='user__user_id', lookup_expr='icontains')
    full_name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Parent
        fields = ['user_id', 'full_name']

class StudentFilter(filters.FilterSet):
    user_id = filters.CharFilter(field_name='user__user_id', lookup_expr='icontains')
    full_name = filters.CharFilter(lookup_expr='icontains')
    active_status = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Student
        fields = ['user_id', 'full_name', 'active_status']
