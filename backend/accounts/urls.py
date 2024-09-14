from django.urls import path
from .views import *


urlpatterns = [
    path('dangnhap/', LoginView.as_view(), name='api-dangnhap'),
]

