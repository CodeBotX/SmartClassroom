# from rest_framework import serializers
# from .models import Semester, StudyWeek

# class SemesterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Semester
#         fields = ['semester', 'day_begin', 'number_of_weeks']

# -----------------------------------------------sử dụng viewset-----------------------------------------------
from rest_framework import serializers
from .models import Semester, StudyWeek

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
        fields = ['id', 'semester', 'week_number']