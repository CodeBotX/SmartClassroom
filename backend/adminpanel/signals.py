from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TeacherAssignment, Lesson

@receiver(post_save, sender=TeacherAssignment)
def assign_teacher_to_existing_lessons(sender, instance, **kwargs):
    # Logic xử lý sau khi phân công giáo viên
    lessons = Lesson.objects.filter(room=instance.room, subject=instance.subject, teacher__isnull=True)
    lessons.update(teacher=instance.teacher)