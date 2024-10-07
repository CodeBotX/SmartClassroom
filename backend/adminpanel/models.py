from django.db import models
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
    id = models.CharField(primary_key=True, max_length=10)
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
    def save(self, *args, **kwargs):
        self.id = f"{self.semester.semester}{self.week_number}"
        super().save(*args, **kwargs)  
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

class Period(models.Model):
    number = models.IntegerField(primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    def __str__(self):
        return f'Tiết {self.number}'
    
class PlannedLesson(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject = models.CharField(max_length=20, choices=SubjectChoices.choices)
    lesson_number = models.IntegerField()  
    name_lesson = models.CharField(max_length=100) 
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE, related_name='planned_lessons')
    class Meta:
        unique_together = ('subject', 'semester', 'lesson_number','room')
        verbose_name = 'Planned Lesson'
        verbose_name_plural = 'Planned Lessons'

    def __str__(self):
        return f"{self.subject} - Tiết {self.lesson_number}: {self.name_lesson} (Kỳ {self.semester})"

# Bảng tiet hoc
class Lesson(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='lessons')
    subject = models.CharField(max_length=20, choices=SubjectChoices.choices)
    lesson_number = models.IntegerField()  # Tiết thứ bao nhiêu trong môn
    name_lesson = models.CharField(max_length=100)  # Tên bài học
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE, related_name='lessons')
    day = models.DateField(null=True, blank=True)  # Ngày học (có thể là null khi chỉ mới lập kế hoạch)
    period = models.ForeignKey(Period, on_delete=models.CASCADE, related_name='lessons', null=True, blank=True)  # Tiết học
    teacher = models.ForeignKey('accounts.Teacher', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    evaluate = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
        unique_together = ('semester', 'room', 'subject','day','period')

    def __str__(self):
        return f"{self.subject} - Tiết {self.lesson_number}: {self.name_lesson} (Phòng {self.room}, Kỳ {self.semester})"
    
# -------------------------------------------------------------------------------
class ScoreType(models.TextChoices):
    MIENG = '15p', 'Điểm 15p'
    MOT_TIET = '1Tiet', 'Điểm 1 tiết'
    GIUA_KY = 'GiuaKy', 'Điểm giữa kỳ'
    CUOI_KY = 'CuoiKy', 'Điểm cuối kỳ'
# Bảng điểm
class Grades(models.Model):
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, related_name='grades')
    subject = models.CharField(max_length=20, choices=SubjectChoices.choices)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    score_type = models.CharField(max_length=10, choices=ScoreType.choices)
    grade = models.FloatField()

    class Meta:
        db_table = 'grades'
        unique_together = ('student', 'subject', 'semester', 'score_type') 
        verbose_name = 'Điểm'
        verbose_name_plural = 'grades'

    def save(self, *args, **kwargs):
        if not 0 <= self.grade <= 10:
            raise ValueError("Điểm phải nằm trong khoảng từ 0 đến 10.") 
        self.grade = round(self.grade, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.full_name} - Môn {self.get_subject_display()} - {self.get_score_type_display()} - Điểm: {self.grade}"




