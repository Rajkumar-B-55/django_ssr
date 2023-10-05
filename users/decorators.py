from functools import wraps

from django.contrib import messages
from django.shortcuts import render


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                error_message = 'You are not authorized to view this page'
                messages.success(request, message=error_message)
                return render(request, 'error_page.html', {'error_message': error_message}, status=403)

        return wrapper

    return decorator
