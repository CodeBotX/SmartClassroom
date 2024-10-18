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
router.register(r'assignments', TeacherAssignmentViewSet, basename='teacher-assignment')
router.register(r'periods', PeriodViewSet, basename='period')

urlpatterns = [
    path('', include(router.urls)),
    path('grades/statistics/', GradesViewSet.as_view({'get': 'get_statistics'}), name='grades-statistics'),
]
