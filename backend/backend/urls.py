
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('adminpanel/', include('adminpanel.urls')),
    path('rooms/', include('rooms.urls')),
]
