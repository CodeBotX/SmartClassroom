from django.contrib import admin
from .models import *

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'get_status', 'attendance_time')
    list_filter = ('status', 'lesson', 'attendance_time')
    search_fields = ('user__username', 'lesson__title')
    date_hierarchy = 'attendance_time'
    ordering = ('-attendance_time',)

    def get_status(self, obj):
        return obj.get_status_display()
    get_status.short_description = 'Trạng thái'

admin.site.register(Attendance, AttendanceAdmin)

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'room')
    search_fields = ('device_id',)
    list_filter = ('room',)
    ordering = ('device_id',)

admin.site.register(Device, DeviceAdmin)