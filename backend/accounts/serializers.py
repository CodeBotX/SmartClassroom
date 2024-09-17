from rest_framework import serializers
from .models import CustomUser




class ExcelUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith('.xlsx'):
            raise serializers.ValidationError("Chỉ chấp nhận file Excel (.xlsx)")
        return value

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'username', 'user_id', 'role', 'phone_number', 'date_of_birth']
        
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'phone_number', 'date_of_birth']  # Các trường có thể cập nhật
        extra_kwargs = {
            'email': {'required': False},
            'phone_number': {'required': False},
            'date_of_birth': {'required': False}
        }