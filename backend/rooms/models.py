# from django.db import models

# # Create your models here.

# # Bảng lớp học
# class Classes(models.Model):
#     class_name = models.CharField(max_length=127,unique=True) 
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