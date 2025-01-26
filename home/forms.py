import re
from django import forms
from .models import Activity, Intern
from django.contrib.auth.models import User
from .models import Activity, Mentor
from home.models import Category
from .models import Task
from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ValidationError



class UpdateTaskForm(forms.ModelForm):
    status = forms.CharField(max_length=50)
    remarks = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Task
        fields = ['status', 'remarks']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=30, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    mobile_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password', 'confirm_password', 'mobile_number']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')


        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
            
        if password:
            if len(password) < 8:
                self.add_error('password', "Password must be at least 8 characters long.")
            if not re.search(r"[A-Z]", password):
                self.add_error('password', "Password must contain at least one uppercase letter.")
            if not re.search(r"[a-z]", password):
                self.add_error('password', "Password must contain at least one lowercase letter.")
            if not re.search(r"[0-9]", password):
                self.add_error('password', "Password must contain at least one digit.")
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                self.add_error('password', "Password must contain at least one special character.")

        return cleaned_data

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)
    
    
    
class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError('No user is associated with this email address.')
        return email

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6)
    email = forms.EmailField()

class PasswordResetForm(SetPasswordForm):
    email = forms.EmailField()
    otp = forms.CharField(max_length=6)





    

            
# class VerifyOtpForm(forms.Form):
#     otp = forms.CharField(label="OTP", max_length=6)
#     new_password = forms.CharField(label="New Password", widget=forms.PasswordInput)
#     confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)            
    


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        exclude = ['created_at', 'updated_at'] 
        fields = ['user', 'first_name', 'last_name', 'description', 'completed']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class AssignMentorForm(forms.Form):
    mentor = forms.ModelChoiceField(queryset=Mentor.objects.all(), empty_label="Select Mentor")





class TaskForm(forms.ModelForm):
    task_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Task
        fields = ['name', 'category','status','remarks', 'assigned_to', 'start_date', 'end_date', 'priority', 'description', 'location', 'organizer']
        
        
class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status']
        
class InternForm(forms.ModelForm):
    class Meta:
        model = Intern
        fields = ['email', 'username' ,'first_name', 'last_name', 'profile_picture', 'mobile_number' ] 
        
        
        

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Intern
#         fields = ['username', 'email', 'first_name', 'last_name', 'profile_picture']



class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(required=False)
    mobile_number = forms.CharField(max_length=15)

    class Meta:
        model = Intern
        fields = ['email', 'profile_picture', 'first_name', 'last_name', 'username', 'mobile_number']  

    def __init__(self, *args, **kwargs):
        # Initialize form instance with extra arguments, if provided
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        
        
        
        


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    mobile_number = forms.CharField(max_length=15)
    
    
    
    
    class Meta:
        model = Intern
        fields = ['first_name', 'last_name', 'email', 'profile_picture', 'mobile_number'] 

    def save(self, commit=True):
        intern = super().save(commit=False)
        user = intern.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.mobile_number = self.cleaned_data['mobile_number']
        if commit:
            user.save()
            intern.save()
        return intern
    
    
class AdminProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)
    mobile_number = forms.CharField(required=False)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile_picture', 'mobile_number'] 
   
        
    
        
class EditAdminProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(required=False)  # Optional field for profile picture
    mobile_number = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile_picture', 'mobile_number']

    def save(self, commit=True):
        Admin = super().save(commit=False)
        user = User.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.profile_picture = self.cleaned_data['profile_picture']
        user.mobile_number = self.cleaned_data['mobile_number']
        if commit:
            user.save()
            Admin.save()
        return Admin       