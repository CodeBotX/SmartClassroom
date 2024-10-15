from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password

# Bảng người dùng
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
    user_id = models.CharField(primary_key=True, max_length=8, editable=False)  
    username = models.CharField(max_length=255, unique=True)  
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True) 
    phone_number = models.CharField(max_length=32,unique=True, null=True, blank=True)
    
    # Vai trò
    is_parent = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    # User permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)  
    last_login = models.DateTimeField(auto_now=True)  
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'  
    REQUIRED_FIELDS = ['user_id']

    def __str__(self):
        return self.username or self.user_id

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
        
# Các đối tượng người dùng (Sau phát triển thành app thông tin cá nhân)
class Teacher(models.Model):
    user = models.OneToOneField(CustomUser,primary_key=True, on_delete=models.CASCADE, related_name='teacher')
    full_name = models.CharField(max_length=255)
    sex = models.CharField(max_length=32, null=True, blank=True)
    day_of_birth = models.DateField(null=True, blank=True)
    nation = models.CharField(max_length=32, null=True, blank=True)
    active_status = models.CharField(max_length=355, null=True, blank=True)
    contract_types= models.CharField(max_length=255, null=True, blank=True)
    expertise_levels = models.CharField(max_length=255, null=True, blank=True)
    subjects = models.TextField(null=True, blank=True)
    def get_teacher_id(self):
        return self.user.user_id
    def __str__(self):
        return f"{self.full_name} - {self.user.user_id}"
    class Meta:
        db_table = 'Teacher'
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

class Admin(models.Model):
    user = models.OneToOneField(CustomUser,primary_key=True, on_delete=models.CASCADE,related_name='admin')
    full_name = models.CharField(max_length=255)
    sex = models.CharField(max_length=32, null=True, blank=True)
    day_of_birth = models.DateField(null=True, blank=True)
    nation = models.CharField(max_length=32, null=True, blank=True)
    active_status = models.CharField(max_length=355, null=True, blank=True)
    contract_types= models.CharField(max_length=255, null=True, blank=True)
    expertise_levels = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=32, null=True, blank=True)
    def get_admin_id(self):
        return self.user.user_id
    def __str__(self):
        return f"{self.full_name} - {self.user.user_id}"
    class Meta:
        db_table = 'Admin'
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'

class Parent(models.Model):
    user = models.OneToOneField(CustomUser,primary_key=True, on_delete=models.CASCADE,related_name='parent')
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    def get_parent_id(self):
        return self.user.user_id
    def __str__(self):
        return f"{self.full_name} - {self.user.user_id}"
    class Meta:
        db_table = 'Parent'
        verbose_name = 'Parent'
        verbose_name_plural = 'Parents'
    

  
class Student(models.Model):
    user = models.OneToOneField(CustomUser,primary_key=True, on_delete=models.CASCADE,related_name='student') 
    full_name = models.CharField(max_length=255)
    sex = models.CharField(max_length=32, null=True, blank=True)
    day_of_birth = models.DateField(null=True, blank=True)
    nation = models.CharField(max_length=32, null=True, blank=True)
    parent = models.ForeignKey(Parent, null=True, blank=True, default=None, on_delete=models.SET_NULL,related_name='students')   
    active_status = models.CharField(max_length=355, null=True, blank=True)
    def get_student_id(self):
        return self.user.user_id
    def __str__(self):
        return f"{self.full_name} - {self.user.user_id}"
    class Meta:
        db_table = 'Student'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


#--------------------------------------------------------------------------------------

