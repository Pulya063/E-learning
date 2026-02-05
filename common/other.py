from django.contrib import messages
from django.shortcuts import redirect

def check_user_group(group_name):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "You do not have permission to view this page.")
                return redirect('login')
        return wrapper
    return decorator
