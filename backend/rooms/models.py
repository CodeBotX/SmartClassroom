from django.db import models

# Bảng lớp học
class Room(models.Model):
    room_name = models.CharField(max_length=127,unique=True) 
    homeroom_teacher = models.ForeignKey('accounts.Teacher', on_delete=models.CASCADE, related_name='homeroom_classes')
    def save(self, *args, **kwargs):
        if self.homeroom_teacher.role != 'teacher':
            raise ValueError("Giáo viên chủ nhiệm phải là giáo viên.")
        super().save(*args, **kwargs)
    def __str__(self):
        return self.room_name
    class Meta:
        db_table = 'room'
        verbose_name = 'room'
        verbose_name_plural = 'rooms'

# Bảng SeatingPosition để quản lý vị trí ngồi của học sinh trong lớp
class SeatingPosition(models.Model):
    student = models.OneToOneField(
        'accounts.Student', 
        on_delete=models.CASCADE, 
        related_name='seating_position'
    )
    room = models.ForeignKey(
        Room, 
        on_delete=models.CASCADE, 
        related_name='seating_positions'
    )
    row = models.IntegerField()
    column = models.IntegerField()

    class Meta:
        db_table = 'seating_position'
        verbose_name = 'Seating Position'
        verbose_name_plural = 'Seating Positions'
        unique_together = ('room', 'row', 'column') 

    def __str__(self):
        return f"Student {self.student.full_name} in Room {self.room.room_name} at position ({self.row}, {self.column})"

class Attendance(models.Model):
    STATUS_CHOICES = [
        (1, 'Có mặt'),
        (2, 'Vắng mặt có phép'),
        (3, 'Vắng mặt không phép'),
        (4, 'Đi muộn'),
    ]

    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, related_name='attendances')
    lesson = models.ForeignKey('adminpanel.Lesson', on_delete=models.CASCADE, related_name='attendances')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    attendance_time = models.DateTimeField(auto_now_add=True)  
    
    class Meta:
        db_table = 'attendance'
        verbose_name = 'Điểm danh'
        verbose_name_plural = 'Danh sách điểm danh'

    def __str__(self):
        return f"{self.student_id} - {self.lesson} - {self.get_status_display()}"