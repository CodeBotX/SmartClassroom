
# -----------------------------------------------sử dụng viewset-----------------------------------------------
from rest_framework import serializers
from .models import *
from rooms.models import Room

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['semester', 'day_begin', 'number_of_weeks']

    def create(self, validated_data):
        semester = Semester.objects.create(**validated_data)
        for week_number in range(1, semester.number_of_weeks + 1):
            StudyWeek.objects.create(semester=semester, week_number=week_number)
        return semester



class StudyWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyWeek
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class GradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grades
        fields = '__all__'
        
# tạo thời khóa biểu


class CreateLessonSerializer(serializers.Serializer):
    semester = serializers.PrimaryKeyRelatedField(queryset=Semester.objects.all())
    subject = serializers.CharField(max_length=20)
    lesson_number = serializers.IntegerField()
    name_lesson = serializers.CharField(max_length=100)
    rooms = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=Room.objects.all()))
    
    
class PlannedLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlannedLesson
        fields = ['semester', 'subject', 'lesson_number', 'name_lesson', 'room']   
    def validate(self, data):
        return data