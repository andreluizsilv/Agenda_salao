from django.shortcuts import redirect
from django.contrib import messages

def admin_congregacao_required(view_func):
    def wrapper(request, *args, **kwargs):
        profile = getattr(request.user, "profile", None)

        if not profile or not profile.is_admin_congregacao:
            messages.error(request, "Você não tem permissão para acessar esta área.")
            return redirect("escolher_mes")

        return view_func(request, *args, **kwargs)
    return wrapper

def superadmin_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not hasattr(request.user, "profile"):
            return redirect("login")

        if not request.user.profile.is_superadmin:
            messages.error(request, "Apenas o SuperAdmin pode acessar esta página.")
            return redirect("escolher_mes")

        return func(request, *args, **kwargs)
    return wrapper