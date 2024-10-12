from django.contrib import admin
from .models import *


class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_students_count', 'homeroom_teacher')
    search_fields = ('name',)
    filter_horizontal = ('students',)  
    def get_students_count(self, obj):
        return obj.students.count()
    get_students_count.short_description = 'Số lượng học sinh'  
admin.site.register(Room, RoomAdmin)

class SeatingPositionAdmin(admin.ModelAdmin):
    list_display = ('student', 'room', 'row', 'column')
    search_fields = ('student__full_name', 'room') 
    list_filter = ('room',)
    ordering = ('room', 'row', 'column')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('student', 'room')

admin.site.register(SeatingPosition, SeatingPositionAdmin)

