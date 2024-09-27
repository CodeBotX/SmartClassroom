from django.db import models
from rooms.models import Room
from accounts.models import Teacher, Admin, Parent, Student
from datetime import timedelta

# Bảng học kỳ
class Semester(models.Model):
    day_begin = models.DateField()
    day_end = models.DateField(null=True, blank=True)
    semester = models.IntegerField(unique=True)
    class Meta:
        db_table = 'semester'
        verbose_name = 'Semester'
        verbose_name_plural = 'Semesters'

    def save(self, *args, **kwargs):
        if not self.day_end and self.day_begin:
            self.day_end = self.day_begin + timedelta(weeks=self.number_of_weeks)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Semester {self.semester} ({self.day_begin} - {self.day_end})"
   
# Bảng tuần học 
class StudyWeek(models.Model):
    semester = models.ForeignKey(Semester, related_name='study_weeks', on_delete=models.CASCADE)
    week_number = models.IntegerField()

    class Meta:
        db_table = 'study_week'
        verbose_name = 'Study Week'
        verbose_name_plural = 'Study Weeks'

    def __str__(self):
        return f"Week {self.week_number} of {self.semester}"
    
# Bảng DayChoices
class DayofWeek(models.TextChoices):
    MONDAY = 'Mon', 'Thứ 2'
    TUESDAY = 'Tue', 'Thứ 3'
    WEDNESDAY = 'Wed', 'Thứ 4'
    THURSDAY = 'Thu', 'Thứ 5'
    FRIDAY = 'Fri', 'Thứ 6'
    SATURDAY = 'Sat', 'Thứ 7'

# # Bảng môn học
class SubjectChoices(models.TextChoices):
    TOAN = 'Toan', 'Toán'
    VAN = 'Van', 'Ngữ Văn'
    ANH = 'Anh', 'Tiếng Anh'
    KHTN_HOA = 'KHTN_Hoa', 'Hoá'
    KHTN_LY = 'KHTN Ly', 'Vật lý'
    KHTN_SINH = 'KHTN Sinh', 'Sinh học'
    LSDL_DIA = 'LSĐL Dia', 'Địa lý'
    LSDL_SU = 'LSĐL Su', 'Lịch sử'
    GDCD = 'GDCD', 'GDCD'
    TD = 'TD', 'Thể dục'
    MT = 'My thuat', 'Mỹ thuật'
    AN = 'Am nhac', 'Âm nhạc'
    TH = 'Tin hoc', 'Tin học'
    CN = 'Cong Nghe', 'Công nghệ'
    HDTN_HN = 'HDTN HN', 'Hoạt động trại nghiệm, hướng nghiệp'

PERIOD_CHOICES = [(i, f'Tiết {i}') for i in range(1, 11)]

# Bảng lớp học
class Lesson(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=3,choices=DayofWeek.choices)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='lessons')
    subject = models.CharField(max_length=20, choices=SubjectChoices.choices) 
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    period = models.IntegerField(choices=PERIOD_CHOICES)
    class Meta:
        db_table = 'Lesson'
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
    
    
    
# -------------------------------------------------------------------------------

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


