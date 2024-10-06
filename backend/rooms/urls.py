from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, SeatingPositionViewSet

router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'seating-positions', SeatingPositionViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
