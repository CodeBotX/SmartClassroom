from django.contrib import admin
from .models import *

# Registering the Semester model
@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name', 'day_begin', 'number_of_weeks', 'get_day_end')
    search_fields = ('name',)

class LessonAdmin(admin.ModelAdmin):
    list_display = ('id','semester','room', 'day', 'teacher')
    search_fields = ('id','name_lesson', 'subject', 'room__name', 'teacher__name')
    list_filter = ('semester', 'subject', 'room', 'teacher', 'day')
    ordering = ('semester', 'room', 'lesson_number')
    list_editable = ('day', 'teacher')

    # Optional: If you have custom validation or saving logic, you can override this method
    def save_model(self, request, obj, form, change):
        # Custom logic can be added here if needed
        super().save_model(request, obj, form, change)

admin.site.register(Lesson, LessonAdmin)

# Registering the Grades model
@admin.register(Grades)
class GradesAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'semester', 'score_type', 'grade')
    list_filter = ('subject', 'semester', 'score_type')
    search_fields = ('student__full_name', 'subject')


class PeriodAdmin(admin.ModelAdmin):
    list_display = ('number', 'start_time', 'end_time')  # Hiển thị các trường trong danh sách
    search_fields = ('number',)  # Tìm kiếm theo số tiết
    ordering = ('number',)  # Sắp xếp theo số tiết

admin.site.register(Period, PeriodAdmin)

class PlannedLessonAdmin(admin.ModelAdmin):
    list_display = ('subject', 'semester', 'lesson_number', 'name_lesson', 'room')
    search_fields = ('name_lesson', 'subject')
    list_filter = ('semester', 'subject', 'room')
    ordering = ('semester', 'lesson_number')
    list_per_page = 20

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('room', 'semester')  # Tối ưu hóa truy vấn

admin.site.register(PlannedLesson, PlannedLessonAdmin)

class ClassSubjectTeacherAssignmentAdmin(admin.ModelAdmin):
    list_display = ('room', 'subject', 'teacher')
    search_fields = ('room__name', 'subject', 'teacher__name')  # Giả sử có trường 'name' trong Room và Teacher
    list_filter = ('room', 'subject', 'teacher')

admin.site.register(ClassSubjectTeacherAssignment, ClassSubjectTeacherAssignmentAdmin)