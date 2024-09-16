from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.contrib.auth.hashers import make_password

# Bảng người dùng
#(user name = id , pass  =  id)
class CustomUserManager(BaseUserManager):
    def create_user(self, full_name, **extra_fields):
        if not full_name:
            raise ValueError('Người dùng phải có họ và tên đầy đủ')

        user = self.model(full_name=full_name, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        superuser = self.model(username=username, **extra_fields)
        superuser.set_password(password)
        superuser.save(using=self._db)

        return superuser
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('parent', 'Phụ huynh'),
        ('student', 'Học sinh'),
        ('teacher', 'Giáo viên'),
        ('admin', 'Quản lý nhà trường'),
    ]
    user_id = models.CharField(max_length=8, unique=True, editable=False) 
    username = models.CharField(max_length=255, unique=True)  # Tên đăng nhập
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)  # Email
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Số điện thoại
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)  # Vai trò
    full_name = models.CharField(max_length=255)  # Họ và tên
    date_of_birth = models.DateField(null=True, blank=True)
    # password = models.CharField(max_length=255)  # Mật khẩu

    # User permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.full_name

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_teacher(self):
        return self.role == 'teacher'

    @property
    def is_student(self):
        return self.role == 'student'

    @property
    def is_parent(self):
        return self.role == 'parent'
    
    def save(self, *args, **kwargs):
    # Kiểm tra vai trò và đặt giá trị cho user_id, username, password
        if self.role in ['teacher', 'admin', 'student']:
            if not self.user_id:
                raise ValueError('Mã định danh Bộ GD&ĐT không được bỏ trống.')

            if not self.username:
                self.username = self.user_id  
            if not self.password:
                self.password = make_password(self.user_id) 
            
        elif self.role == 'parent':
            if not self.phone_number:
                raise ValueError('Số điện thoại không được bỏ trống đối với phụ huynh.')

            if not self.username:
                self.username = self.phone_number
            if not self.password:
                self.password = make_password(self.phone_number)  

        super().save(*args, **kwargs)
#--------------------------------------------------------------------------------------
# # Bảng học kỳ
# class Semester(models.Model):
#     year_begins = models.IntegerField()
#     year_ends = models.IntegerField()
#     semesters = models.IntegerField()

#     class Meta:
#         db_table = 'semester'

# # Bảng môn học
# class Subjects(models.Model):
#     subject_name = models.CharField(max_length=255)

#     class Meta:
#         db_table = 'subjects'



# # Bảng lớp học
# class Classes(models.Model):
#     class_name = models.CharField(max_length=127,unique=True) # bổ sung unique=True để tránh trường hợp trùng lặp so với bảng thiết kế
#     homeroom_teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'}, related_name='homeroom_classes')
#     def save(self, *args, **kwargs):
#         if self.homeroom_teacher.role != 'teacher':
#             raise ValueError("Giáo viên chủ nhiệm phải là giáo viên.")
#         super().save(*args, **kwargs)
#     def __str__(self):
#         return self.class_name
#     class Meta:
#         db_table = 'classes'
#         verbose_name = 'Lớp học'
#         verbose_name_plural = 'Các Lớp học'

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
        
# # Bảng bài giảng (tiết học)
# class Lessons(models.Model):
#     class_id = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name='lessons')
#     semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
#     subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
#     teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'}, related_name='lessons')
#     name_lesson = models.CharField(max_length=255)
#     period_number = models.IntegerField()
#     comment = models.TextField()

#     class Meta:
#         db_table = 'lessons'

# # Bảng thời khóa biểu
# class Timetables(models.Model):
#     semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='timetables')
#     day_of_week = models.IntegerField()  # Giá trị từ 0 đến 6
#     lesson_number = models.IntegerField()
#     lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, related_name='timetables')
    
#     def save(self, *args, **kwargs):
#         if not 0 <= self.day_of_week <= 6:
#             raise ValueError("Ngày trong tuần phải nằm trong khoảng từ 0 đến 6 (Chủ nhật đến Thứ Bảy).")   
#         if not 1 <= self.lesson_number <= 10:
#             raise ValueError("Số tiết học phải nằm trong khoảng từ 1 đến 10.")        
#         super().save(*args, **kwargs)       
#     def get_day_of_week_display(self):
#         days = ["Chủ nhật", "Thứ hai", "Thứ ba", "Thứ tư", "Thứ năm", "Thứ sáu", "Thứ bảy"]
#         return days[self.day_of_week]

#     class Meta:
#         db_table = 'timetables'
#         verbose_name = 'Thời khóa biểu'
#         verbose_name_plural = 'Các thời khóa biểu'
        


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


# # Bảng điểm danh
# class Attendance(models.Model):
#     student_id = models.ForeignKey(Students, on_delete=models.CASCADE,related_name='attendances')
#     class_id = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name='attendances')
#     lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, related_name='attendances')
#     status = models.BooleanField()

#     class Meta:
#         db_table = 'attendance'
#         verbose_name = 'Điểm danh'
#         verbose_name_plural = 'Danh sách điểm danh'

# # Bảng quản lý trường học
# class SchoolManagement(models.Model):
#     admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='school_managements')
#     action = models.BigIntegerField() # 1: Thêm, 2: Sửa, 3: Xóa + thông tin chi tiết
#     timestamp = models.BigIntegerField() # Thời gian thực hiện hành động

#     class Meta:
#         db_table = 'school_management'

