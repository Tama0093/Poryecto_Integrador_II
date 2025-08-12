from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def group_required(group_names):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            if request.user.groups.filter(name__in=group_names).exists():
                return view_func(request, *args, **kwargs)
            return redirect('home')
        return _wrapped
    return decorator
