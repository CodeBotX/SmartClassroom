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
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'grades', GradesViewSet, basename='grades') 
router.register(r'planned-lessons', PlannedLessonViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('student/<str:user_id>/grades/', StudentGradesViewSet.as_view({'get': 'list'}), name='student-grades'),
    # path('top-students/', TopStudentsViewSet.as_view({'get': 'list'}), name='top-students'),
    path('assign-teacher/', TeacherAssignmentView.as_view(), name='assign-teacher'),
]
