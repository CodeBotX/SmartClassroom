
# -----------------------------------------------sử dụng viewset-----------------------------------------------
from rest_framework import serializers
from .models import *
from rooms.models import Room

# kì hoc
class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'
# Lesson
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
# BẢNG điểm 
class GradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grades
        fields = '__all__'
        
# tạo thời khóa biểu  
class PlannedLessonSerializer(serializers.ModelSerializer):
    semester = serializers.PrimaryKeyRelatedField(queryset=Semester.objects.all())
    rooms = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Room.objects.all()),
        required=True
    )

    class Meta:
        model = PlannedLesson
        fields = ['semester', 'subject', 'lesson_number', 'name_lesson', 'rooms']

    def validate(self, data):
        return data

#bảng phân công giáo viên
class TeacherAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSubjectTeacherAssignment
        fields = ['teacher', 'room', 'subject']

# Tiết học
class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = ['number', 'start_time', 'end_time']