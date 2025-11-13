#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados de teste
para validar o novo sistema de membership
"""

from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Event, Player, Membership, MembershipStatus

def create_test_data():
    db = SessionLocal()
    
    try:
        # Criar evento de teste
        print("[INFO] Criando evento de teste...")
        event = Event(
            name="Copa do Clube - Teste",
            date="2025-11-13",
            time="19:00",
            active=True
        )
        db.add(event)
        db.flush()
        print(f"[OK] Evento criado: ID {event.id}")
        
        # Criar jogadores
        print("[INFO] Criando jogadores...")
        players = []
        for i in range(1, 5):
            player = Player(
                name=f"Jogador {i}",
                event_id=event.id,
                elo_rating=1500,
                score=0,
                active=True
            )
            db.add(player)
            db.flush()
            players.append(player)
            print(f"[OK] Jogador criado: ID {player.id}, Name {player.name}")
        
        # Criar memberships ATIVO para cada jogador
        print("[INFO] Criando memberships...")
        for player in players:
            membership = Membership(
                event_id=event.id,
                player_id=player.id,
                status=MembershipStatus.CONVIDADO  # Comeca como CONVIDADO
            )
            membership.accept_invite()  # Transiciona para ATIVO
            db.add(membership)
            print(f"[OK] Membership criado: Player {player.id} → Event {event.id} [ATIVO]")
        
        db.commit()
        
        print("\n[SUCCESS] Dados de teste criados com sucesso!")
        print(f"[INFO] Evento: {event.name} (ID {event.id})")
        print(f"[INFO] Jogadores: {len(players)}")
        print(f"[INFO] Agora você pode criar partidas entre esses jogadores")
        
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Erro ao criar dados: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()
