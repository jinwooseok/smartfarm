from functools import wraps
from django.core import exceptions
from rest_framework import exceptions

def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.session.get('user')
        if user is None:
            raise exceptions.NotAuthenticated()
        return view_func(request, *args, **kwargs)

    return _wrapped_view