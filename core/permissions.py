from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from functools import wraps

def user_has_total_access(user):
    """Verifica se o usuário tem acesso total."""
    return user.is_authenticated and (user.profile.has_total_access or user.is_staff)

def require_total_access(view_func):
    """
    Decorator que verifica se o usuário tem acesso total.
    Redireciona para a página de login se o usuário não estiver autenticado.
    Levanta PermissionDenied se o usuário não tiver acesso total.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if not user_has_total_access(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def is_admin(user):
    """Verifica se o usuário é administrador."""
    return user.is_authenticated and (user.is_staff or user.is_superuser)

def require_admin(view_func):
    """
    Decorator que verifica se o usuário é administrador.
    Redireciona para a página de login se o usuário não estiver autenticado.
    Levanta PermissionDenied se o usuário não for administrador.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if not is_admin(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view