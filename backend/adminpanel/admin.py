from django.contrib import admin
from .models import Semester, StudyWeek, PlannedLesson, Lesson, Grades

# Registering the Semester model
@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('semester', 'day_begin', 'number_of_weeks', 'get_day_end')
    search_fields = ('semester',)

# Registering the StudyWeek model
@admin.register(StudyWeek)
class StudyWeekAdmin(admin.ModelAdmin):
    list_display = ('semester', 'week_number')
    list_filter = ('semester',)
    search_fields = ('semester__semester', 'week_number')

# Registering the PlannedLesson model
@admin.register(PlannedLesson)
class PlannedLessonAdmin(admin.ModelAdmin):
    list_display = ('subject', 'semester', 'lesson_number', 'name_lesson')
    list_filter = ('subject', 'semester')
    search_fields = ('name_lesson',)

# Registering the Lesson model
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('semester', 'day', 'room', 'period_number', 'planned_lesson', 'teacher')
    list_filter = ('semester', 'room', 'teacher')
    search_fields = ('planned_lesson__name_lesson', 'teacher__full_name')

# Registering the Grades model
@admin.register(Grades)
class GradesAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'semester', 'score_type', 'grade')
    list_filter = ('subject', 'semester', 'score_type')
    search_fields = ('student__full_name', 'subject')

