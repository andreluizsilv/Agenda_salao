from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Congregacao(models.Model):
    nome = models.CharField(max_length=150, unique=True)
    responsavel = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.nome


class UsuarioProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    congregacao = models.ForeignKey(Congregacao, on_delete=models.SET_NULL, null=True, blank=True)
    is_admin_congregacao = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Agendamento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="agendamentos")
    data = models.DateField()
    horario = models.TimeField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("data", "horario")  # evita duplicidade (salão compartilhado)
        ordering = ["data", "horario"]

    def __str__(self):
        return f"{self.data} {self.horario} - {self.usuario.username}"
