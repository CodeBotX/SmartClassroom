from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password




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


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Mật khẩu cũ không chính xác.")
        return value

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Mật khẩu mới phải có ít nhất 8 ký tự.")
        return value

class AdminPasswordResetSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
