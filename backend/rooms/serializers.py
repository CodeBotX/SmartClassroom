from rest_framework import serializers
from accounts.serializers import StudentSerializer, TeacherSerializer
from .models import Room, SeatingPosition
from accounts.models import Student,Teacher

class RoomSerializer(serializers.ModelSerializer):
    homeroom_teacher = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(), required=False
    )

    class Meta:
        model = Room
        fields = '__all__'
        
    def update(self, instance, validated_data):
        students_data = validated_data.pop('students', [])
        homeroom_teacher = validated_data.pop('homeroom_teacher', None)
        
        # Cập nhật các trường khác của lớp học
        instance = super().update(instance, validated_data)
        
        # Cập nhật danh sách học sinh nếu có
        if students_data:
            instance.students.set(students_data)

        # Cập nhật giáo viên chủ nhiệm nếu có
        if homeroom_teacher is not None:
            instance.homeroom_teacher = homeroom_teacher

        instance.save()
        return instance

class SeatingPositionSerializer(serializers.ModelSerializer):
    # student = StudentSerializer()
    student = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all()
    ) 
    student_details = StudentSerializer(source='student', read_only=True) 
    class Meta:
        model = SeatingPosition
        fields = '__all__'

