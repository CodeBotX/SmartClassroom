from django.contrib import admin
from .models import Semester, StudyWeek, PlannedLesson, Lesson

# Hiển thị thông tin chi tiết của học kỳ
@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('semester', 'day_begin', 'number_of_weeks')
    search_fields = ('semester',)
    list_filter = ('day_begin', 'number_of_weeks')

# Hiển thị tuần học trong học kỳ
@admin.register(StudyWeek)
class StudyWeekAdmin(admin.ModelAdmin):
    list_display = ('semester', 'week_number')
    list_filter = ('semester',)
    search_fields = ('semester__semester', 'week_number')

# Hiển thị tiết học đã được lên kế hoạch
@admin.register(PlannedLesson)
class PlannedLessonAdmin(admin.ModelAdmin):
    list_display = ('subject', 'semester', 'lesson_number', 'name_lesson')
    list_filter = ('subject', 'semester')
    search_fields = ('name_lesson', 'subject', 'semester__semester')

# Hiển thị thông tin tiết học
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('semester', 'study_week', 'day', 'period_number', 'room', 'teacher', 'get_weekday', 'planned_lesson', 'evaluate')
    list_filter = ('semester', 'study_week', 'period_number', 'room', 'teacher')
    search_fields = ('room__name', 'teacher__name', 'planned_lesson__name_lesson')
    date_hierarchy = 'day'
    ordering = ('day', 'period_number')

    # Hiển thị tên tuần (thứ 2 - chủ nhật)
    def get_weekday(self, obj):
        return obj.get_weekday()
    get_weekday.short_description = 'Weekday'

