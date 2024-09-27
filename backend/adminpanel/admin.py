from django.contrib import admin
from .models import Semester, StudyWeek, Lesson

# Tùy chỉnh hiển thị cho bảng Semester
@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('semester', 'day_begin', 'day_end')  # Hiển thị các trường quan trọng
    search_fields = ('semester',)  # Cho phép tìm kiếm theo học kỳ
    list_filter = ('day_begin', 'day_end')  # Cho phép lọc theo ngày bắt đầu và ngày kết thúc

    def save_model(self, request, obj, form, change):
        if not obj.day_end and obj.day_begin:
            obj.save()  # Tự động lưu `day_end` nếu chưa được đặt

# Tùy chỉnh hiển thị cho bảng StudyWeek
@admin.register(StudyWeek)
class StudyWeekAdmin(admin.ModelAdmin):
    list_display = ('week_number', 'semester')  # Hiển thị số tuần và học kỳ
    search_fields = ('week_number',)  # Cho phép tìm kiếm theo số tuần
    list_filter = ('semester',)  # Lọc theo học kỳ

# Tùy chỉnh hiển thị cho bảng Lesson
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('semester', 'day_of_week', 'room', 'subject', 'teacher', 'period')  # Hiển thị chi tiết bài học
    search_fields = ('subject', 'teacher__name')  # Tìm kiếm theo môn học và giáo viên
    list_filter = ('semester', 'day_of_week', 'room', 'teacher', 'subject')  # Cho phép lọc theo học kỳ, ngày trong tuần, phòng học, giáo viên và môn học
    ordering = ('semester', 'day_of_week', 'period')  # Sắp xếp theo học kỳ, ngày trong tuần và tiết học
