from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import date, time, timedelta
from django.utils import timezone
from django.db import transaction  # Adicionar esta importação

# Importações absolutas
from agendamento.models import Congregacao, UsuarioProfile, Agendamento, BloqueioAgenda

User = get_user_model()


class ModelTests(TestCase):
    def setUp(self):
        self.congregacao = Congregacao.objects.create(nome="Congregação Central")

        # Criar usuários
        self.user1 = User.objects.create_user(
            username="usuario1",
            password="senha123",
            first_name="João",
            last_name="Silva"
        )
        self.profile1 = UsuarioProfile.objects.create(
            user=self.user1,
            congregacao=self.congregacao
        )

        # Criar admin
        self.admin = User.objects.create_user(
            username="admin",
            password="admin123"
        )
        self.admin_profile = UsuarioProfile.objects.create(
            user=self.admin,
            congregacao=self.congregacao,
            is_admin_congregacao=True
        )

    def test_congregacao_creation(self):
        """Testa criação de congregação"""
        self.assertEqual(str(self.congregacao), "Congregação Central")
        self.assertEqual(Congregacao.objects.count(), 1)

    def test_usuario_profile_creation(self):
        """Testa criação de perfil de usuário"""
        self.assertEqual(self.profile1.congregacao.nome, "Congregação Central")
        self.assertFalse(self.profile1.is_admin_congregacao)
        self.assertFalse(self.profile1.is_superadmin)

    def test_agendamento_creation(self):
        """Testa criação de agendamento"""
        agendamento = Agendamento.objects.create(
            usuario=self.user1,
            congregacao=self.congregacao,
            data=date.today(),
            horario=time(10, 0)
        )
        self.assertIn("usuario1", str(agendamento))
        self.assertEqual(Agendamento.objects.count(), 1)

    def test_bloqueio_agenda_creation(self):
        """Testa criação de bloqueio de agenda"""
        bloqueio = BloqueioAgenda.objects.create(
            congregacao=self.congregacao,
            dia_semana=2,  # Quarta-feira
            hora_inicio=time(19, 0),
            hora_fim=time(21, 0),
            motivo="Reunião de Meio de Semana"
        )
        self.assertTrue(bloqueio.ativo)
        self.assertEqual(bloqueio.get_dia_semana_display(), "Quarta-feira")

    def test_agendamento_uniqueness(self):
        """Testa que não pode haver dois agendamentos no mesmo horário para mesma congregação"""
        # Cria primeiro agendamento
        Agendamento.objects.create(
            usuario=self.user1,
            congregacao=self.congregacao,
            data=date.today(),
            horario=time(14, 0)
        )

        # CORREÇÃO: Usar transaction.atomic para testar a exceção
        with transaction.atomic():
            try:
                # Tenta criar segundo agendamento no mesmo horário
                Agendamento.objects.create(
                    usuario=self.admin,
                    congregacao=self.congregacao,
                    data=date.today(),
                    horario=time(14, 0)
                )
                # Se chegou aqui, algo está errado
                self.fail("Deveria ter levantado IntegrityError")
            except Exception as e:
                # Verifica que é um IntegrityError
                self.assertIn('UNIQUE constraint failed', str(e))

        # Verifica que temos exatamente 1 agendamento
        # CORREÇÃO: Forçar um refresh da conexão
        from django.db import connection
        connection.close()

        self.assertEqual(Agendamento.objects.count(), 1)

        # Testa que agendamentos em congregações diferentes são permitidos
        congregacao2 = Congregacao.objects.create(nome="Outra Congregação")
        Agendamento.objects.create(
            usuario=self.admin,
            congregacao=congregacao2,
            data=date.today(),
            horario=time(14, 0)
        )

        # Agora devem ter 2 agendamentos (congregações diferentes)
        self.assertEqual(Agendamento.objects.count(), 2)

    # Versão alternativa mais simples do teste
    def test_agendamento_uniqueness_simple(self):
        """Versão simplificada do teste de unicidade"""
        # Cria primeiro agendamento
        Agendamento.objects.create(
            usuario=self.user1,
            congregacao=self.congregacao,
            data=date.today(),
            horario=time(14, 0)
        )

        # Tenta criar duplicado - deve levantar exceção
        with self.assertRaises(Exception) as context:
            with transaction.atomic():
                Agendamento.objects.create(
                    usuario=self.admin,
                    congregacao=self.congregacao,
                    data=date.today(),
                    horario=time(14, 0)
                )

        # Verifica a mensagem de erro
        error_msg = str(context.exception)
        self.assertIn('UNIQUE', error_msg or '')

        # Verifica contagem
        self.assertEqual(Agendamento.objects.count(), 1)

# ... (o resto do código permanece igual) ...