from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Congregacao

User = get_user_model()


class UsuarioCreationForm(UserCreationForm):
    nome_completo = forms.CharField(max_length=200, required=True, label="Nome completo",
                                   widget=forms.TextInput(attrs={"class": "form-control"}))
    congregacao = forms.ModelChoiceField(
        queryset=Congregacao.objects.all(),
        required=False,
        label="Congregação",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta:
        model = User
        fields = ("username", "nome_completo", "congregacao", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get("nome_completo", "")
        if commit:
            user.save()
            # criar profile
            from .models import UsuarioProfile
            perfil, created = UsuarioProfile.objects.get_or_create(user=user)
            perfil.congregacao = self.cleaned_data.get("congregacao")
            perfil.save()
        return user
