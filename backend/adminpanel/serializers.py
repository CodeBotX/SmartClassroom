
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

class GradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grades
        fields = '__all__'
        
# tạo thời khóa biểu  
class PlannedLessonSerializer(serializers.ModelSerializer):
    semester = serializers.PrimaryKeyRelatedField(queryset=Semester.objects.all())
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    class Meta:
        model = PlannedLesson
        fields = ['semester', 'subject', 'lesson_number', 'name_lesson', 'room']   
    def validate(self, data):
        return data

