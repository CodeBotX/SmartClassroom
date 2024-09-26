from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Student, Admin, Parent, Teacher, CustomUser

@receiver(post_delete, sender=Student)
@receiver(post_delete, sender=Admin)
@receiver(post_delete, sender=Parent)
@receiver(post_delete, sender=Teacher)
def delete_custom_user(sender, instance, **kwargs):
    """
    Xóa CustomUser khi xóa một trong các đối tượng liên quan như Student, Admin, Parent, Teacher
    """
    if instance.user:
        instance.user.delete()
