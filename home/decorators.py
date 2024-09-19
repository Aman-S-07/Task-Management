# home/decorators.py
from django.shortcuts import redirect
from .models import Mentor
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from .models import Intern


'''
def mentor_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not Mentor.objects.filter(user=request.user).exists():
            return redirect('Home')  # or some other page
        return view_func(request, *args, **kwargs)
    return wrapper_func
    
'''
from django.http import HttpRequest

def test_func(request: HttpRequest) -> bool:
    # Now you can access the user attribute
    if request.user:
        pass
    return True




def admin_required(function):
    """
    Decorator to ensure the user is an admin.
    """
    return user_passes_test(lambda u: u.is_superuser, login_url='login')(function)

def user_is_intern(function):
    """
    Decorator to ensure the user is an intern.
    """
    return user_passes_test(lambda u: hasattr(u, 'intern'), login_url='login')(function)

def intern_required(function):
    """
    Decorator to ensure the user is an intern and the intern exists.
    """
    def wrap(request, *args, **kwargs):
        intern_id = kwargs.get('intern_id')
        intern = get_object_or_404(Intern, id=intern_id)
        if request.user.intern == intern:
            return function(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized to access this intern's data.")
    return wrap
