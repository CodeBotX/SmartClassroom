from django.contrib import admin
from .models import Room, SeatingPosition

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'homeroom_teacher_info')
    search_fields = ('name',)
    list_filter = ('homeroom_teacher',)
    def homeroom_teacher_info(self, obj):
        return f"{obj.homeroom_teacher.full_name} (ID: {obj.homeroom_teacher.user_id})"
    homeroom_teacher_info.short_description = 'Homeroom Teacher'

@admin.register(SeatingPosition)
class SeatingPositionAdmin(admin.ModelAdmin):
    list_display = ('student', 'room', 'row', 'column')
    search_fields = ('student__full_name', 'room__room_name')
    list_filter = ('room',)
