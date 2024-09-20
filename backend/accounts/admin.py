from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user_id', 'role', 'phone_number','email', 'date_of_birth')
    search_fields = ('full_name', 'user_id', 'phone_number')
    list_filter = ('role',)
    ordering = ('-date_of_birth',)

    fields = ('full_name', 'username','password', 'user_id', 'role','phone_number','email', 'date_of_birth')
    readonly_fields = ('user_id',)
