from rest_framework import serializers
from .models import *

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'user', 'lesson', 'status', 'attendance_time']  # Cập nhật tên trường ở đây

    def create(self, validated_data):
        return Attendance.objects.create(**validated_data)


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['device_id', 'room']
