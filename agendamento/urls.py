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

    path("admin-congregacao/usuarios/", views.gerenciar_usuarios_congregacao, name="gerenciar_usuarios"),
    path("admin-congregacao/bloqueios/criar", views.criar_bloqueio, name="criar_bloqueio"),
    path("admin-congregacao/bloqueios/", views.listar_bloqueios, name="listar_bloqueios"),
    path("admin-congregacao/bloqueios/editar/<int:id>/", views.editar_bloqueio, name="editar_bloqueio"),
    path("admin-congregacao/bloqueios/excluir/<int:id>/", views.excluir_bloqueio, name="excluir_bloqueio"),

    path("superadmin/bloqueios/", views.listar_todos_bloqueios, name="superadmin_bloqueios"),
    path("superadmin/bloqueios/editar/<int:id>/", views.superadmin_editar_bloqueio, name="superadmin_editar_bloqueio"),
    path("superadmin/bloqueios/excluir/<int:id>/", views.superadmin_excluir_bloqueio, name="superadmin_excluir_bloqueio"),

]
