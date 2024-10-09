from rest_framework import serializers
from .models import *

class DocumentSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)  # Trường đọc chỉ
    category = serializers.CharField(write_only=True)  # Trường ghi chỉ

    class Meta:
        model = Document
        fields = ['id', 'title', 'description', 'file', 'category', 'category_name', 'author']

    def validate_category(self, value):
        # Kiểm tra xem danh mục với tên được cung cấp có tồn tại không
        try:
            return Category.objects.get(name=value)
        except Category.DoesNotExist:
            raise serializers.ValidationError("Category with this name does not exist.")

    def create(self, validated_data):
        category_name = validated_data.pop('category')  # Lấy tên danh mục
        category = self.validate_category(category_name)  # Kiểm tra và lấy danh mục
        validated_data['category'] = category  # Gán danh mục vào validated_data
        return super().create(validated_data)  # Gọi phương thức tạo tài liệu

    def update(self, instance, validated_data):
        category_name = validated_data.pop('category', None)  # Lấy tên danh mục nếu có
        if category_name:
            category = self.validate_category(category_name)  # Kiểm tra và lấy danh mục
            validated_data['category'] = category  # Gán danh mục vào validated_data
        return super().update(instance, validated_data)  # Gọi phương thức cập nhật tài liệu

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']