from rest_framework import viewsets
from .models import Room, SeatingPosition
from .serializers import RoomSerializer, SeatingPositionSerializer

# api room
class RoomViewSet(viewsets.ModelViewSet):
    authencation_classes = []
    permission_classes = []
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
# api chỗ ngồi
class SeatingPositionViewSet(viewsets.ModelViewSet):
    authencation_classes = []
    permission_classes = []
    queryset = SeatingPosition.objects.all()
    serializer_class = SeatingPositionSerializer

