"""
E2E Tests for Membership Lifecycle - Sprint 2

Cenários:
  1. Criar evento e jogadores
  2. Convidar jogador (membership com status CONVIDADO)
  3. Aceitar convite (transição CONVIDADO -> ATIVO)
  4. Jogar match com membro ATIVO (deve funcionar)
  5. Sair do evento (transição ATIVO -> INATIVO)
  6. Tentar jogar after leaving (deve falhar com status 403)
  7. Suspender membro (transição -> SUSPENSO)
  8. Tentar jogar when suspended (deve falhar com status 403)
  9. Reativar membro suspenso (transição SUSPENSO -> ATIVO)
  10. Jogar novamente após reativação (deve funcionar)
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def print_section(title):
    """Imprimir seção formatada"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def print_test(number, title, result):
    """Imprimir resultado de teste"""
    symbol = "✓" if result else "✗"
    print(f"  {symbol} {number}. {title}")

def test_membership_lifecycle():
    """Teste E2E completo do ciclo de vida de membership"""
    
    print_section("TESTE E2E - MEMBERSHIP LIFECYCLE SPRINT 2")
    
    all_passed = True
    
    try:
        # ========== 1. Criar evento e jogadores ==========
        print("1. Criando evento e jogadores...")
        
        event_data = {
            "name": "Copa Membership Test",
            "date": "2025-11-13",
            "time": "15:00"
        }
        event_response = requests.post(f"{BASE_URL}/events", json=event_data)
        assert event_response.status_code == 200, f"Falha ao criar evento: {event_response.text}"
        event = event_response.json()
        event_id = event['id']
        print(f"  ✓ Evento criado: {event['name']} (ID: {event_id})")
        
        # Criar dois jogadores
        player_data_1 = {
            "name": "Alice",
            "event_id": event_id
        }
        player_response_1 = requests.post(f"{BASE_URL}/players", json=player_data_1)
        assert player_response_1.status_code == 200
        alice = player_response_1.json()
        alice_id = alice['id']
        print(f"  ✓ Jogador criado: Alice (ID: {alice_id})")
        
        player_data_2 = {
            "name": "Bob",
            "event_id": event_id
        }
        player_response_2 = requests.post(f"{BASE_URL}/players", json=player_data_2)
        assert player_response_2.status_code == 200
        bob = player_response_2.json()
        bob_id = bob['id']
        print(f"  ✓ Jogador criado: Bob (ID: {bob_id})")
        
        # ========== 2. Convidar Alice (membership CONVIDADO) ==========
        print("\n2. Convidando Alice para o evento (membership CONVIDADO)...")
        
        invite_data = {
            "event_id": event_id,
            "player_id": alice_id
        }
        invite_response = requests.post(f"{BASE_URL}/members", json=invite_data)
        assert invite_response.status_code == 200, f"Falha ao convidar: {invite_response.text}"
        membership = invite_response.json()
        membership_id = membership['id']
        assert membership['status'] == 'convidado', f"Status incorreto: {membership['status']}"
        assert membership['data_entrada'] is None, "data_entrada não deve ser preenchida antes de aceitar"
        print(f"  ✓ Alice convidada (membership ID: {membership_id}, status: convidado)")
        
        # ========== 3. Convidar Bob também (membership CONVIDADO) ==========
        print("\n3. Convidando Bob para o evento...")
        
        invite_data_bob = {
            "event_id": event_id,
            "player_id": bob_id
        }
        invite_response_bob = requests.post(f"{BASE_URL}/members", json=invite_data_bob)
        assert invite_response_bob.status_code == 200
        membership_bob = invite_response_bob.json()
        membership_bob_id = membership_bob['id']
        assert membership_bob['status'] == 'convidado'
        print(f"  ✓ Bob convidado (membership ID: {membership_bob_id}, status: convidado)")
        
        # ========== 4. Alice aceita convite (CONVIDADO -> ATIVO) ==========
        print("\n4. Alice aceitando convite (CONVIDADO -> ATIVO)...")
        
        accept_response = requests.put(f"{BASE_URL}/members/{membership_id}/accept")
        assert accept_response.status_code == 200, f"Falha ao aceitar: {accept_response.text}"
        membership_updated = accept_response.json()
        assert membership_updated['status'] == 'ativo', f"Status deve ser 'ativo', got {membership_updated['status']}"
        assert membership_updated['data_entrada'] is not None, "data_entrada deve ser preenchida"
        print(f"  ✓ Alice aceitou convite (status: ativo, data_entrada: {membership_updated['data_entrada']})")
        
        # ========== 5. Bob aceita convite também ==========
        print("\n5. Bob aceitando convite...")
        
        accept_response_bob = requests.put(f"{BASE_URL}/members/{membership_bob_id}/accept")
        assert accept_response_bob.status_code == 200
        membership_bob_updated = accept_response_bob.json()
        assert membership_bob_updated['status'] == 'ativo'
        print(f"  ✓ Bob aceitou convite (status: ativo)")
        
        # ========== 6. Jogar match com membros ATIVO (deve funcionar) ==========
        print("\n6. Criando match entre Alice (ATIVO) e Bob (ATIVO)...")
        
        match_data = {
            "event_id": event_id,
            "player1_id": alice_id,
            "player2_id": bob_id,
            "winner_id": alice_id,
            "player1_games": 3,
            "player2_games": 0,
            "games_score": "11-9,11-8,11-7",
            "best_of": 5
        }
        match_response = requests.post(f"{BASE_URL}/matches", json=match_data)
        assert match_response.status_code == 201, f"Falha ao criar match: {match_response.text}"
        match = match_response.json()
        match_id = match['id']
        assert match['winner_id'] == alice_id
        print(f"  ✓ Match criado com sucesso (ID: {match_id}, winner: Alice)")
        print(f"    Alice e Bob puderam jogar porque ambos têm status ATIVO")
        
        # ========== 7. Alice sai do evento (ATIVO -> INATIVO) ==========
        print("\n7. Alice saindo do evento (ATIVO -> INATIVO)...")
        
        leave_response = requests.put(f"{BASE_URL}/members/{membership_id}/leave")
        assert leave_response.status_code == 200, f"Falha ao sair: {leave_response.text}"
        membership_left = leave_response.json()
        assert membership_left['status'] == 'inativo', f"Status deve ser 'inativo', got {membership_left['status']}"
        assert membership_left['data_saida'] is not None, "data_saida deve ser preenchida"
        print(f"  ✓ Alice saiu (status: inativo, data_saida: {membership_left['data_saida']})")
        
        # ========== 8. Tentar criar match com Alice (INATIVO) - deve falhar ==========
        print("\n8. Tentando criar match com Alice (INATIVO) - deve falhar com 403...")
        
        match_data_fail_1 = {
            "event_id": event_id,
            "player1_id": alice_id,
            "player2_id": bob_id,
            "winner_id": bob_id,
            "best_of": 5
        }
        match_fail_response_1 = requests.post(f"{BASE_URL}/matches", json=match_data_fail_1)
        assert match_fail_response_1.status_code == 403, \
            f"Deve retornar 403, mas retornou {match_fail_response_1.status_code}: {match_fail_response_1.text}"
        error = match_fail_response_1.json()
        assert "não pode jogar" in error['detail'].lower(), f"Mensagem de erro: {error['detail']}"
        print(f"  ✓ Match rejeitado com status 403 - Alice não pode jogar (status: inativo)")
        print(f"    Mensagem: {error['detail']}")
        
        # ========== 9. Suspender Bob (-> SUSPENSO) ==========
        print("\n9. Suspendendo Bob por violação de regras...")
        
        suspend_data = {
            "motivo_suspensao": "Violação de regras de conduta"
        }
        suspend_response = requests.put(
            f"{BASE_URL}/members/{membership_bob_id}/suspend",
            json=suspend_data
        )
        assert suspend_response.status_code == 200, f"Falha ao suspender: {suspend_response.text}"
        membership_suspended = suspend_response.json()
        assert membership_suspended['status'] == 'suspenso', f"Status deve ser 'suspenso', got {membership_suspended['status']}"
        assert membership_suspended['data_suspensao'] is not None
        assert membership_suspended['motivo_suspensao'] == "Violação de regras de conduta"
        print(f"  ✓ Bob suspenso (status: suspenso, motivo: {membership_suspended['motivo_suspensao']})")
        
        # ========== 10. Tentar criar match com Bob (SUSPENSO) - deve falhar ==========
        print("\n10. Tentando criar match com Bob (SUSPENSO) - deve falhar com 403...")
        
        # Criar terceiro jogador ATIVO para jogar com Bob
        player_data_3 = {
            "name": "Charlie",
            "event_id": event_id
        }
        player_response_3 = requests.post(f"{BASE_URL}/players", json=player_data_3)
        assert player_response_3.status_code == 200
        charlie = player_response_3.json()
        charlie_id = charlie['id']
        
        # Convidar e aceitar para Charlie
        invite_data_charlie = {
            "event_id": event_id,
            "player_id": charlie_id
        }
        invite_response_charlie = requests.post(f"{BASE_URL}/members", json=invite_data_charlie)
        assert invite_response_charlie.status_code == 200
        membership_charlie = invite_response_charlie.json()
        membership_charlie_id = membership_charlie['id']
        
        accept_response_charlie = requests.put(f"{BASE_URL}/members/{membership_charlie_id}/accept")
        assert accept_response_charlie.status_code == 200
        
        # Tentar criar match com Bob (SUSPENSO)
        match_data_fail_2 = {
            "event_id": event_id,
            "player1_id": bob_id,
            "player2_id": charlie_id,
            "winner_id": charlie_id,
            "best_of": 5
        }
        match_fail_response_2 = requests.post(f"{BASE_URL}/matches", json=match_data_fail_2)
        assert match_fail_response_2.status_code == 403, \
            f"Deve retornar 403, mas retornou {match_fail_response_2.status_code}"
        error = match_fail_response_2.json()
        assert "não pode jogar" in error['detail'].lower()
        print(f"  ✓ Match rejeitado com status 403 - Bob não pode jogar (status: suspenso)")
        print(f"    Mensagem: {error['detail']}")
        
        # ========== 11. Reativar Bob (SUSPENSO -> ATIVO) ==========
        print("\n11. Reativando Bob...")
        
        reactivate_response = requests.put(f"{BASE_URL}/members/{membership_bob_id}/reactivate")
        assert reactivate_response.status_code == 200, f"Falha ao reativar: {reactivate_response.text}"
        membership_reactivated = reactivate_response.json()
        assert membership_reactivated['status'] == 'ativo', f"Status deve ser 'ativo', got {membership_reactivated['status']}"
        assert membership_reactivated['data_suspensao'] is None, "data_suspensao deve ser limpa"
        assert membership_reactivated['motivo_suspensao'] is None, "motivo_suspensao deve ser limpo"
        print(f"  ✓ Bob reativado (status: ativo)")
        
        # ========== 12. Jogar match com Bob (agora ATIVO) - deve funcionar ==========
        print("\n12. Criando match com Bob (agora ATIVO) - deve funcionar...")
        
        match_data_success = {
            "event_id": event_id,
            "player1_id": bob_id,
            "player2_id": charlie_id,
            "winner_id": bob_id,
            "player1_games": 3,
            "player2_games": 1,
            "games_score": "11-9,10-12,11-8,11-7",
            "best_of": 5
        }
        match_response_success = requests.post(f"{BASE_URL}/matches", json=match_data_success)
        assert match_response_success.status_code == 201, f"Falha ao criar match: {match_response_success.text}"
        match_success = match_response_success.json()
        print(f"  ✓ Match criado com sucesso - Bob pode jogar novamente (status: ativo)")
        
        # ========== 13. Listar membros do evento ==========
        print("\n13. Listando todos os membros do evento...")
        
        members_response = requests.get(f"{BASE_URL}/members/{event_id}")
        assert members_response.status_code == 200
        members = members_response.json()
        assert len(members) == 3  # Alice (inativo), Bob (ativo), Charlie (ativo)
        
        # Contar por status
        statuses = {m['status']: 0 for m in members}
        for m in members:
            statuses[m['status']] += 1
        
        print(f"  ✓ Total de membros: {len(members)}")
        for status, count in statuses.items():
            print(f"    - {status}: {count}")
        
        assert statuses.get('ativo', 0) == 2, f"Deve haver 2 ativos, got {statuses.get('ativo', 0)}"
        assert statuses.get('inativo', 0) == 1, f"Deve haver 1 inativo, got {statuses.get('inativo', 0)}"
        
        # ========== 14. Filtrar por status ==========
        print("\n14. Filtrando membros por status...")
        
        active_response = requests.get(f"{BASE_URL}/members/{event_id}?status=ativo")
        assert active_response.status_code == 200
        active_members = active_response.json()
        assert len(active_members) == 2, f"Deve haver 2 ativos, got {len(active_members)}"
        print(f"  ✓ Membros ATIVO: {len(active_members)}")
        
        inactive_response = requests.get(f"{BASE_URL}/members/{event_id}?status=inativo")
        assert inactive_response.status_code == 200
        inactive_members = inactive_response.json()
        assert len(inactive_members) == 1, f"Deve haver 1 inativo, got {len(inactive_members)}"
        print(f"  ✓ Membros INATIVO: {len(inactive_members)}")
        
        print_test("✓", "TODOS OS TESTES PASSARAM!", True)
        
    except AssertionError as e:
        print(f"\n  ✗ ERRO: {str(e)}")
        all_passed = False
    except Exception as e:
        print(f"\n  ✗ ERRO INESPERADO: {str(e)}")
        all_passed = False
    
    print_section("RESULTADO FINAL" if all_passed else "FALHA")
    return all_passed


if __name__ == "__main__":
    success = test_membership_lifecycle()
    exit(0 if success else 1)
