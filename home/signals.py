from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Intern, Task
from .models import User

# @receiver(post_save, sender=Task)
# def send_due_date_notification(sender, instance, **kwargs):
#     end_date = instance.end_date

#     if instance.status in ['In Progress'] and end_date <= timezone.now().date() + timedelta(days=1):
#         subject = f'Task "{instance.name}" is nearing its due date'
#         message = f'Dear {instance.assigned_to.username},\n\nYour task "{instance.name}" is due on {instance.end_date}. Please make sure to complete it on time.'
#         email_from = settings.EMAIL_HOST_USER
#         recipient_list = [instance.assigned_to.email]
#         send_mail(subject, message, email_from, recipient_list)




@receiver(post_save, sender=User)
def create_intern_profile(sender, instance, created, **kwargs):
    if created and not instance.is_superuser: 
        Intern.objects.create(user=instance)
        
        
from django.contrib.auth.models import User, Group
        
@receiver(post_save, sender=User)
def add_user_to_intern_group(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        intern_group, created = Group.objects.get_or_create(name='intern')
        instance.groups.add(intern_group)        