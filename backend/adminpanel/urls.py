# from django.urls import path
# from .views import SemesterCreateAPIView

# urlpatterns = [
#     path('semesters/', SemesterCreateAPIView.as_view(), name='create-semester'),
# ]

# -----------------------------------------------sử dụng viewset-----------------------------------------------
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'semesters', SemesterViewSet)
router.register(r'studyweeks', StudyWeekViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
