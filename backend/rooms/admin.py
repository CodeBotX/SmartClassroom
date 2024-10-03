from django.contrib import admin
from .models import Room, SeatingPosition, Attendance

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'homeroom_teacher')
    search_fields = ('room_name',)
    list_filter = ('homeroom_teacher',)

@admin.register(SeatingPosition)
class SeatingPositionAdmin(admin.ModelAdmin):
    list_display = ('student', 'room', 'row', 'column')
    search_fields = ('student__full_name', 'room__room_name')
    list_filter = ('room',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'status', 'attendance_time')
    search_fields = ('student__full_name', 'lesson__id')
    list_filter = ('status', 'lesson')
    date_hierarchy = 'attendance_time'

