"""
Unit Tests for Membership Model - Sprint 2

Testes:
  1. Criar membership com status CONVIDADO
  2. Transição CONVIDADO -> ATIVO (accept_invite)
  3. Transição ATIVO -> INATIVO (leave_group)
  4. Transição ATIVO -> SUSPENSO (suspend_member)
  5. Transição SUSPENSO -> ATIVO (reactivate)
  6. Propriedades is_active e can_play
  7. Transições inválidas levantam erro
  8. Preservação de timeline (data_entrada, data_saida, etc)
"""

import unittest
from datetime import datetime, timedelta
from models.membership import Membership, MembershipStatus


class TestMembershipModel(unittest.TestCase):
    """Testes para o modelo Membership"""

    def setUp(self):
        """Setup antes de cada teste"""
        self.membership = Membership(
            id=1,
            event_id=1,
            player_id=1,
            status=MembershipStatus.CONVIDADO
        )

    def test_membership_initial_state(self):
        """Teste 1: Membership criado com status CONVIDADO"""
        self.assertEqual(self.membership.status, MembershipStatus.CONVIDADO)
        self.assertIsNone(self.membership.data_entrada)
        self.assertIsNone(self.membership.data_saida)
        self.assertIsNone(self.membership.data_suspensao)
        self.assertFalse(self.membership.is_active)
        self.assertFalse(self.membership.can_play)

    def test_accept_invite_transition(self):
        """Teste 2: Transição CONVIDADO -> ATIVO"""
        # Estado inicial
        self.assertEqual(self.membership.status, MembershipStatus.CONVIDADO)
        self.assertIsNone(self.membership.data_entrada)

        # Aceitar convite
        self.membership.accept_invite()

        # Verificar transição
        self.assertEqual(self.membership.status, MembershipStatus.ATIVO)
        self.assertIsNotNone(self.membership.data_entrada)
        self.assertTrue(self.membership.is_active)
        self.assertTrue(self.membership.can_play)

    def test_leave_group_transition(self):
        """Teste 3: Transição ATIVO -> INATIVO"""
        # Preparar: colocar em estado ATIVO
        self.membership.accept_invite()
        self.assertEqual(self.membership.status, MembershipStatus.ATIVO)
        self.assertIsNone(self.membership.data_saida)

        # Sair
        self.membership.leave_group()

        # Verificar transição
        self.assertEqual(self.membership.status, MembershipStatus.INATIVO)
        self.assertIsNotNone(self.membership.data_saida)
        self.assertFalse(self.membership.is_active)
        self.assertFalse(self.membership.can_play)

    def test_suspend_member_transition(self):
        """Teste 4: Transição ATIVO -> SUSPENSO"""
        # Preparar: colocar em estado ATIVO
        self.membership.accept_invite()
        self.assertEqual(self.membership.status, MembershipStatus.ATIVO)

        # Suspender
        motivo = "Violação de regras"
        self.membership.suspend_member(motivo)

        # Verificar transição
        self.assertEqual(self.membership.status, MembershipStatus.SUSPENSO)
        self.assertIsNotNone(self.membership.data_suspensao)
        self.assertEqual(self.membership.motivo_suspensao, motivo)
        self.assertFalse(self.membership.is_active)
        self.assertFalse(self.membership.can_play)

    def test_reactivate_member_transition(self):
        """Teste 5: Transição SUSPENSO -> ATIVO"""
        # Preparar: CONVIDADO -> ATIVO -> SUSPENSO
        self.membership.accept_invite()
        self.membership.suspend_member("Inatividade")
        self.assertEqual(self.membership.status, MembershipStatus.SUSPENSO)
        self.assertIsNotNone(self.membership.motivo_suspensao)

        # Reativar
        self.membership.reactivate()

        # Verificar transição
        self.assertEqual(self.membership.status, MembershipStatus.ATIVO)
        self.assertIsNone(self.membership.data_suspensao)
        self.assertIsNone(self.membership.motivo_suspensao)
        self.assertTrue(self.membership.is_active)
        self.assertTrue(self.membership.can_play)

    def test_is_active_property(self):
        """Teste 6a: Propriedade is_active"""
        # CONVIDADO não é ativo
        self.membership.status = MembershipStatus.CONVIDADO
        self.assertFalse(self.membership.is_active)

        # ATIVO é ativo
        self.membership.status = MembershipStatus.ATIVO
        self.assertTrue(self.membership.is_active)

        # INATIVO não é ativo
        self.membership.status = MembershipStatus.INATIVO
        self.assertFalse(self.membership.is_active)

        # SUSPENSO não é ativo
        self.membership.status = MembershipStatus.SUSPENSO
        self.assertFalse(self.membership.is_active)

        # DELETADO não é ativo
        self.membership.status = MembershipStatus.DELETADO
        self.assertFalse(self.membership.is_active)

    def test_can_play_property(self):
        """Teste 6b: Propriedade can_play (deve ser igual a is_active)"""
        test_cases = [
            (MembershipStatus.CONVIDADO, False),
            (MembershipStatus.ATIVO, True),
            (MembershipStatus.INATIVO, False),
            (MembershipStatus.SUSPENSO, False),
            (MembershipStatus.DELETADO, False),
        ]
        
        for status, expected_can_play in test_cases:
            self.membership.status = status
            self.assertEqual(
                self.membership.can_play, 
                expected_can_play,
                f"Status {status} deveria ter can_play={expected_can_play}"
            )

    def test_invalid_transition_from_convidado_to_inactive(self):
        """Teste 7a: Transição inválida CONVIDADO -> INATIVO"""
        self.membership.status = MembershipStatus.CONVIDADO
        with self.assertRaises(ValueError):
            self.membership.leave_group()

    def test_invalid_transition_from_convidado_to_ativo(self):
        """Teste 7b: accept_invite só funciona de CONVIDADO"""
        self.membership.status = MembershipStatus.ATIVO
        with self.assertRaises(ValueError):
            self.membership.accept_invite()

    def test_invalid_transition_from_inativo_to_ativo(self):
        """Teste 7c: Não pode reativar de INATIVO"""
        self.membership.status = MembershipStatus.INATIVO
        with self.assertRaises(ValueError):
            self.membership.reactivate()

    def test_timeline_preservation(self):
        """Teste 8: Timeline é preservada corretamente"""
        # Inicial
        self.assertIsNone(self.membership.data_entrada)
        self.assertIsNone(self.membership.data_saida)
        self.assertIsNone(self.membership.data_suspensao)

        # Aceitar
        entrada_antes = datetime.utcnow()
        self.membership.accept_invite()
        entrada_depois = datetime.utcnow()
        
        self.assertIsNotNone(self.membership.data_entrada)
        self.assertGreaterEqual(self.membership.data_entrada, entrada_antes)
        self.assertLessEqual(self.membership.data_entrada, entrada_depois)
        self.assertIsNone(self.membership.data_saida)
        self.assertIsNone(self.membership.data_suspensao)

        # Suspender
        saida_original = self.membership.data_saida
        suspensao_antes = datetime.utcnow()
        self.membership.suspend_member("Teste")
        suspensao_depois = datetime.utcnow()
        
        self.assertIsNotNone(self.membership.data_entrada)  # Mantém data_entrada
        self.assertEqual(self.membership.data_saida, saida_original)  # data_saida não muda
        self.assertIsNotNone(self.membership.data_suspensao)
        self.assertGreaterEqual(self.membership.data_suspensao, suspensao_antes)
        self.assertLessEqual(self.membership.data_suspensao, suspensao_depois)

    def test_soft_delete(self):
        """Teste adicional: soft_delete marca como DELETADO"""
        self.membership.accept_invite()
        self.assertEqual(self.membership.status, MembershipStatus.ATIVO)
        
        self.membership.soft_delete()
        
        self.assertEqual(self.membership.status, MembershipStatus.DELETADO)
        self.assertFalse(self.membership.is_active)
        self.assertFalse(self.membership.can_play)

    def test_membership_repr(self):
        """Teste adicional: __repr__ funciona"""
        repr_str = repr(self.membership)
        self.assertIn("Membership", repr_str)
        self.assertIn("event_id", repr_str)


class TestMembershipStatuses(unittest.TestCase):
    """Testes para MembershipStatus enum"""

    def test_all_statuses_exist(self):
        """Verificar que todos os 5 status existem"""
        expected = {"convidado", "ativo", "inativo", "suspenso", "deletado"}
        actual = {status.value for status in MembershipStatus}
        self.assertEqual(expected, actual)

    def test_status_values_are_strings(self):
        """Status são strings (para JSON serialization)"""
        for status in MembershipStatus:
            self.assertIsInstance(status.value, str)


if __name__ == "__main__":
    unittest.main()
