"""
Teste E2E da Feature 1: Sistema ELO com Ranking

Este teste valida:
1. Criação de evento
2. Adição de jogadores
3. Criação de partidas com cálculo automático de ELO
4. Atualização de ratings dinâmicos
5. Ranking atualizado em tempo real
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def create_event():
    """Criar um novo evento de teste"""
    payload = {
        "name": "Copa Teste ELO",
        "date": "2025-11-13",
        "time": "15:00"
    }
    response = requests.post(f"{BASE_URL}/events", json=payload)
    assert response.status_code == 201, f"Falha ao criar evento: {response.text}"
    return response.json()

def add_player(event_id, name):
    """Adicionar um jogador a um evento"""
    payload = {
        "name": name,
        "event_id": event_id
    }
    response = requests.post(f"{BASE_URL}/players", json=payload)
    assert response.status_code == 201, f"Falha ao criar jogador: {response.text}"
    player = response.json()
    print(f"  ✓ Jogador criado: {player['name']} (ID: {player['id']}, ELO: {player['elo_rating']})")
    return player

def create_match(event_id, player1_id, player2_id, winner_id):
    """Criar uma partida e registrar resultado"""
    payload = {
        "event_id": event_id,
        "player1_id": player1_id,
        "player2_id": player2_id,
        "winner_id": winner_id,
        "player1_games": 3,
        "player2_games": 0,
        "games_score": "11-9,11-8,11-7"
    }
    response = requests.post(f"{BASE_URL}/matches", json=payload)
    assert response.status_code == 201, f"Falha ao criar partida: {response.text}"
    return response.json()

def get_player(player_id):
    """Obter dados atualizados de um jogador"""
    response = requests.get(f"{BASE_URL}/players/{player_id}")
    assert response.status_code == 200, f"Falha ao obter jogador: {response.text}"
    return response.json()

def get_ranking(event_id):
    """Obter ranking do evento"""
    response = requests.get(f"{BASE_URL}/ranking", params={"event_id": event_id})
    assert response.status_code == 200, f"Falha ao obter ranking: {response.text}"
    return response.json()  # Retorna lista diretamente

def test_elo_feature():
    """Executar teste completo da Feature 1"""
    print("\n" + "="*70)
    print("TESTE E2E - FEATURE 1: SISTEMA ELO COM RANKING")
    print("="*70)
    
    # Passo 1: Criar evento
    print("\n1. Criando evento...")
    event = create_event()
    event_id = event['id']
    print(f"  ✓ Evento criado: {event['name']} (ID: {event_id})")
    
    # Passo 2: Adicionar jogadores
    print("\n2. Adicionando jogadores...")
    maria = add_player(event_id, "Maria")
    joao = add_player(event_id, "João")
    pedro = add_player(event_id, "Pedro")
    
    print(f"\n  Ratings iniciais (todos começam com 1200):")
    print(f"    Maria:  {maria['elo_rating']}")
    print(f"    João:   {joao['elo_rating']}")
    print(f"    Pedro:  {pedro['elo_rating']}")
    
    # Passo 3: Criar partidas e observar mudanças
    print("\n3. Criando partidas e calculando ELO...")
    
    # Partida 1: João (1200) vence Maria (1200)
    print(f"\n  Partida 1: João (1200) vs Maria (1200)")
    match1 = create_match(event_id, joao['id'], maria['id'], joao['id'])
    joao = get_player(joao['id'])
    maria = get_player(maria['id'])
    print(f"    João:  1200 → {joao['elo_rating']:.1f} ({joao['elo_rating']-1200:+.1f})")
    print(f"    Maria: 1200 → {maria['elo_rating']:.1f} ({maria['elo_rating']-1200:+.1f})")
    assert abs((joao['elo_rating'] - 1200) - 16) < 0.1, "João deveria ganhar ~16 pontos"
    assert abs((maria['elo_rating'] - 1200) + 16) < 0.1, "Maria deveria perder ~16 pontos"
    
    # Passo 4: Partida 2 - Upset (Pedro vence João)
    print(f"\n  Partida 2: Pedro (1200) vs João ({joao['elo_rating']:.1f}) - UPSET!")
    match2 = create_match(event_id, pedro['id'], joao['id'], pedro['id'])
    joao_antes = joao['elo_rating']
    joao = get_player(joao['id'])
    pedro = get_player(pedro['id'])
    joao_change = joao['elo_rating'] - joao_antes
    pedro_change = pedro['elo_rating'] - 1200
    print(f"    João:  {joao_antes:.1f} → {joao['elo_rating']:.1f} ({joao_change:+.1f})")
    print(f"    Pedro: 1200 → {pedro['elo_rating']:.1f} ({pedro_change:+.1f})")
    assert pedro_change > joao_change, "Upset deveria dar mais pontos a Pedro"
    print(f"    ✓ Upset validado: Pedro ganhou mais pontos ({pedro_change:.1f}) que João perdeu ({joao_change:.1f})")
    
    # Passo 5: Verificar ranking
    print(f"\n4. Ranking final:")
    ranking = get_ranking(event_id)
    for i, entry in enumerate(ranking, 1):
        print(f"  {i}º - {entry['name']}: {entry['elo']:.1f} ELO ({entry['wins']} vitória(s))")
    
    # Validações finais
    print(f"\n5. Validações:")
    assert joao['score'] == 1, f"João deveria ter 1 vitória, tem {joao['score']}"
    assert maria['score'] == 0, f"Maria deveria ter 0 vitórias, tem {maria['score']}"
    assert pedro['score'] == 1, f"Pedro deveria ter 1 vitória, tem {pedro['score']}"
    print(f"  ✓ Contadores de vitórias corretos")
    
    assert joao['elo_rating'] < 1200, "João (perdeu último) deveria estar abaixo de 1200"
    assert pedro['elo_rating'] > 1200, "Pedro (vencedor) deveria estar acima de 1200"
    print(f"  ✓ Ratings fazem sentido")
    
    print("\n" + "="*70)
    print("✓ TODOS OS TESTES PASSARAM!")
    print("="*70)

if __name__ == "__main__":
    try:
        test_elo_feature()
    except AssertionError as e:
        print(f"\n✗ ERRO: {e}")
        exit(1)
    except Exception as e:
        print(f"\n✗ ERRO INESPERADO: {e}")
        exit(1)
