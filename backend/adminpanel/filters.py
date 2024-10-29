


import django_filters
from django_filters import rest_framework as filters
from .models import *

class LessonFilter(filters.FilterSet):
    semester = filters.CharFilter(field_name='semester__name', lookup_expr='iexact')
    subject = filters.CharFilter(field_name='subject', lookup_expr='icontains')
    room = filters.CharFilter(field_name='room__name', lookup_expr='iexact')
    day = django_filters.DateFilter(field_name='day')
    day_range = filters.DateFromToRangeFilter(field_name='day')  
    teacher = filters.CharFilter(field_name='teacher__user_id', lookup_expr='exact')
    evaluate = filters.NumberFilter(field_name='evaluate')
    period = filters.CharFilter(field_name='period__number', lookup_expr='iexact')

    class Meta:
        model = Lesson
        fields = ['semester', 'subject', 'room', 'day_range','day', 'teacher', 'evaluate','period']


class GradesFilter(django_filters.FilterSet):
    student = django_filters.CharFilter(field_name='student__user__user_id', lookup_expr='exact')
    subject = django_filters.CharFilter(field_name='subject', lookup_expr='exact')
    semester = django_filters.CharFilter(field_name='semester__name', lookup_expr='exact')
    score_type = django_filters.CharFilter(field_name='score_type', lookup_expr='exact')

    class Meta:
        model = Grades
        fields = ['student', 'subject', 'semester', 'score_type']