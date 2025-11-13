from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from agendamento.models import Congregacao

User = get_user_model()


class CongregacaoForm(forms.ModelForm):
    class Meta:
        model = Congregacao
        fields = ["nome", "responsavel"]
        labels = {
            "nome": "Nome da Congregação",
            "responsavel": "Responsável",
        }
        widgets = {
            "nome": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Digite o nome da congregação"
            }),
            "responsavel": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Digite o nome do responsável"
            }),
        }


class UsuarioCreationForm(UserCreationForm):
    nome_completo = forms.CharField(
        max_length=200,
        required=True,
        label="Nome completo",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    congregacao = forms.ModelChoiceField(
        queryset=Congregacao.objects.all(),
        required=False,
        empty_label="Selecione a congregação",
        label="Congregação",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta:
        model = User
        fields = ("username", "nome_completo", "congregacao", "password1", "password2")
