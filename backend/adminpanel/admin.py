from django.contrib import admin
from .models import *

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name', 'day_begin', 'number_of_weeks', 'get_day_end')
    search_fields = ('name',)

#Lesson
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id','semester','room', 'day', 'teacher')
    search_fields = ('id','name_lesson', 'subject', 'room__name', 'teacher__name')
    list_filter = ('semester', 'subject', 'room', 'teacher', 'day')
    ordering = ('semester', 'room', 'lesson_number')
    list_editable = ('day', 'teacher')
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

admin.site.register(Lesson, LessonAdmin)

# Điểm
@admin.register(Grades)
class GradesAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'semester', 'score_type', 'grade')
    list_filter = ('subject', 'semester', 'score_type')
    search_fields = ('student__full_name', 'subject')

#Tiết học
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('number', 'start_time', 'end_time')
    search_fields = ('number',)  
    ordering = ('number',)
admin.site.register(Period, PeriodAdmin)


# Kế hoạch bài học
class PlannedLessonAdmin(admin.ModelAdmin):
    list_display = ('subject', 'semester', 'lesson_number', 'name_lesson', 'room')
    search_fields = ('name_lesson', 'subject')
    list_filter = ('semester', 'subject', 'room')
    ordering = ('semester', 'lesson_number')
    list_per_page = 20

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('room', 'semester')
admin.site.register(PlannedLesson, PlannedLessonAdmin)



# Phân công giáo viên
class TeacherAssignmentAdmin(admin.ModelAdmin):
    list_display = ('room', 'subject', 'teacher')
    search_fields = ('room__name', 'subject', 'teacher__name') 
    list_filter = ('room', 'subject', 'teacher')

admin.site.register(TeacherAssignment, TeacherAssignmentAdmin)