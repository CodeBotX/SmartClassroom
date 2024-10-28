# import django_filters
# from .models import Lesson

# class LessonFilter(django_filters.FilterSet):
#     semester = django_filters.NumberFilter(field_name='semester')
#     subject = django_filters.CharFilter(field_name='subject', lookup_expr='icontains')
#     room = django_filters.CharFilter(field_name='room__name',lookup_expr='iexact')
#     day = django_filters.DateFilter(field_name='day')
#     period = django_filters.NumberFilter(field_name='period')
#     day_range = django_filters.DateFromToRangeFilter(field_name='day')

#     class Meta:
#         model = Lesson
#         fields = ['semester', 'subject', 'room', 'day', 'period']


import django_filters
from django_filters import rest_framework as filters
from .models import Lesson

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
