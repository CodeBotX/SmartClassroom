import django_filters
from .models import Attendance

class AttendanceFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name='user__id', lookup_expr='icontains')
    lesson = django_filters.CharFilter(field_name='lesson__id', lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=Attendance.STATUS_CHOICES)

    class Meta:
        model = Attendance
        fields = ['user', 'lesson', 'status']
