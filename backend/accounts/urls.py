from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', ApiLoginView.as_view(), name='api-dangnhap'),
    path('register-teacher/', APIRegisterTeacherView.as_view(), name='api-register-teacher'),
    path('register-student/', APIRegisterStudentView.as_view(), name='api-register-student'),
    path('register-parent/', APIRegisterParentView.as_view(), name='api-register-parent'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('detail/', UserDetailView.as_view(), name='user-detail'),
    path('update/', UserUpdateView.as_view(), name='user-update'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('admin-reset-password/', AdminPasswordResetView.as_view(), name='admin-reset-password'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

