from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("cadastro/", views.cadastro, name="cadastro"),
    path("agendar/", views.escolher_mes, name="escolher_mes"),
    path("agendar/<int:ano>/<int:mes>/", views.escolher_dia, name="escolher_dia"),
    path("agendar/<int:ano>/<int:mes>/<int:dia>/", views.escolher_horario, name="escolher_horario"),
    path("meus-agendamentos/", views.meus_agendamentos, name="meus_agendamentos"),
    path("agendamento/cancelar/<int:id>/", views.cancelar_agendamento, name="cancelar_agendamento"),
    path("agendamento/editar/<int:id>/", views.editar_agendamento, name="editar_agendamento"),
]
