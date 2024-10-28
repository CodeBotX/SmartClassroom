from django.db import models
from datetime import timedelta, date

# Bảng học kỳ   
class Semester(models.Model):
    name = models.IntegerField(primary_key=True)
    day_begin = models.DateField()
    number_of_weeks = models.IntegerField()

    class Meta:
        db_table = 'semester'
        verbose_name = 'Semester'
        verbose_name_plural = 'Semesters'

    def get_day_end(self):
        return self.day_begin + timedelta(weeks=self.number_of_weeks)
    @property
    def day_end(self):
        return self.get_day_end()
    def get_week(self, input_date=None):
        if input_date is None:
            input_date = date.today()  
        if input_date < self.day_begin:
            return None 
        delta_days = (input_date - self.day_begin).days
        current_week = (delta_days // 7) + 1
        if current_week > self.number_of_weeks:
            return None  
        return current_week


    def __str__(self):
        day_end = self.get_day_end()
        return f"{self.name}"

   
# # Bảng môn học (choice)
class SubjectChoices(models.TextChoices):
    TOAN = 'TOAN', 'Toán'
    VAN = 'VAN', 'Ngữ Văn'
    ANH = 'ANH', 'Tiếng Anh'
    KHTN_HOA = 'KHTN_HOA', 'Hoá'
    KHTN_LY = 'KHTN_LY', 'Vật lý'
    KHTN_SINH = 'KHTN_SINH', 'Sinh học'
    KHXH_DIA = 'KHXH_DIA', 'Địa lý'
    KHXH_SU = 'KHXH_SU', 'Lịch sử'
    KHXH_GDCD = 'KHXH_GDCD', 'GDCD'
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
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='planned_lessons')
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
    lesson_number = models.IntegerField(null=True, blank=True) 
    name_lesson = models.CharField(max_length=100, null=True, blank=True) 
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE, related_name='lessons')
    day = models.DateField()  
    period = models.ForeignKey(Period, on_delete=models.CASCADE, related_name='lessons') 
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
    TX = 'TX', 'Đánh giá thường xuyên'
    GK = 'GK', 'Điểm giữa kỳ'
    CK = 'CK', 'Điểm cuối kỳ'
# Bảng điểm
class Grades(models.Model):
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, related_name='grades') 
    subject = models.CharField(max_length=20, choices=SubjectChoices.choices)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    score_type = models.CharField(max_length=10, choices=ScoreType.choices)
    grade = models.FloatField()

    class Meta:
        db_table = 'grades'
        verbose_name = 'Điểm'
        verbose_name_plural = 'grades'
    
    @staticmethod
    def calculate_average(student_id, subject, semester_id):
        grades = Grades.objects.filter(student__id=student_id, subject=subject, semester__id=semester_id)
        
        tx_grades = grades.filter(score_type=ScoreType.TX)
        gk_grade = grades.filter(score_type=ScoreType.GK).first()
        ck_grade = grades.filter(score_type=ScoreType.CK).first()

        if tx_grades.exists():
            tx_average = tx_grades.aggregate(tx_avg=models.Avg('grade'))['tx_avg']
        else:
            tx_average = 0
        gk = gk_grade.grade if gk_grade else 0
        ck = ck_grade.grade if ck_grade else 0
        total_weight = 1 + 2 + 3  
        weighted_total = (tx_average * 1) + (gk * 2) + (ck * 3)
        average_score = weighted_total / total_weight
        return round(average_score, 2)

    def save(self, *args, **kwargs):
        if not 0 <= self.grade <= 10:
            raise ValueError("Điểm phải nằm trong khoảng từ 0 đến 10.") 
        self.grade = round(self.grade, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.full_name} - Môn {self.get_subject_display()} - {self.get_score_type_display()} - Điểm: {self.grade}"


class TeacherAssignment(models.Model):
    semester= models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='assignments')
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE, related_name='assignments')
    subject = models.CharField(max_length=20, choices=SubjectChoices.choices)
    teacher = models.ForeignKey('accounts.Teacher', on_delete=models.CASCADE, related_name='assignments')

    class Meta:
        unique_together = ('room', 'subject')  
