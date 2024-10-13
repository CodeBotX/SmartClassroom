from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()
router.register(r'roomset', RoomViewSet)
router.register(r'seating-positions', SeatingPositionViewSet)

urlpatterns = [
    path('', include(router.urls)),  
    path('<str:room_name>/allseatings/', SeatingPositionListView.as_view(), name='allseatings'),
];