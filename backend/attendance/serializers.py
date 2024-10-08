from rest_framework import serializers
from .models import Attendance
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['student', 'lesson', 'status', 'attendance_time']  # Thêm 'attendance_time' nếu cần
        read_only_fields = ['attendance_time']  # Không cho phép sửa đổi thời gian điểm danh