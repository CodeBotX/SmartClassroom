import django_filters
from .models import Lesson

class LessonFilter(django_filters.FilterSet):
    semester = django_filters.NumberFilter(field_name='semester')
    subject = django_filters.CharFilter(field_name='subject', lookup_expr='icontains')
    room = django_filters.NumberFilter(field_name='room')
    day = django_filters.DateFilter(field_name='day')
    period = django_filters.NumberFilter(field_name='period')
    day_range = django_filters.DateFromToRangeFilter(field_name='day')

    class Meta:
        model = Lesson
        fields = ['semester', 'subject', 'room', 'day', 'period']
