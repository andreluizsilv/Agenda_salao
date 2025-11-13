from django.urls import path
from agendamento import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('cadastro-congregacao/', views.cadastrar_congregacao, name='cadastrar_congregacao'),
]

