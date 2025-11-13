#!/usr/bin/env python
"""
E2E Test for Membership Lifecycle (Sprint 2) - DIRECT DATABASE TEST
Sem usar HTTP - testando direto a lógica de negócio

Este teste valida:
1. Ciclo de vida do membership (CONVIDADO → ATIVO → INATIVO → SUSPENSO → ATIVO)
2. Validações de quem pode jogar
3. Transições de estado
4. Timeline (data_entrada, data_saida, data_suspensao)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from datetime import datetime, timedelta
from database import SessionLocal, Base, engine
from models import Event, Player, Membership, Match, MembershipStatus

def print_section(title):
    print(f"\n{'='*70}")
    print(f"{title}")
    print(f"{'='*70}\n")

def print_success(msg):
    print(f"  ✓ {msg}")

def print_error(msg):
    print(f"  ✗ {msg}")

def main():
    print_section("TESTE E2E - MEMBERSHIP LIFECYCLE (DIRECT DATABASE)")
    
    try:
        # Setup database
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        
        # Teste 1: Criar evento
        print("1. Criando evento...")
        event = Event(
            name="Teste Membership E2E",
            date="2025-11-13",
            time="19:00",
            active=True
        )
        db.add(event)
        db.flush()
        event_id = event.id
        print_success(f"Evento criado (ID: {event_id})")
        
        # Teste 2: Criar jogadores
        print("\n2. Criando 3 jogadores...")
        players = []
        for name in ["Ana", "Bruno", "Carlos"]:
            player = Player(
                event_id=event_id,
                name=name,
                elo_rating=1200.0,
                active=True
            )
            db.add(player)
            db.flush()
            players.append(player)
            print_success(f"Jogador criado: {name} (ID: {player.id})")
        
        # Teste 3: Convidar jogadores (criar memberships CONVIDADO)
        print("\n3. Convidando jogadores (status CONVIDADO)...")
        memberships = []
        for player in players:
            membership = Membership(
                event_id=event_id,
                player_id=player.id,
                status=MembershipStatus.CONVIDADO
            )
            db.add(membership)
            db.flush()
            memberships.append(membership)
            print_success(f"Convite enviado para {player.name} (ID: {membership.id}, Status: {membership.status.value})")
        
        # Teste 4: Ana aceita convite
        print("\n4. Ana aceitando convite (CONVIDADO → ATIVO)...")
        membership_ana = memberships[0]
        membership_ana.accept_invite()
        db.commit()
        print_success(f"Ana agora está {membership_ana.status.value} (data_entrada: {membership_ana.data_entrada})")
        assert membership_ana.is_active, "Ana deveria estar ATIVO"
        assert membership_ana.can_play, "Ana deveria poder jogar"
        
        # Teste 5a: Bruno ainda está CONVIDADO - não pode jogar
        print("\n5a. Tentando criar match: Ana (ATIVO) vs Bruno (CONVIDADO)...")
        membership_bruno = memberships[1]
        
        if membership_bruno.is_active:
            print_error("Bruno não deveria estar ATIVO ainda!")
            return False
        else:
            print_success("Corretamente: Bruno não pode jogar (ainda é CONVIDADO)")
        
        # Teste 5b: Bruno também aceita
        print("\n5b. Bruno aceitando convite...")
        membership_bruno.accept_invite()
        db.commit()
        print_success(f"Bruno agora está {membership_bruno.status.value}")
        assert membership_bruno.is_active, "Bruno deveria estar ATIVO"
        
        # Teste 5c: Agora podem jogar juntos
        print("\n5c. Criando match: Ana vs Bruno (ambos ATIVO)...")
        match_ana_bruno = Match(
            event_id=event_id,
            player1_id=players[0].id,
            player2_id=players[1].id,
            player1_games=0,
            player2_games=0,
            games_score="0-0",
            winner_id=players[0].id,
            best_of=5,
            finished=True
        )
        db.add(match_ana_bruno)
        db.commit()
        print_success(f"Match criado com sucesso (ID: {match_ana_bruno.id})")
        
        # Teste 6: Ana sai do evento
        print("\n6. Ana saindo do evento (ATIVO → INATIVO)...")
        membership_ana.leave_group()
        db.commit()
        print_success(f"Ana agora está {membership_ana.status.value} (data_saida: {membership_ana.data_saida})")
        assert not membership_ana.is_active, "Ana não deveria estar ATIVO"
        assert not membership_ana.can_play, "Ana não deveria poder jogar"
        
        # Teste 7: Ana tenta jogar (deveria falhar)
        print("\n7. Tentando criar match: Ana (INATIVO) vs Bruno (ATIVO)...")
        if not membership_ana.can_play:
            print_success("Corretamente: Ana não pode jogar (está INATIVO)")
        else:
            print_error("Ana não deveria poder jogar!")
            return False
        
        # Teste 8: Carlos aceita e depois é suspenso
        print("\n8. Carlos aceitando convite...")
        membership_carlos = memberships[2]
        membership_carlos.accept_invite()
        db.commit()
        print_success(f"Carlos agora está {membership_carlos.status.value}")
        
        print("\n9. Suspendendo Carlos (ATIVO → SUSPENSO)...")
        membership_carlos.suspend_member()
        db.commit()
        print_success(f"Carlos agora está {membership_carlos.status.value} (data_suspensao: {membership_carlos.data_suspensao})")
        assert not membership_carlos.is_active, "Carlos não deveria estar ATIVO"
        assert not membership_carlos.can_play, "Carlos não deveria poder jogar"
        
        # Teste 9: Carlos não pode jogar (SUSPENSO)
        print("\n10. Tentando criar match: Carlos (SUSPENSO) vs Bruno (ATIVO)...")
        if not membership_carlos.can_play:
            print_success("Corretamente: Carlos não pode jogar (está SUSPENSO)")
        else:
            print_error("Carlos não deveria poder jogar!")
            return False
        
        # Teste 10: Carlos é reativado
        print("\n11. Reativando Carlos (SUSPENSO → ATIVO)...")
        membership_carlos.reactivate()
        db.commit()
        print_success(f"Carlos agora está {membership_carlos.status.value}")
        assert membership_carlos.is_active, "Carlos deveria estar ATIVO"
        assert membership_carlos.can_play, "Carlos deveria poder jogar"
        
        # Teste 11: Carlos agora consegue jogar
        print("\n12. Criando match: Carlos (ATIVO) vs Bruno (ATIVO)...")
        match_carlos_bruno = Match(
            event_id=event_id,
            player1_id=players[2].id,
            player2_id=players[1].id,
            player1_games=0,
            player2_games=0,
            games_score="0-0",
            winner_id=players[2].id,
            best_of=5,
            finished=True
        )
        db.add(match_carlos_bruno)
        db.commit()
        print_success(f"Match criado com sucesso (ID: {match_carlos_bruno.id})")
        
        # Teste 12: Validar timeline de Ana
        print("\n13. Validando timeline de Ana...")
        assert membership_ana.data_entrada is not None, "data_entrada deveria ser preenchida"
        assert membership_ana.data_saida is not None, "data_saida deveria ser preenchida"
        assert membership_ana.data_suspensao is None, "data_suspensao não deveria ser preenchida"
        assert membership_ana.data_saida > membership_ana.data_entrada, "data_saida deveria ser depois de data_entrada"
        print_success("Timeline de Ana validada corretamente")
        
        # Teste 13: Validar timeline de Carlos
        print("\n14. Validando timeline de Carlos...")
        assert membership_carlos.data_entrada is not None, "data_entrada deveria ser preenchida"
        # Nota: data_suspensao foi removida quando reativado
        assert membership_carlos.data_saida is None, "data_saida não deveria ser preenchida"
        assert membership_carlos.is_active, "Carlos deveria estar ATIVO"
        print_success("Timeline de Carlos validada corretamente")
        
        # Teste 14: Listar membros
        print("\n15. Listando membros do evento...")
        all_memberships = db.query(Membership).filter(Membership.event_id == event_id).all()
        statuses = {}
        for m in all_memberships:
            status = m.status.value
            statuses[status] = statuses.get(status, 0) + 1
            can_play = "✓" if m.can_play else "✗"
            print(f"    {can_play} {m.player.name}: {status}")
        
        print_success(f"Total membros: {len(all_memberships)}")
        print_success(f"ATIVO: {statuses.get('ativo', 0)}, INATIVO: {statuses.get('inativo', 0)}, SUSPENSO: {statuses.get('suspenso', 0)}")
        
        # Validações finais
        assert statuses.get('ativo', 0) == 2, f"Deveria haver 2 ATIVO, got {statuses.get('ativo', 0)}"
        assert statuses.get('inativo', 0) == 1, f"Deveria haver 1 INATIVO, got {statuses.get('inativo', 0)}"
        assert statuses.get('suspenso', 0) == 0, f"Deveria haver 0 SUSPENSO, got {statuses.get('suspenso', 0)}"
        
        print_section("✓ TODOS OS TESTES PASSARAM COM SUCESSO!")
        print(f"Resumo:")
        print(f"  Evento ID: {event_id}")
        print(f"  Jogadores: {len(players)}")
        print(f"  Membros: {len(all_memberships)}")
        print(f"  Partidas criadas: 2")
        print(f"  Transições validadas: 6 (accept, leave, suspend, reactivate, etc.)")
        print(f"  Validações: Todas passando")
        
        db.close()
        return True
        
    except Exception as e:
        print_section("✗ TESTE FALHOU")
        print_error(f"{type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
