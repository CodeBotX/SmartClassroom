from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from .models import *

# Phần đăng ký
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'user_id', 'full_name', 'phone_number', 'day_of_birth', 'email', 'is_teacher', 'is_admin', 'is_parent', 'is_student']

# Serializer cho Teacher
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['active_status', 'contract_types', 'expertise_levels', 'subjects']

# Serializer cho Admin
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['active_status', 'contract_types', 'expertise_levels', 'description']

# Serializer cho Parent
class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['address','students']

# Serializer cho Student
class StudentSerializer(serializers.ModelSerializer):
    room = serializers.CharField(source='room.name', read_only=True)
    parent = serializers.CharField(source='parent.user.full_name', read_only=True)

    class Meta:
        model = Student
        fields = ['active_status', 'room', 'parent']

#up file excel
class ExcelUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith('.xlsx'):
            raise serializers.ValidationError("Chỉ chấp nhận file Excel (.xlsx)")
        return value

# --------------------------------------------------------------------------------------


# update thông tin user
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'sex', 'nation', 'email', 'phone_number', 'day_of_birth']
        read_only_fields = ['user_id','username']

class TeacherUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()  # Serializer lồng ghép để cập nhật thông tin user

    class Meta:
        model = Teacher
        fields = ['user', 'active_status', 'contract_types', 'expertise_levels', 'subjects']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()
        return super().update(instance, validated_data)

class AdminUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()  # Serializer lồng ghép

    class Meta:
        model = Admin
        fields = ['user', 'active_status', 'contract_types', 'expertise_levels', 'description']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()
        return super().update(instance, validated_data)

class ParentUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()

    class Meta:
        model = Parent
        fields = ['user', 'address']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()
        return super().update(instance, validated_data)

class StudentUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()

    class Meta:
        model = Student
        fields = ['user', 'room', 'parent', 'active_status']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()
        return super().update(instance, validated_data)



# --------------------------------------------------------------------------------------

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