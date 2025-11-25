from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime, date, timedelta, time
import calendar
from .forms import *
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()

MESES_PT = [
    "Janeiro","Fevereiro","Março","Abril","Maio","Junho",
    "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"
]


def login_view(request):
    if request.user.is_authenticated:
        return redirect("escolher_mes")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("escolher_mes")
        messages.error(request, "Usuário ou senha inválidos.")
        return redirect("cadastro")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def cadastro(request):
    if request.user.is_authenticated:
        return redirect("escolher_mes")

    if request.method == "POST":
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Conta criada com sucesso. Faça login.")
            return redirect("login")
        else:
            messages.error(request, "Corrija os erros abaixo.")
    else:
        form = UsuarioCreationForm()
    return render(request, "cadastro.html", {"form": form})


# helper para adicionar meses sem dependency externa
def add_months(dt: date, months: int) -> date:
    month = dt.month - 1 + months
    year = dt.year + month // 12
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


@login_required
def escolher_mes(request):
    hoje = date.today().replace(day=1)
    meses = []
    for i in range(7):
        data = add_months(hoje, i)
        meses.append({
            "numero": data.month,
            "ano": data.year,
            "nome": MESES_PT[data.month - 1]
        })
    return render(request, "escolher_mes.html", {"meses": meses})


@login_required
def escolher_dia(request, ano, mes):
    dias_no_mes = calendar.monthrange(ano, mes)[1]
    dias = list(range(1, dias_no_mes + 1))
    return render(request, "escolher_dia.html", {"ano": ano, "mes": mes, "dias": dias, "mes_nome": MESES_PT[mes-1]})


@login_required
def escolher_horario(request, ano, mes, dia):
    dt = date(ano, mes, dia)

    # Se for edição, pegar o ID
    editar_id = request.GET.get("editar")
    ag_editando = None

    if editar_id:
        ag_editando = get_object_or_404(Agendamento, id=editar_id, usuario=request.user)

    # montar horários 07:00 - 21:00 com 30min
    horarios = []
    t = datetime.combine(dt, time(7, 0))
    fim = datetime.combine(dt, time(21, 0))
    while t <= fim:
        horarios.append(t.time().strftime("%H:%M"))
        t += timedelta(minutes=30)

    # horários ocupados
    ags = Agendamento.objects.filter(data=dt)
    ocupados = []
    detalhes = {}
    for a in ags:
        hora_str = a.horario.strftime("%H:%M")
        ocupados.append(hora_str)
        perfil = getattr(a.usuario, "profile", None)
        congreg = perfil.congregacao.nome if perfil and perfil.congregacao else ""
        detalhes[hora_str] = {
            "usuario": a.usuario.get_full_name() or a.usuario.username,
            "congregacao": congreg
        }

    # --- PROCESSAR POST ---
    if request.method == "POST":
        horario = request.POST.get("horario")
        if not horario:
            messages.error(request, "Horário inválido.")
            return redirect(request.path + (f"?editar={editar_id}" if editar_id else ""))

        horario_obj = datetime.strptime(horario, "%H:%M").time()

        # --- MODO EDIÇÃO ---
        if ag_editando:
            conflito = Agendamento.objects.filter(data=dt, horario=horario_obj)\
                                          .exclude(id=ag_editando.id).exists()
            if conflito:
                messages.error(request, "Este horário já está ocupado.")
                return redirect(request.path + f"?editar={editar_id}")

            ag_editando.data = dt
            ag_editando.horario = horario_obj
            ag_editando.save()

            messages.success(request, "Agendamento atualizado com sucesso.")
            return redirect("meus_agendamentos")

        # --- MODO CRIAÇÃO ---
        if Agendamento.objects.filter(data=dt, horario=horario_obj).exists():
            messages.error(request, "Horário já ocupado.")
            return redirect(reverse("escolher_horario", args=[ano, mes, dia]))

        Agendamento.objects.create(
            usuario=request.user,
            data=dt,
            horario=horario_obj
        )

        messages.success(request, "Agendamento realizado com sucesso.")
        return redirect("meus_agendamentos")

    # renderizar página
    return render(request, "escolher_horario.html", {
        "data": dt,
        "horarios": horarios,
        "ocupados": ocupados,
        "detalhes": detalhes,
        "mes_nome": MESES_PT[mes-1],
        "ag_editando": ag_editando,
    })

@login_required
def meus_agendamentos(request):
    hoje = date.today()
    ags = Agendamento.objects.filter(usuario=request.user, data__gte=hoje).order_by("data", "horario")
    return render(request, "meus_agendamentos.html", {"agendamentos": ags})


@login_required
def cancelar_agendamento(request, id):
    ag = get_object_or_404(Agendamento, id=id, usuario=request.user)
    if request.method == "POST":
        ag.delete()
        messages.success(request, "Agendamento cancelado.")
        return redirect("meus_agendamentos")
    return render(request, "confirmar_cancelamento.html", {"ag": ag})


@login_required
def editar_agendamento(request, id):
    ag = get_object_or_404(Agendamento, id=id, usuario=request.user)

    # Redireciona para a página de horários já passando info de edição
    return redirect(
        reverse("escolher_horario", args=[ag.data.year, ag.data.month, ag.data.day])
        + f"?editar={ag.id}"
    )
