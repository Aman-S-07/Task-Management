from django.shortcuts import redirect

class InternRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_superuser:
            if not hasattr(request.user, 'intern'):
                return redirect('some_intern_creation_view')  
        response = self.get_response(request)
        return response
