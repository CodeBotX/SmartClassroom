from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.apps import apps
from django.utils import timezone

# Bảng người dùng
#(user name = id , pass  =  id)
class CustomUserManager(BaseUserManager):
    def create_user(self,user_id, full_name, **extra_fields):
        if not full_name:
            raise ValueError('Người dùng phải có họ và tên đầy đủ')
        if not user_id:
                raise ValueError('Không tìm thấy mã định danh Bộ GD&ĐT.')
        user = self.model(user_id=user_id,full_name=full_name, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self,user_id, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)


        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        superuser = self.model(user_id=user_id,username=username, **extra_fields)
        superuser.set_password(password)
        superuser.save(using=self._db)

        return superuser

class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(primary_key=True, max_length=8, editable=False)  # Làm khóa chính, không cần unique=True
    username = models.CharField(max_length=255, unique=True)  # Tên đăng nhập, unique để đảm bảo duy nhất
    full_name = models.CharField(max_length=255)
    sex = models.CharField(max_length=32, null=True, blank=True)
    nation = models.CharField(max_length=32, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True) 
    phone_number = models.CharField(max_length=32, null=True, blank=True)
    day_of_birth = models.DateField(null=True, blank=True)
    
    # Vai trò
    is_parent = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    # User permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)  # Thời gian tạo tài khoản
    last_login = models.DateTimeField(auto_now=True)  # Tự động cập nhật khi đăng nhập

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'  # Trường sử dụng để đăng nhập
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if self.is_teacher or self.is_admin or self.is_student:
            if not self.user_id:
                raise ValueError('Mã định danh Bộ GD&ĐT không được bỏ trống.')

            if not self.username:
                self.username = str(self.user_id)  
            if not self.password:
                self.password = make_password(str(self.user_id)) 

        elif self.is_parent:
            if not self.phone_number:
                raise ValueError('Số điện thoại không được bỏ trống.')
            if not self.username:
                self.username = str(self.phone_number)
            if not self.password:
                self.password = make_password(self.phone_number)  

        super().save(*args, **kwargs)
        
        
class Teacher(models.Model):
    user = models.OneToOneField(CustomUser,primary_key=True, on_delete=models.CASCADE, related_name='teacher')
    active_status = models.CharField(max_length=355, null=True, blank=True)
    contract_types= models.CharField(max_length=255, null=True, blank=True)
    expertise_levels = models.CharField(max_length=255, null=True, blank=True)
    subjects = models.TextField(null=True, blank=True)

class Admin(models.Model):
    user = models.OneToOneField(CustomUser,primary_key=True, on_delete=models.CASCADE,related_name='admin')
    active_status = models.CharField(max_length=355, null=True, blank=True)
    contract_types= models.CharField(max_length=255, null=True, blank=True)
    expertise_levels = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=32, null=True, blank=True)

class Parent(models.Model):
    user = models.OneToOneField(CustomUser,primary_key=True, on_delete=models.CASCADE,related_name='parent')
    address = models.CharField(max_length=255, null=True, blank=True)

  
class Student(models.Model):
    user = models.OneToOneField(CustomUser,primary_key=True, on_delete=models.CASCADE,related_name='student') 
    room = models.ForeignKey('rooms.Room',null=True, blank=True, default=None,related_name='students', on_delete=models.SET_NULL)
    parent = models.ForeignKey(Parent, null=True, blank=True, default=None, on_delete=models.SET_NULL,related_name='students')   
    active_status = models.CharField(max_length=355, null=True, blank=True)


#--------------------------------------------------------------------------------------





# # Bảng sinh học sinh
# class Students(models.Model):
#     full_name = models.CharField(max_length=127)  
#     class_id = models.ForeignKey(
#         Classes, 
#         on_delete=models.CASCADE, 
#         related_name='students'  
#     )
#     parent_id = models.ForeignKey(
#         CustomUser, 
#         on_delete=models.CASCADE, 
#         limit_choices_to={'role': 'parent'}, 
#         related_name='parent_students'  
#     )

#     def save(self, *args, **kwargs):
#         if self.parent_id.role != 'parent':
#             raise ValueError("Người dùng được chọn phải là phụ huynh.")
#         super().save(*args, **kwargs)  

#     def __str__(self):
#         return self.full_name  

#     class Meta:
#         db_table = 'students'  
#         verbose_name = 'Học sinh'
#         verbose_name_plural = 'Các Học sinh'
        



        


# # Bảng điểm
# class Grades(models.Model):
#     student_id = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='grades')
#     subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE, related_name='grades')
#     semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
#     lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, related_name='grades')
#     grade = models.FloatField()  # float, làm tròn đến 2 chữ số

#     class Meta:
#         db_table = 'grades'
#         unique_together = ('student_id', 'subject_id')  # Khóa chính tổ hợp
#         verbose_name = 'Điểm'
#         verbose_name_plural = 'Các điểm'

#     def save(self, *args, **kwargs):
#         # Kiểm tra giá trị của grade (phải nằm trong khoảng từ 0 đến 10)
#         if not 0 <= self.grade <= 10:
#             raise ValueError("Điểm phải nằm trong khoảng từ 0 đến 10.") 
#         # Làm tròn điểm đến 2 chữ số thập phân
#         self.grade = round(self.grade, 2)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.student_id.full_name} - Môn {self.subject_id.subject_name} - Điểm: {self.grade}"



# # Bảng quản lý trường học
# class SchoolManagement(models.Model):
#     admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='school_managements')
#     action = models.BigIntegerField() # 1: Thêm, 2: Sửa, 3: Xóa + thông tin chi tiết
#     timestamp = models.BigIntegerField() # Thời gian thực hiện hành động

#     class Meta:
#         db_table = 'school_management'

