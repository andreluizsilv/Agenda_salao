from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Congregacao(models.Model):
    nome = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.nome


class UsuarioProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    congregacao = models.ForeignKey(Congregacao, on_delete=models.SET_NULL, null=True, blank=True)
    is_admin_congregacao = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    def __str__(self):
        return f'Nome:{self.user.get_full_name() or self.user.username}, Nome da Congregação:{self.congregacao.nome}'


class Agendamento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="agendamentos")
    congregacao = models.ForeignKey(Congregacao, on_delete=models.CASCADE, null=True, blank=True)

    data = models.DateField()
    horario = models.TimeField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("congregacao", "data", "horario")  # evita choque entre congregações diferentes
        ordering = ["data", "horario"]

    def __str__(self):
        try:
            nome_congregacao = self.usuario.profile.congregacao.nome if self.usuario.profile.congregacao else "Sem Congregação"
        except UsuarioProfile.DoesNotExist:
            nome_congregacao = "Perfil não encontrado"

        return f"Nome:{self.usuario.username}, Congregação:{nome_congregacao}, Data:{self.data}, Horário:{self.horario}"


class BloqueioAgenda(models.Model):
    DIAS_SEMANA = [
        (0, "Segunda-feira"),
        (1, "Terça-feira"),
        (2, "Quarta-feira"),
        (3, "Quinta-feira"),
        (4, "Sexta-feira"),
        (5, "Sábado"),
        (6, "Domingo"),
    ]

    congregacao = models.ForeignKey(
        "Congregacao",
        on_delete=models.CASCADE,
        related_name="bloqueios"
    )

    dia_semana = models.IntegerField(
        choices=DIAS_SEMANA
    )

    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

    motivo = models.CharField(
        max_length=120,
        help_text="Ex: Reunião, Manutenção, Evento especial"
    )

    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"Dia Semana:{self.get_dia_semana_display()}, Horário Inicio:{self.hora_inicio}, Horário Fim:{self.hora_fim}, Motivo:{self.motivo}, Nome da Congregação: {self.congregacao.nome}"
