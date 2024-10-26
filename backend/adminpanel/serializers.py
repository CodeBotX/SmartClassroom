
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
        

# class PlannedLessonSerializer(serializers.ModelSerializer):
#     rooms = serializers.ListField(
#         child=serializers.CharField(max_length=10),
#         write_only=True  # Để không trả về trong response
#     )

#     class Meta:
#         model = PlannedLesson
#         fields = ['semester', 'subject', 'lesson_number', 'name_lesson', 'rooms']

#     def create(self, validated_data):
#         rooms = validated_data.pop('rooms')
#         lessons = []
#         for room in rooms:
#             lesson = PlannedLesson.objects.create(room=room, **validated_data)
#             lessons.append(lesson)
#         return lessons

class PlannedLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlannedLesson
        fields = '__all__'  # Hoặc bạn có thể chỉ định các trường cụ thể
    
#bảng phân công giáo viên
class TeacherAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAssignment
        fields = ['semester','teacher', 'room', 'subject']

# Tiết học
class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = ['number', 'start_time', 'end_time']