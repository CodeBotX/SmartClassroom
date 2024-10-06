from rest_framework import serializers
from .models import Room, SeatingPosition

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class SeatingPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatingPosition
        fields = '__all__'

