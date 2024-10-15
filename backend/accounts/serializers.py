from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from .models import *

# Phần đăng ký
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        
# Serializer cho Teacher
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'
        
# Serializer cho Admin
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'
        
# Serializer cho Parent
class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'
        
# Serializer cho Student
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

#up file excel
class ExcelUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith('.xlsx'):
            raise serializers.ValidationError("Chỉ chấp nhận file Excel (.xlsx)")
        return value

# --------------------------------------------------------------------------------------
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number']

    def validate_email(self, value):
        # Kiểm tra nếu email đã được sử dụng
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email này đã được sử dụng.")
        return value

    def validate_phone_number(self, value):
        # Kiểm tra nếu số điện thoại đã được sử dụng
        if CustomUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Số điện thoại này đã được sử dụng.")
        return value
    
# đổi password
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
# --------------------------------------------------------------------------------------

#admin reset password
class AdminPasswordResetSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
# --------------------------------------------------------------------------------------