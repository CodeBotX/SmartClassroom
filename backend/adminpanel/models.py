# from django.db import models


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


