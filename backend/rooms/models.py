from django.db import models


# Bảng lớp học
class Room(models.Model):
    name = models.CharField(primary_key=True,max_length=127,unique=True) 
    students = models.ManyToManyField('accounts.Student', related_name='rooms')
    homeroom_teacher = models.ForeignKey('accounts.Teacher', on_delete=models.SET_NULL, related_name='homeroom_rooms', blank=True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'room'
        verbose_name = 'room'
        verbose_name_plural = 'rooms'
        

# Bảng SeatingPosition để quản lý vị trí ngồi của học sinh trong lớp
class SeatingPosition(models.Model):
    student = models.OneToOneField(
        'accounts.Student', 
        primary_key=True,
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
         return f"Student {self.student.full_name} in Room {self.room.name} at position ({self.row}, {self.column})"

