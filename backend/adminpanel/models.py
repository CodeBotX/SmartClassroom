from django.db import models
from rooms.models import Room
from accounts.models import Teacher, Admin, Parent, Student
from datetime import timedelta


# Bảng học kỳ   
class Semester(models.Model):
    semester = models.IntegerField(primary_key=True)
    day_begin = models.DateField()
    number_of_weeks = models.IntegerField()

    class Meta:
        db_table = 'semester'
        verbose_name = 'Semester'
        verbose_name_plural = 'Semesters'

    def get_day_end(self):
        return self.day_begin + timedelta(weeks=self.number_of_weeks)

    def __str__(self):
        day_end = self.get_day_end()
        return f"Semester {self.semester} ({self.day_begin} - {day_end})"


# Bảng tuần học 
class StudyWeek(models.Model):
    semester = models.ForeignKey(Semester, related_name='study_weeks', on_delete=models.CASCADE)
    week_number = models.IntegerField()

    class Meta:
        db_table = 'study_week'
        verbose_name = 'Study Week'
        verbose_name_plural = 'Study Weeks'

    def get_week_dates(self):
        start_date = self.semester.day_begin + timedelta(weeks=self.week_number - 1)
        end_date = start_date + timedelta(days=6)
        return start_date, end_date

    def __str__(self):
        return f"Week {self.week_number} of Semester {self.semester.semester}"


   
# # Bảng môn học (choice)
class SubjectChoices(models.TextChoices):
    TOAN = 'Toan', 'Toán'
    VAN = 'Van', 'Ngữ Văn'
    ANH = 'Anh', 'Tiếng Anh'
    KHTN_HOA = 'Hoa', 'Hoá'
    KHTN_LY = 'Ly', 'Vật lý'
    KHTN_SINH = 'Sinh', 'Sinh học'
    KHXH_DIA = 'Dia', 'Địa lý'
    KHXH_SU = 'Su', 'Lịch sử'
    KHXH_GDCD = 'GDCD', 'GDCD'
    TD = 'TD', 'Thể dục'
    MT = 'MT', 'Mỹ thuật'
    AN = 'AN', 'Âm nhạc'
    TH = 'TH', 'Tin học'
    CN = 'CN', 'Công nghệ'
    HDTN_HN = 'HDTN-HN', 'Hoạt động trại nghiệm, hướng nghiệp'

PERIOD_CHOICES = [(i, f'Tiết {i}') for i in range(1, 11)]

class PlannedLesson(models.Model):
    subject = models.CharField(max_length=20, choices=SubjectChoices.choices)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    lesson_number = models.IntegerField()  # Tiết thứ bao nhiêu trong môn
    name_lesson = models.CharField(max_length=100)  # Tên bài học

    class Meta:
        unique_together = ('subject', 'semester', 'lesson_number')
        verbose_name = 'Planned Lesson'
        verbose_name_plural = 'Planned Lessons'

    def __str__(self):
        return f"{self.subject} - Tiết {self.lesson_number}: {self.name_lesson} (Kỳ {self.semester})"

# Bảng tiet hoc
class Lesson(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    day = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='lessons')
    period_number = models.IntegerField(choices=PERIOD_CHOICES)
    planned_lesson = models.ForeignKey(PlannedLesson, on_delete=models.SET_NULL, null=True, blank=True)  
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    evaluate = models.IntegerField(null=True, blank=True)
    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'

    def get_weekday(self):
        day_names = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ Nhật']
        return day_names[self.day.weekday()]

    def __str__(self):
        return f"Lesson on {self.get_weekday()}, Period {self.period_number}"
    
    
# -------------------------------------------------------------------------------
# Bảng điểm
class Grades(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject = models.CharField(max_length=20, choices=SubjectChoices.choices)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    grade = models.FloatField()  

    class Meta:
        db_table = 'grades'
        unique_together = ('student', 'subject') 
        verbose_name = 'Điểm'
        verbose_name_plural = 'Các điểm'

    def save(self, *args, **kwargs):
        if not 0 <= self.grade <= 10:
            raise ValueError("Điểm phải nằm trong khoảng từ 0 đến 10.") 
        self.grade = round(self.grade, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.full_name} - Môn {self.subject.subject_name} - Điểm: {self.grade}"



# # Bảng quản lý trường học
# class SchoolManagement(models.Model):
#     admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='school_managements')
#     action = models.BigIntegerField() # 1: Thêm, 2: Sửa, 3: Xóa + thông tin chi tiết
#     timestamp = models.BigIntegerField() # Thời gian thực hiện hành động

#     class Meta:
#         db_table = 'school_management'



