from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(primary_key=True,max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Document(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/')  # Đường dẫn lưu trữ tệp
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Thời gian tải lên tự động
    updated_at = models.DateTimeField(auto_now=True)  # Thời gian cập nhật tự động
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='documents')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documents')

    def __str__(self):
        return self.title