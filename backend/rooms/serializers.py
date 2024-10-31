from rest_framework import serializers
from accounts.serializers import StudentSerializer
from .models import Room, SeatingPosition

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        
    def update(self, instance, validated_data):
        students_data = validated_data.pop('students', [])
        instance = super().update(instance, validated_data)
        if students_data:
            instance.students.set(students_data)
        return instance

class SeatingPositionSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    class Meta:
        model = SeatingPosition
        fields = '__all__'

