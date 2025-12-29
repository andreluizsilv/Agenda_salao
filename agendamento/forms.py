from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class PrimeiroUsuarioForm(UserCreationForm):
    """Form para o PRIMEIRO usuário (cria congregação)
       → Também torna o usuário superadmin do Django automaticamente
    """

    nome_completo = forms.CharField(
        max_length=200,
        required=True,
        label="Nome completo",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ex: João da Silva"
        })
    )

    nome_congregacao = forms.CharField(
        max_length=150,
        required=True,
        initial="Congregação Principal",
        label="Nome da Congregação",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ex: Congregação Central"
        }),
        help_text="Este será o nome da congregação principal do sistema"
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ex: joao.silva"
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Crie uma senha segura"
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Digite a mesma senha novamente"
        })
    )

    class Meta:
        model = User
        fields = ("username", "nome_completo", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)

        # salva nome completo
        user.first_name = self.cleaned_data.get("nome_completo", "")

        # 🔥 TORNA O PRIMEIRO USUÁRIO SUPERADMIN NO DJANGO
        # isso garante acesso total ao /admin
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True

        if commit:
            user.save()
        return user


class UsuarioCreationForm(UserCreationForm):
    nome_completo = forms.CharField(
        max_length=200,
        required=True,
        label="Nome completo",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ex: João da Silva"
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ex: joao.silva"
        })
    )

    # 🔥 CORREÇÃO: Carrega queryset apenas quando necessário
    congregacao = forms.ModelChoiceField(
        queryset=None,  # Inicialmente vazio
        required=False,
        label="Congregação",
        widget=forms.Select(attrs={
            "class": "form-select",
            "data-bs-toggle": "tooltip",
            "title": "Selecione a congregação a qual você pertence."
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Crie uma senha segura"
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Digite a mesma senha novamente"
        })
    )

    class Meta:
        model = User
        fields = ("username", "nome_completo", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 🔥 Carrega as congregações apenas se a tabela existir
        try:
            from .models import Congregacao
            self.fields['congregacao'].queryset = Congregacao.objects.all()
        except:
            # Se não conseguir (tabela não existe), deixa vazio
            self.fields['congregacao'].queryset = Congregacao.objects.none()
            self.fields['congregacao'].help_text = "Aguarde um administrador criar congregações"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get("nome_completo", "")
        if commit:
            user.save()
            # O perfil será criado na view
        return user