from django.db import models
from django.contrib.auth.models import User


class Congregacao(models.Model):
    nome = models.CharField(max_length=150, unique=True)
    responsavel = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Congregação"
        verbose_name_plural = "Congregações"

    def __str__(self):
        return self.nome


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    congregacao = models.ForeignKey(Congregacao, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.user.get_full_name() or self.user.username
