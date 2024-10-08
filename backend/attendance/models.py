from django.db import models

class Attendance(models.Model):
    STATUS_CHOICES = [
        (1, 'Có mặt'),
        (2, 'Vắng mặt có phép'),
        (3, 'Vắng mặt không phép'),
        (4, 'Đi muộn'),
    ]   

    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, related_name='attendances')
    lesson = models.ForeignKey('adminpanel.Lesson', on_delete=models.CASCADE, related_name='attendances')
    status = models.IntegerField(choices=STATUS_CHOICES, null=True, blank=True)
    attendance_time = models.DateTimeField(auto_now_add=True)  
    
    class Meta:
        db_table = 'attendance'
        verbose_name = 'Điểm danh'
        verbose_name_plural = 'Danh sách điểm danh'

    def __str__(self):
        return f"{self.student_id} - {self.lesson} - {self.get_status_display()}"
    
class Device(models.Model):
    device_id = models.CharField(max_length=50, unique=True)
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE, related_name='devices')

    def __str__(self):
        return self.device_id