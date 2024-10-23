from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'attendance', AttendanceViewSet, basename='attendance')
router.register(r'devices', DeviceViewSet, basename='device')
urlpatterns = [
    path('', include(router.urls)),
    path('rfid/start/', RFIDViewSet.as_view({'post': 'start'}), name='rfid-start'),
    # path('rfid/input/', RFIDViewSet.as_view({'post': 'input_student_id'}), name='rfid-input'),
    path('rfid/complete/', RFIDViewSet.as_view({'post': 'complete'}), name='rfid-complete'),
]
