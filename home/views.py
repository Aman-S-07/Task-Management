from email.headerregistry import Group
import random
from django.conf import settings
from django.shortcuts import render , redirect, get_object_or_404
from datetime import datetime
from django.utils import timezone
from django.views import View
from django.urls import reverse
from home.forms import LoginForm, OTPForm, RegistrationForm
from home.models import Contact 
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from home.models import  Task
from .models import  Category, PasswordResetRequest
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
import logging
from .forms import AdminProfileForm, AssignMentorForm, EditProfileForm, OTPVerificationForm, PasswordResetForm, PasswordResetRequestForm,  TaskForm, ProfileForm
from .models import Intern, Activity
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.models import Group, User
from django.db import transaction, IntegrityError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User, Group
from django.utils.dateparse import parse_date




logger = logging.getLogger(__name__)


def is_admin(user):
    return user.is_superuser

admin_required = user_passes_test(lambda user: user.is_superuser)



@login_required
@admin_required
def delete_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        task.delete()
    return redirect(reverse('category_list'))


@login_required
def index(request):
    context = {
        "variable1" : "oye bunny",
        "variable2" : "oye sun"
    }
    return render(request , 'index.html', context)

def home_page(request, task_id=None):
    task_id=task_id
    return render (request, 'index.html')





def generate_intern_id():
    last_intern = Intern.objects.last()
    if last_intern:
        return last_intern.intern_id + 1
    return 1


def Register(request):
    if request.method == 'POST':
        if 'otp' in request.POST:
            form = OTPForm(request.POST)
            if form.is_valid():
                otp = request.session.get('otp')
                if otp == form.cleaned_data['otp']:
                    form_data = request.session.get('form_data')

                    # Check if username already exists
                    if User.objects.filter(username=form_data['username'], email=form_data['email']).exists():
                        return render(request, 'register.html', {
                            'form': form,
                            'error_message': 'Username already exists. Please choose a different username.'
                        })

                    # Create the user
                    user = User.objects.create_user(
                        username=form_data['username'],
                        email=form_data['email'],
                        password=form_data['password'],
                        first_name=form_data['first_name'],
                        last_name=form_data['last_name']
                    )

                    # Assign the user as an intern by default, if not a superuser
                    if not user.is_superuser:
                        try:
                            with transaction.atomic():
                                intern_group, created = Group.objects.get_or_create(name='Intern')
                                user.groups.add(intern_group)

                                # Create Intern profile and assign intern_id
                                intern_profile = Intern.objects.create(user=user, intern_id=generate_intern_id())
                                intern_profile.save()
                        except IntegrityError:
                            # Handle the exception if the group was created by another process/thread
                            intern_group = Group.objects.get(name='Intern')
                            user.groups.add(intern_group)

                    # If admin flag is set, make the user staff
                    if form_data.get('is_admin'):
                        user.is_staff = True
                        user.save()

                    messages.success(request, 'You have successfully registered.')
                    return redirect('login')
                else:
                    form.add_error('otp', 'Invalid OTP')
        else:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                otp = send_otp(form.cleaned_data['email'])
                request.session['otp'] = str(otp)
                request.session['form_data'] = form.cleaned_data
                return render(request, 'register.html', {'form': form, 'otp_sent': True})
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form, 'otp_sent': False})


    

def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp(email):
    otp = random.randint(100000, 999999)
    send_mail('Your OTP', f'Your OTP is {otp}', 'from@example.com', [email])
    return otp


def verify_otp(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = request.session.get('otp')
            if otp == form.cleaned_data['otp']:
                form_data = request.session.get('form_data')
                user = User.objects.create_user(
                    username=form_data['username'],
                    email=form_data['email'],
                    password=form_data['password']
                )
                del request.session['otp']
                del request.session['form_data']
                return redirect('login')  # Replace with your success URL
            else:
                form.add_error('otp', 'Invalid OTP')
    else:
        form = OTPForm()

    return render(request, 'Verify_otp.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    messages.success(request, f'Successfully logged in as {username}')
                    login(request, user)
                    return redirect('home_page')  
                else:
                    messages.error(request, 'Account is inactive.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def Logout(request):
    logout(request)
    return render(request, 'logout.html')

def about(request):
    return render(request, 'about.html')



def password_reset_request_view(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.get(email=email)
            PasswordResetRequest.objects.filter(user=user).update(is_used=True)
            reset_request = PasswordResetRequest(user=user)
            reset_request.save()

            send_mail(
                'Your OTP for Password Reset',
                f'Your OTP is {reset_request.otp}. It is valid for 10 minutes.',
                'noreply@yourdomain.com',
                [email],
                fail_silently=False,
            )

            messages.success(request, 'OTP has been sent to your email.')
            return redirect(reverse('otp_verification') + f'?email={email}')
    else:
        form = PasswordResetRequestForm()

    return render(request, 'password_reset_request.html', {'form': form})

def otp_verification_view(request):
    email = request.GET.get('email')
    if not email:
        return redirect('password_reset_request')

    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('otp')
            user = User.objects.get(email=email)
            reset_request = PasswordResetRequest.objects.filter(user=user, is_used=False).first()

            if reset_request and reset_request.is_valid_otp(otp):
                reset_request.is_used = True
                reset_request.save()
                request.session['reset_user_id'] = user.id
                return redirect('password_reset')
            else:
                messages.error(request, 'Invalid OTP or OTP expired.')
    else:
        form = OTPVerificationForm(initial={'email': email})

    return render(request, 'otp_verification.html', {'form': form})

def password_reset_view(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('password_reset_request')

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = PasswordResetForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been reset successfully.')
            login(request, user)
            return redirect('home_page')
    else:
        form = PasswordResetForm(user)

    return render(request, 'password_reset.html', {'form': form})





@login_required
def create_task(request):
    if request.method == 'POST':
        status = request.POST.get('status')  
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        priority = request.POST.get('priority')
        description = request.POST.get('description')
        location = request.POST.get('location')
        organizer = request.POST.get('organizer')
        assigned_to_id = request.POST.get('assigned_to')
        
        try:
            assigned_to_user = User.objects.get(pk=assigned_to_id)
        except User.DoesNotExist:
            return render(request, 'error.html', {'error_message': 'Assigned user does not exist.'})
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M')
        except ValueError as e:
            return render(request, 'error.html', {'error_message': f'Invalid date format: {e}'})
        
        if not (name and category_id and start_date and end_date and priority and assigned_to_id):
            return render(request, 'error.html', {'error_message': 'All fields are required.'})

        try:
            task_category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return render(request, 'error.html', {'error_message': 'Category does not exist.'})
        
        task = Task.objects.create(
            name=name,
            category=task_category,
            start_date=start_date,
            end_date=end_date,
            priority=priority,
            description=description,
            location=location,
            organizer=organizer,
            assigned_to=assigned_to_user,
            status=status,
            created_by=request.user,
        )

        return redirect('user_task_list')
    else:
        form = TaskForm()
        categories = Category.objects.all()
        users = User.objects.all()
        return render(request, "create_task.html", {'form': form, 'categories': categories, 'users': users})

    
def error_message(request):
    return render (request , 'error.html')

def View_Task(request):
    return render (request , 'task.html')




@login_required
@admin_required
def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return redirect('category_list')
    return render (request, 'create_category.html')

@login_required
@admin_required
def Delete_Category(request, category_id):
    category = Category.objects.get(pk=category_id)
    if category.task_set.exists():
        messages.error(
            request, "You can not delete this category as it contains tasks"
        )
    else:
        category.delete()
        messages.success(request, "Category deleted successfully.")
        

@login_required
@admin_required
def Category_List(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories':categories})

@login_required
@admin_required
def Category_Task(request, category_id):
    category = get_object_or_404(Category, pk = category_id)
    task = category.task_set.all()
    return render(request, 'category_task.html', {'category':category, 'task':task})

@login_required
def Task_Chart(request):
    categories = Category.objects.all()
    pending_counts = {}
    for category in categories:
        # Count tasks with a start date greater than the current time
        count = Task.objects.filter(
            category=category,
            start_date__gt=timezone.now()
        ).count()
        pending_counts[category.name] = count

    return render(request, 'task_chart.html', {'pending_counts': pending_counts})

@login_required
def user_task_list(request, task_id=None):
    tasks = Task.objects.filter(assigned_to=request.user).exclude(status='Completed', updated_by_admin__isnull=False)
    
    if request.method == 'POST':
        # Handle form submissions or other POST requests
        task = Task.objects.get(id=task_id, assigned_to=request.user)
        
        new_status = request.POST.get('status')
        
        # Update task details
        if new_status:
            task.status = new_status
        
        task.save()
    
    # Render the template with the context data
    return render(request, 'user_task_list.html', {'tasks': tasks})



@login_required
@admin_required
def assign_mentor(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = AssignMentorForm(request.POST)
        if form.is_valid():
            mentor = form.cleaned_data['mentor']
            # Assuming you have a field in User or a related model to save the mentor
            user.profile.mentor = mentor
            user.profile.save()
            return redirect('user_detail', user_id=user.id)  # Adjust redirect as needed
    else:
        form = AssignMentorForm()
    return render(request, 'assign_mentor.html', {'form': form, 'user': user})





@admin_required
def close_task(request, task_id):
    activity = get_object_or_404(Activity, id=task_id)
    activity.completed = True
    activity.save()
    return redirect(reverse('activity_list')) 






def admin_required(function):
    return user_passes_test(lambda u: u.is_superuser)(function)


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date=datetime.today())
        contact.save()
        # Send email to admin
        send_mail(
            'New Contact Form Submission',
            f'Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {desc}',
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAILS],
        )
        messages.success(request, 'Your Message Has Been Sent!')
        return redirect('contact')  # Redirect to the contact page or another page

    return render(request, 'contact.html')







def get_full_name(self):
        return f"{self.intern.user.first_name} {self.intern.user.last_name}"

@login_required
def intern_profile(request, intern_id=None, user_id=None):
    user_id=user_id
    user = request.user

    # Determine the user to display
    if user.is_staff or user.is_superuser:
        if intern_id:
            intern = get_object_or_404(Intern, intern_id=intern_id) 
            user_to_display = intern.user
        else:
            intern = None
            user_to_display = user
    else:
        try:
            intern = Intern.objects.get(user=user)
            user_to_display = user
        except Intern.DoesNotExist:
            return HttpResponseNotFound("No Intern matches the given query.")

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_to_display)
        if form.is_valid():
            if user_to_display.email != form.cleaned_data['email']:
                if User.objects.filter(email=form.cleaned_data['email']).exclude(id=user_to_display.id).exists():
                    messages.error(request, 'This email is already in use by another account.')
                else:
                    user_to_display.email = form.cleaned_data['email']        
            form.save()
            user_to_display.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('intern_profile', intern_id=intern_id or user.id)
        else:
            messages.error(request, 'Error updating profile. Please correct the errors below.')


    else:
        form = ProfileForm(instance=intern)

    template_name = 'intern_profile_admin.html' if user.is_staff or user.is_superuser else 'intern_profile.html'

    context = {
        'form': form,
        'intern': intern,
        'user_to_display': user_to_display,
    }

    return render(request, template_name, context)




@login_required
def update_task_status(request, task_id=None):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)

        new_status = request.POST.get('status')

        task.status = new_status
        task.save()
        
        return redirect('user_task_list')
    
    return HttpResponse("Invalid request method.", status=405)










def some_view(request):
    intern = Intern.objects.get()
    url = reverse('intern_profile', kwargs=[intern.id])
    return redirect(url)








def intern_list(request):
    search_query = request.GET.get('search', '')

    try:
        interns_list = Intern.objects.filter(user__first_name__icontains=search_query)
        
        paginator_interns = Paginator(interns_list, 10)  
        page_number_interns = request.GET.get('page_interns', 1)
        interns = paginator_interns.get_page(page_number_interns)
    except Intern.DoesNotExist:
        interns = []

    context = {
        'interns': interns,
        'search_query': search_query,
    }

    return render(request, 'intern_list.html', context)






from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.shortcuts import render


def is_admin(user):
    return user.is_superuser or user.is_staff

@admin_required
def admin_dashboard(request):
    tasks = Task.objects.all().order_by('end_date')

    status_filter = request.GET.get('status')
    intern_filter = request.GET.get('intern')
    superuser_filter = request.GET.get('superuser')
    search_query = request.GET.get('q')
    start_date = request.GET.get('start_date') 
    end_date = request.GET.get('end_date')
    
    if status_filter:
        tasks = tasks.filter(status=status_filter)
        
    if intern_filter:
        if intern_filter.isdigit():  
            tasks = tasks.filter(
                Q(created_by__id=int(intern_filter)) |
                Q(assigned_to__id=int(intern_filter))
            )

    if superuser_filter == '1':  
        tasks = tasks.filter(created_by__is_superuser=True)

    if search_query:
        tasks = tasks.filter(
            Q(created_by__username__icontains=search_query) |  
            Q(assigned_to__username__icontains=search_query)
        )
    
    if start_date:
        start_date_parsed = parse_date(start_date)
        if start_date_parsed:
            tasks = tasks.filter(end_date__gte=start_date_parsed)

    if end_date:
        end_date_parsed = parse_date(end_date)
        if end_date_parsed:
            tasks = tasks.filter(end_date__lte=end_date_parsed)
    
    
    paginator = Paginator(tasks, 10)  
    page = request.GET.get('page')
    
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
    
    interns = User.objects.filter(is_staff=False)  # Assuming `User` model is used for interns
    
    return render(request, 'Dashboard.html', {
        'tasks': tasks,
        'interns': interns,
        'status_filter': status_filter,
        'intern_filter': intern_filter,
        'superuser_filter': superuser_filter, 
        'search_query': search_query,
        'start_date': start_date,
        'end_date': end_date,
    })








def completed_tasks(request):
    tasks = Task.objects.filter(status='Completed', assigned_to=request.user).exclude(updated_by_admin__isnull=True)
    return render(request, 'completed_task.html', {'tasks': tasks})

@user_passes_test(is_admin)
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.status = request.POST.get('status', task.status)
        task.remarks = request.POST.get('remarks', task.remarks)
        task.updated_by_admin = request.user
        task.save()
        
        send_mail(
            subject='Task Status Updated',
            message=f'The status of your task "{task.name}" has been updated to "{task.status}". Remarks: {task.remarks}',
            from_email= settings.EMAIL_HOST_USER,
            recipient_list=[task.assigned_to.email],  
            fail_silently=False,
        )
        
        if task.status == 'Completed':
            return redirect('admin_dashboard')

        return redirect('admin_dashboard')
        
    return render(request, 'update_task.html', {'task': task})






@admin_required
def daily_due_dates(request):
    today = timezone.now().date()
    tasks = Task.objects.filter(end_date=today).select_related('assigned_to').order_by('end_date')
    search_query = request.GET.get('q')
    
    if search_query:
        tasks = tasks.filter(
            Q(created_by__username__icontains=search_query) |  
            Q(assigned_to__username__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(tasks, 10)  # Show 10 tasks per page
    page = request.GET.get('page')
    
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    context = {
        'tasks': tasks,
        'search_query': search_query,
    }
    return render(request, 'Daily_Due_Date.html', context)







def edit_profile(request, intern_id):
    intern_id=intern_id
    intern = Intern.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=intern)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('intern_profile', intern_id=intern_id)  # Replace 'intern_profile' with the name of the profile view
    else:
        form = EditProfileForm(instance=intern)
    
    context = {
        'form': form,
        'intern': intern,
    }
    return render(request, 'edit_profile.html', context)



class InternProfileView(View):
    def get(self, request, intern_id=None):
        if intern_id is None:
            interns = Intern.objects.all()  # Get all interns if no intern_id is provided
        else:
            intern = get_object_or_404(Intern, pk=intern_id)  # Use pk for primary key lookup
            interns = [intern]
        return render(request, 'intern_profile_view.html', {'interns': interns})


        
# def edit_profile_admin(request, user_id=None):
#     if user_id is None:
#         user = request.user
#     else:
#         user = get_object_or_404(User, user_id=user_id)
    
#     if request.method == 'POST':
#         form = AdminProfileForm(request.POST, request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('intern_profile', user_id=user.id)  
#     else:
#         form = AdminProfileForm(instance=user)

#     context = {
#         'form': form,
#         'user': user, 
#     }
    
#     return render(request, 'edit_profile_admin.html', context)        

@admin_required
def edit_profile_admin(request):
    user = request.user
    user_id = user.id
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = AdminProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            # Render the updated user object in the template
            return render(request, 'intern_profile_admin.html')
        else:
            messages.error(request, 'Error updating profile. Please correct the errors below.')
    else:
        form = AdminProfileForm(instance=user)

    return render(request, 'edit_profile_admin.html', {'form': form, 'user': user})





@login_required
def mark_for_re_attempt(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if task.status == 'Completed':
        task.re_attempt = True
        task.status = 'In Progress'  # Change status back to "In Progress"
        task.save()

        # Send an email notification (optional)
        send_mail(
            'Task Marked for Re-Attempt',
            f'The task "{task.name}" has been marked for re-attempt.',
            'from@example.com',
            [task.assigned_to.email],
            fail_silently=False,
        )

        messages.success(request, f'Task "{task.name}" has been marked for re-attempt.')
    else:
        messages.error(request, 'Only completed tasks can be marked for re-attempt.')

    return redirect('user_task_list', task_id=task.id)



def reattempt_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST' and task.assigned_to == request.user:
        task.status = "Not Started"  # Reset the task status
        task.attempts += 1 
        task.save()
        messages.success(request, 'Task re-attempted successfully!')
    return redirect('user_task_list', category_id=task.category.id)