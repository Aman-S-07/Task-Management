from datetime import timezone
import random
import string
import uuid
from click import BaseCommand
from django.conf import settings
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from datetime import timedelta
from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=12)
    desc = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name


class user_task_list(models.Model):
    name = models.CharField(max_length=100)


class RegisterForm(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    confirm_password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=12, default='Mobile No.')


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    
class Task(models.Model):
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High')
    ]
    
    
    STATUS_CHOICES = [
        ('Not Started', 'Not Started',),
        ('In Progress', 'In Progress'),
        ( 'Completed', 'Completed'),

    ]
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    priority = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100)
    organizer = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Not Started')  
    remarks = models.TextField(blank=True, null=True, default="")
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks') 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks') 
    updated_by_admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_tasks')
    completed = models.BooleanField(default=False)
    re_attempt = models.BooleanField(default=False)
    attempts = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status', 'remarks']

class updatetaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'start_date', 'status','remarks','end_date', 'priority', 'description', 'location', 'organizer', 'assigned_to']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
        task_id = forms.IntegerField()
        status = forms.CharField(max_length=50)
        remarks = forms.CharField(max_length=255, required=False)
        


class Mentor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    expertise = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    
# Assuming you have a Profile model linked to User
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=12, default='Conatct No:')
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)
    mentor = models.ForeignKey(Mentor, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.username

class Intern(models.Model):
    intern_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(default='Enter your email')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    mobile_number = models.CharField(max_length=15)
    

    def get_full_name(self):
        return f"{self.intern.user.first_name} {self.intern.user.last_name}"

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def __str__(self):
        return self.description
    
class NotificationLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    email = models.EmailField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.task.name} sent to {self.email} on {self.sent_at}'
    
    
    



class PasswordResetRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    otp_expiry = models.DateTimeField()

    def generate_otp(self):
        return str(uuid.uuid4().int)[:6]

    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = self.generate_otp()
        self.otp_expiry = timezone.now() + timezone.timedelta(minutes=10)
        super().save(*args, **kwargs)

    def is_valid_otp(self, otp):
        return self.otp == otp and timezone.now() < self.otp_expiry and not self.is_used


from django.contrib.auth.decorators import login_required
from django.contrib import messages



@login_required
def mark_for_re_attempt(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if task.status == 'Completed':
        task.re_attempt = True
        task.status = 'In Progress'  # Change status back to "In Progress"
        task.save()
        messages.success(request, f'Task "{task.name}" has been marked for re-attempt.')
    else:
        messages.error(request, 'Only completed tasks can be marked for re-attempt.')

    return redirect('task_detail', task_id=task.id)