from django.shortcuts import render, redirect
from django.contrib import messages
from agendamento.forms import UsuarioCreationForm, CongregacaoForm

# Create your views here.

def login_view(request):
    return render(request, 'login.html')



def cadastro(request):
    if request.method == "POST":
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            form.save_m2m()
            messages.success(request, "Conta criada com sucesso! Faça login.")
            return redirect("login")
        else:
            messages.error(request, "Corrija os erros abaixo.")
    else:
        form = UsuarioCreationForm()

    return render(request, "cadastro.html", {"form": form})



def cadastrar_congregacao(request):
    if request.method == "POST":
        form = CongregacaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congregação cadastrada com sucesso!")
            return redirect("cadastrar_congregacao")
        else:
            messages.error(request, "Corrija os erros abaixo.")
    else:
        form = CongregacaoForm()

    return render(request, "cadastro_congregacao.html", {"form": form})
