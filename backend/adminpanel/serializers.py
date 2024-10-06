
# -----------------------------------------------sử dụng viewset-----------------------------------------------
from rest_framework import serializers
from .models import *

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['semester', 'day_begin', 'number_of_weeks']

    def create(self, validated_data):
        semester = Semester.objects.create(**validated_data)
        for week_number in range(1, semester.number_of_weeks + 1):
            StudyWeek.objects.create(semester=semester, week_number=week_number)
        return semester

# class StudyWeekSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StudyWeek
#         fields = ['id', 'semester', 'week_number']


# class SemesterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Semester
#         fields = '__all__'

class StudyWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyWeek
        fields = '__all__'

class PlannedLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlannedLesson
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class GradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grades
        fields = '__all__'