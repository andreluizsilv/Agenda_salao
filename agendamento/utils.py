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
