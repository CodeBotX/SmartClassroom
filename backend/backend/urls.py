
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/adminpanel/', include('adminpanel.urls')),
    path('api/rooms/', include('rooms.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/documents/', include('Appdocuments.urls')),
]
