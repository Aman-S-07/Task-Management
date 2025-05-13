

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views
from .views import InternProfileView, intern_list


urlpatterns = [
    # Main views
    path('', views.login_view, name='login'),
    path('home', views.home_page, name='home_page'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('register', views.Register, name='register'),
    path('logout', views.Logout, name='logout'),
    path('logout/login', views.login_view, name='login'),
    path('login', views.login_view, name='login'),
    path('error', views.error_message, name='error_message'),

    # Tasks
    path('tasks', views.user_task_list, name='user_task_list'),
    path('create', views.create_task, name='create_task'),
    path('create_task', views.create_task, name='create_task'),
    path('chart', views.Task_Chart, name='task_chart'),
    path('tasks/<int:task_id>/view', views.View_Task, name='view_task'),
    path('tasks/<int:task_id>/update', views.update_task, name='update_task'),
    path('tasks/<int:task_id>/update-status', views.update_task_status, name='update_task_status'),

   

    # Charts
    path('tasks', views.Task_Chart, name='task_chart'),
    path('Task_Chart', views.Task_Chart, name='task_chart'),

    # Interns
    path('intern_list', views.intern_list, name='intern_list'),
    path('intern_profile', views.intern_profile, name='intern profile'),
    path('intern_profile_admin', views.intern_profile, name='Admin profile'),
    path('intern_list', views.intern_list, name='intern_list'),
    path('intern_list/<int:intern_id>', views.intern_list, name='intern_list'),
   

    
    # Admin dashboard
    path('Dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('Dashboard/tasks', views.user_task_list, name='admin_user_task_list'),
    path('tasks/<int:id>/update', views.update_task, name='update_task'),
    path('Dashboard/interns', views.intern_list, name='admin_intern_list'),
    path('Dashboard/interns/<int:intern_id>', views.intern_profile, name='admin_intern_profile'),
    path('edit_profile_admin', views.edit_profile_admin, name='admin_edit_profile'),
    
    path('edit_profile_admin/<int:user_id>', views.edit_profile_admin, name='admin_edit_profile_id'),
    


    #completed task
    path('completed_task', views.completed_tasks, name='completed task'),
    path('tasks/completed', views.completed_tasks, name='completed_tasks'),

    # DUe Date Tasks
    path('Daily_Due_Date', views.daily_due_dates, name='daily_due_dates'),
    
    
    # Profile
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('edit_profile/<int:intern_id>', views.edit_profile, name='edit_profile'),
    path('edit_profile/home/', views.home_page, name='Home Page'),
    path('interns/<int:intern_id>/', views.intern_profile, name='intern_profile'),
    path('intern_profile_admin', views.intern_profile, name='intern_profile'),
    path('intern_profile_admin/<int:user_id>', views.intern_profile, name='intern_profile'),
    path('intern/<int:intern_id>/', InternProfileView.as_view(), name='intern_profile_view'),

    
    path('intern_profile_view', InternProfileView.as_view(), name='intern profile'),
    path('intern_profile_view/<int:intern_id>', InternProfileView.as_view(), name='intern profile'),
    
    # Reset Password
    path('password_reset_request', views.password_reset_request_view, name='password_reset_request'),
    path('otp-verification/', views.otp_verification_view, name='otp_verification'),
    path('reset-password/', views.password_reset_view, name='password_reset'),

 
    # Re-Attempt
    path('reattempt_task/<int:task_id>/', views.reattempt_task, name='reattempt_task'),
        

    # Static and media files handling
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



    
