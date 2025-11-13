# 🎯 Refinamento Feature 1: Organização de Partidas
**Fórmula de Ranking, Frequência de Atualização e Ciclo de Vida de Membership**

**Data:** 13 de novembro de 2025  
**Versão:** 1.0  
**Status:** ✅ Especificação Finalizada

---

## 📋 Índice

1. [Fórmula ELO](#fórmula-elo)
2. [Frequência de Atualização](#frequência-de-atualização)
3. [Ciclo de Vida de Membership](#ciclo-de-vida-de-membership)
4. [Tipos de Torneio](#tipos-de-torneio)
5. [Modelos de Dados](#modelos-de-dados)
6. [Fluxo de Implementação](#fluxo-de-implementação)

---

## 1. Fórmula ELO

### 📌 O que é ELO?

**ELO (Elo Rating)** é um sistema matemático que:
- Calcula o nível de habilidade de um jogador baseado em resultados
- Ajusta ratings após cada partida
- Considera a diferença de força entre adversários
- Recompensa vitórias inesperadas

**Origem:** Criado por Arpad Elo para xadrez, agora usado em: League of Legends, Dota 2, Pokémon, Badminton...

### ✅ Vantagens para Ping-Pong

| Aspecto | Benefício |
|--------|----------|
| **Justo** | Jogadores fracos ganham mais pontos por vitória |
| **Dinâmico** | Rankings mudam após cada partida |
| **Previsível** | Odds de vitória calculáveis |
| **Escalável** | Funciona com 10 ou 10.000 jogadores |
| **Competitivo** | Mantém tensão e engajamento |

### 🧮 Fórmula Matemática

```
Novo Rating = Rating Antigo + K × (Resultado - Expected Score)

Onde:
  K = Fator de multiplicador (30 padrão, 16 para masters)
  Resultado = 1 se ganhou, 0 se perdeu, 0.5 se empate
  Expected Score = 1 / (1 + 10^((Rating Adversário - Rating) / 400))
```

### 📊 Exemplo Prático

**Cenário:** João (1200) vence Maria (1400)

**Passo 1: Calcular Expected Score de João**
```
Expected = 1 / (1 + 10^((1400 - 1200) / 400))
         = 1 / (1 + 10^(0.5))
         = 1 / (1 + 3.162)
         = 1 / 4.162
         ≈ 0.240 (24% chance esperado)
```

**Passo 2: João venceu (Resultado = 1)**
```
Change = 30 × (1 - 0.240)
       = 30 × 0.760
       = 22.8 pontos

Novo Rating João = 1200 + 22.8 = 1222.8
```

**Passo 3: Maria perdeu (Resultado = 0)**
```
Expected = 1 / (1 + 10^((1200 - 1400) / 400))
         = 1 / (1 + 10^(-0.5))
         = 1 / (1 + 0.316)
         = 1 / 1.316
         ≈ 0.760 (76% chance esperado)

Change = 30 × (0 - 0.760)
       = 30 × (-0.760)
       = -22.8 pontos

Novo Rating Maria = 1400 - 22.8 = 1377.2
```

**Resultado:**
- João: 1200 → 1222.8 (+22.8) ✅ Ganho por upset
- Maria: 1400 → 1377.2 (-22.8) ⚠️ Perda esperada (quase nenhuma penalidade)

### ⚙️ Parâmetros Ajustáveis

**K-Factor (Volatilidade)**
```python
# Padrão por nível
K_NOVATO = 32        # Novatos (0-5 partidas) - muda rápido
K_INTERMEDIARIO = 24 # Intermediários - estável
K_MASTER = 16        # Masters (2200+) - quase não muda

# Regra de atribuição
def get_k_factor(rating: int, match_count: int) -> int:
    if match_count < 5:
        return 32  # Novato
    elif rating >= 2200:
        return 16  # Master
    else:
        return 24  # Intermediário
```

**Bônus Iniciais**
```python
INITIAL_RATING = 1200
INITIAL_DEVIATION = 350  # Incerteza (será refinado)
```

### 📈 Implementação Python

```python
from math import log10

class ELOCalculator:
    def __init__(self, k_factor: int = 30):
        self.k_factor = k_factor
    
    def expected_score(self, player_rating: float, opponent_rating: float) -> float:
        """
        Calcula a probabilidade esperada de vitória
        
        Args:
            player_rating: Rating do jogador
            opponent_rating: Rating do adversário
        
        Returns:
            Valor entre 0 e 1 (0 = 0%, 1 = 100%)
        """
        rating_diff = opponent_rating - player_rating
        return 1 / (1 + 10 ** (rating_diff / 400))
    
    def new_rating(self, 
                   old_rating: float, 
                   opponent_rating: float,
                   result: int) -> float:
        """
        Calcula novo rating após partida
        
        Args:
            old_rating: Rating anterior
            opponent_rating: Rating do adversário
            result: 1 (ganhou), 0 (perdeu), 0.5 (empate)
        
        Returns:
            Novo rating (float)
        """
        expected = self.expected_score(old_rating, opponent_rating)
        change = self.k_factor * (result - expected)
        return old_rating + change
    
    def calculate_match_outcome(self, 
                               player1_rating: float,
                               player2_rating: float,
                               winner_id: int) -> dict:
        """
        Calcula novo ratings para ambos após partida
        
        Returns:
            {
                'player1_new_rating': float,
                'player2_new_rating': float,
                'player1_change': float,
                'player2_change': float
            }
        """
        result1 = 1 if winner_id == 1 else 0
        result2 = 1 - result1
        
        new_rating1 = self.new_rating(player1_rating, player2_rating, result1)
        new_rating2 = self.new_rating(player2_rating, player1_rating, result2)
        
        return {
            'player1_new_rating': new_rating1,
            'player2_new_rating': new_rating2,
            'player1_change': new_rating1 - player1_rating,
            'player2_change': new_rating2 - player2_rating
        }


# Teste
elo = ELOCalculator(k_factor=30)
result = elo.calculate_match_outcome(1200, 1400, winner_id=1)
print(f"João: +{result['player1_change']:.1f}")  # +22.8
print(f"Maria: {result['player2_change']:.1f}")  # -22.8
```

### 🔄 Quando Recalcular?

**Opção A: Real-time (Recomendado)**
```
Operação: Usuário cria/finaliza match → ELO recalculado imediatamente
Vantagem: Rankings sempre atualizados, jogadores veem mudanças ao vivo
Desvantagem: Mais cálculos no banco de dados
```

**Opção B: Batch (Noturno)**
```
Operação: Cron job 00:00 → Processa todas as matches do dia
Vantagem: Performance, menos cálculos durante o dia
Desvantagem: Rankings desatualizados até meia-noite
```

**Recomendação:** **Real-time** (Opção A)
- Ping-pong é sport com poucos matches por dia
- Jogadores esperam feedback imediato
- Implementar cache para evitar lentidão

---

## 2. Frequência de Atualização

### ❓ Qual parte do projeto?

**A frequência de atualização ELO afeta:**

```
Frontend
  ↓
[User clica "Match Finalizado"]
  ↓
API (Backend)
  ├─→ 1️⃣ Validar dados
  ├─→ 2️⃣ Salvar Match no DB
  ├─→ 3️⃣ Calcular novo ELO [AQUI]
  ├─→ 4️⃣ Atualizar Rating dos Jogadores
  ├─→ 5️⃣ Atualizar Ranking do Grupo
  └─→ 6️⃣ Retornar resultado
  ↓
Frontend
  └─→ Atualiza ranking em tempo real
```

### 🏗️ Arquitetura de Atualização

```yaml
Fluxo Real-time:
  
  1. POST /api/v1/grupos/{grupo_id}/eventos/{evento_id}/partidas
     Payload:
       {
         "jogador_1_id": 5,
         "jogador_2_id": 12,
         "vencedor_id": 5
       }
  
  2. Backend:
     - Validar se match é válida (ambos no evento)
     - Buscar ratings atuais de ambos
     - Calcular novo ELO (função acima)
     - Atualizar ratings no DB
     - Retornar novos ratings
  
  3. Response:
     {
       "match_id": 42,
       "jogador_1": {
         "id": 5,
         "rating_antigo": 1200,
         "rating_novo": 1222.8,
         "change": +22.8
       },
       "jogador_2": {
         "id": 12,
         "rating_antigo": 1400,
         "rating_novo": 1377.2,
         "change": -22.8
       }
     }
  
  4. Frontend:
     - Recebe resposta
     - Atualiza UI com novos ratings
     - Mostra animação de mudança
     - Atualiza ranking da página
```

### ⚡ Otimizações de Performance

**1. Cache de Rankings**
```python
# backend/routers/ranking.py

from functools import lru_cache
import time

class RankingCache:
    def __init__(self, ttl_seconds=300):  # 5 minutos
        self.cache = {}
        self.ttl = ttl_seconds
    
    def get_ranking(self, grupo_id: int, evento_id: int):
        key = f"{grupo_id}:{evento_id}"
        
        if key in self.cache:
            cached_data, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return cached_data
        
        # Recalcular se expirou
        ranking = db_get_ranking(grupo_id, evento_id)
        self.cache[key] = (ranking, time.time())
        return ranking
    
    def invalidate(self, grupo_id: int, evento_id: int):
        key = f"{grupo_id}:{evento_id}"
        if key in self.cache:
            del self.cache[key]

# Instância global
ranking_cache = RankingCache()

# Uso após criar match:
def create_match(...):
    # Salvar match
    db.add(match)
    
    # Calcular ELO
    novo_elo = elo.calculate(...)
    
    # ✅ Invalidar cache
    ranking_cache.invalidate(grupo_id, evento_id)
    
    return result
```

**2. Índices de Banco de Dados**
```sql
-- Acelerar queries de ranking
CREATE INDEX idx_player_rating ON jogador(grupo_id, evento_id, rating);
CREATE INDEX idx_match_date ON partida(evento_id, data_criacao DESC);
```

**3. Limpar ratings antigos**
```python
# Manter histórico por 30 dias
def cleanup_old_ratings(days=30):
    cutoff_date = datetime.now() - timedelta(days=days)
    RatingHistorico.query.filter(
        RatingHistorico.data_criacao < cutoff_date
    ).delete()
    db.commit()
```

### 📊 Monitoramento

```python
# backend/utils/monitoring.py

import logging
from datetime import datetime

class ELOMonitor:
    def __init__(self):
        self.logger = logging.getLogger('elo')
    
    def log_calculation(self, jogador_id: int, rating_change: float, 
                       adversario_rating: int, result: str):
        self.logger.info(
            f"ELO: Player {jogador_id} | "
            f"Change: {rating_change:+.1f} | "
            f"vs {adversario_rating} | "
            f"Result: {result}"
        )
    
    def check_rating_sanity(self, rating: float):
        """Validar se rating está em range aceitável"""
        if not (400 <= rating <= 3000):
            self.logger.warning(f"Unusual rating: {rating}")
        return 400 <= rating <= 3000
```

---

## 3. Ciclo de Vida de Membership

### 📋 O que é?

**Membership** é a relação de um **jogador com um grupo**:

```
Grupo: "Copa Sudeste 2025"
  ├─ Maria (Membro ativo)
  ├─ João (Membro ativo)
  ├─ Pedro (Membro saiu em 2024-11)
  └─ Ana (Membro suspenso)
```

### 🔄 Estados de Membership

```
                    ┌─────────────────────────┐
                    │   CONVIDADO             │
                    │ (Convite enviado)       │
                    └──────────┬──────────────┘
                               │
                               ↓
         ┌─────────────────────────────────────────┐
         │   ATIVO                                 │
         │ (Jogando no grupo)                      │
         │ - Pode jogar partidas                   │
         │ - Tem rating no grupo                   │
         │ - Visível no ranking                    │
         └──────┬──────────────────────┬───────────┘
                │                      │
                │ (Sai)               │ (Suspenso)
                ↓                      ↓
         ┌─────────────────┐  ┌──────────────────┐
         │   INATIVO       │  │  SUSPENSO        │
         │ (Saiu do grupo) │  │ (Temporariamente)│
         │ - Sem rating    │  │ - Sem rating     │
         │ - Histórico     │  │ - Pode retornar  │
         └─────────────────┘  └──────────────────┘
                │                      │
                └──────┬───────────────┘
                       ↓
              ┌──────────────────┐
              │   DELETADO       │
              │ (Permanentemente)│
              │ - Sem histórico  │
              └──────────────────┘
```

### 📅 Dados do Ciclo de Vida

```python
# models/membership.py

from datetime import datetime
from database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum

class MembershipStatus(str, Enum):
    CONVIDADO = "convidado"
    ATIVO = "ativo"
    INATIVO = "inativo"  # Saiu
    SUSPENSO = "suspenso"  # Temporariamente
    DELETADO = "deletado"  # Permanentemente

class Membership(Base):
    __tablename__ = "memberships"
    
    id = Column(Integer, primary_key=True)
    
    # Chaves estrangeiras
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=False)
    jogador_id = Column(Integer, ForeignKey("jogadores.id"), nullable=False)
    
    # Status
    status = Column(Enum(MembershipStatus), default=MembershipStatus.CONVIDADO)
    
    # Timeline
    data_convite = Column(DateTime, default=datetime.utcnow)
    data_entrada = Column(DateTime, nullable=True)  # Quando aceitou convite
    data_saida = Column(DateTime, nullable=True)    # Quando saiu
    data_suspensao = Column(DateTime, nullable=True) # Quando foi suspenso
    data_reativacao = Column(DateTime, nullable=True) # Quando voltou do suspenso
    
    # Metadados
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    grupo = relationship("Grupo", back_populates="memberships")
    jogador = relationship("Jogador", back_populates="memberships")
    
    def __repr__(self):
        return f"<Membership {self.jogador.nome} → {self.grupo.nome} ({self.status})>"
```

### 🎬 Transições de Estado

**1. CONVIDADO → ATIVO**
```python
def accept_invite(membership: Membership):
    """Jogador aceita convite"""
    membership.status = MembershipStatus.ATIVO
    membership.data_entrada = datetime.utcnow()
    
    # Criar rating inicial
    jogador_rating = JogadorRating(
        jogador_id=membership.jogador_id,
        grupo_id=membership.grupo_id,
        rating=1200,  # Rating inicial
        desvio=350    # Incerteza alta
    )
    db.add(jogador_rating)
    db.commit()
    
    return membership
```

**2. ATIVO → INATIVO**
```python
def leave_group(membership: Membership):
    """Jogador sai do grupo"""
    membership.status = MembershipStatus.INATIVO
    membership.data_saida = datetime.utcnow()
    
    # ✅ NÃO deletar rating (preservar histórico)
    # Rating fica marcado como "histórico"
    
    db.commit()
    return membership
```

**3. ATIVO → SUSPENSO**
```python
def suspend_member(membership: Membership, reason: str):
    """Admin suspende jogador"""
    membership.status = MembershipStatus.SUSPENSO
    membership.data_suspensao = datetime.utcnow()
    
    # Jogador não pode jogar enquanto suspenso
    db.commit()
    
    # Enviar notificação
    notify_suspension(membership.jogador, membership.grupo, reason)
```

**4. SUSPENSO → ATIVO**
```python
def reactivate_member(membership: Membership):
    """Admin reativa jogador"""
    membership.status = MembershipStatus.ATIVO
    membership.data_reativacao = datetime.utcnow()
    
    db.commit()
```

**5. Qualquer → DELETADO**
```python
def hard_delete_membership(membership: Membership):
    """Deletar permanentemente (raro)"""
    membership.status = MembershipStatus.DELETADO
    
    # Opcionalmente, deletar ratings também
    JogadorRating.query.filter_by(
        jogador_id=membership.jogador_id,
        grupo_id=membership.grupo_id
    ).delete()
    
    db.commit()
```

### 📊 Consultas Importantes

```python
# routers/memberships.py

def get_active_members(grupo_id: int):
    """Todos jogadores ativos do grupo"""
    return db.query(Membership).filter(
        Membership.grupo_id == grupo_id,
        Membership.status == MembershipStatus.ATIVO
    ).all()

def get_member_history(jogador_id: int, grupo_id: int):
    """Histórico completo de um membro no grupo"""
    return db.query(Membership).filter(
        Membership.jogador_id == jogador_id,
        Membership.grupo_id == grupo_id
    ).first()

def get_membership_timeline(membership_id: int):
    """Timeline de evento de um membership"""
    membership = db.query(Membership).get(membership_id)
    return {
        "convite": membership.data_convite,
        "entrada": membership.data_entrada,
        "saida": membership.data_saida,
        "suspensao": membership.data_suspensao,
        "reativacao": membership.data_reativacao,
        "status": membership.status
    }
```

### 🎯 Implicações para Ranking

**Regra 1: Membros inativos não aparecem no ranking**
```python
def get_ranking_grupo(grupo_id: int, evento_id: int):
    return db.query(JogadorRating).join(Membership).filter(
        JogadorRating.grupo_id == grupo_id,
        JogadorRating.evento_id == evento_id,
        Membership.status == MembershipStatus.ATIVO  # ← Apenas ativos
    ).order_by(JogadorRating.rating.desc()).all()
```

**Regra 2: Histórico preservado mesmo após sair**
```python
def get_player_history(jogador_id: int, grupo_id: int):
    """Mostrar toda a história do jogador no grupo"""
    # Inclui períodos inativos
    return JogadorRating.query.filter(
        JogadorRating.jogador_id == jogador_id,
        JogadorRating.grupo_id == grupo_id
    ).order_by(JogadorRating.data_criacao.desc()).all()
```

---

## 4. Tipos de Torneio

### 🌍 Baseado em: https://mycup.me/blog/tournament-types/

Ping Champions suportará os 3 tipos principais:

### 1️⃣ Single Elimination (Eliminação Simples)

**Descrição:**
- Uma perda = você está fora
- Rápido e dramático
- Ideal para eventos pequenos/rápidos

**Exemplo Visual:**
```
┌─────────────┐
│ 8 Jogadores │
└──────┬──────┘
       │
   SEMIFINAIS (4 partidas)
       │
   ┌───┴────┬────┬────┐
   │        │    │    │
   P1 ─────┐    │    │
   P2 ─────┘    │    │
              │    │    │
   P3 ─────┐    │    │
   P4 ─────┘    │    │
              │    │
   P5 ─────┐    │    │
   P6 ─────┘    │    │
              │    │
   P7 ─────┐    │    │
   P8 ─────┘    │    │
                │    │
   QUARTAS (2 partidas)
                │
           ┌────┴────┐
           │         │
        SEMIFINAL     │
           │         │
        ┌──┴──┐      │
        │     │      │
       FINAL  │      │
        │     │      │
        └─────┘  3º lugar
            │        │
          CAMPEÃO  VICE
```

**Características de Dados:**
```python
class SingleElimination:
    TOTAL_MATCHES = (num_players - 1)  # 8 players = 7 matches
    ROUNDS = log2(num_players)         # 8 players = 3 rounds
    SCHEDULING = "rápido"               # Dias/semanas
    FAIRNESS = "baixa"                  # Um upset elimina
```

**Quando usar:**
- ✅ Eventos sociais rápidos
- ✅ Finais de torneios longos
- ✅ Shows/demonstrações
- ❌ Não recomendado como formato único

### 2️⃣ Swiss System (Sistema Suíço)

**Descrição:**
- Ninguém é eliminado
- Cada rodada: vencedores jogam com vencedores, perdedores com perdedores
- N rodadas (típico: 4-9 rodadas)
- Justo e eficiente para grandes grupos

**Exemplo Visual:**
```
RODADA 1: Todos jogam (emparelhamento aleatório)
  P1 vs P5 → P1 vence
  P2 vs P6 → P2 vence
  P3 vs P7 → P7 vence
  P4 vs P8 → P8 vence
  
  Placar: P1 (1-0), P2 (1-0), P7 (1-0), P8 (1-0)
          P3 (0-1), P4 (0-1), P5 (0-1), P6 (0-1)

RODADA 2: Vencedores com vencedores
  P1 vs P2 → P2 vence
  P7 vs P8 → P7 vence
  P3 vs P4 → P4 vence
  P5 vs P6 → P5 vence
  
  Placar: P2 (2-0), P7 (2-0)
          P1 (1-1), P4 (1-1), P5 (1-1), P8 (1-1)
          P3 (0-2), P6 (0-2)

RODADA 3: Pelo placar acumulado
  P2 vs P7 → P7 vence
  P1 vs P4 → P1 vence
  ...e assim continua

FINAL: Ranking por vitórias, depois tiebreaker (ex: SOS = Sum of Opponents' Scores)
  1º: P7 (3-0)
  2º: P2 (2-1)
  3º: P1 (2-1) [melhor SOS]
  ...
```

**Características de Dados:**
```python
class SwissSystem:
    TOTAL_MATCHES = (num_players / 2) × num_rounds  # 8 players, 4 rounds = 16 matches
    ROUNDS = 4 a 9                                   # Ajustável
    FAIRNESS = "médio-alto"                         # Todos jogam sempre
    SCHEDULING = "médio"                             # Semanas
    TIEBREAKER = "SOS ou SOSOS"                     # Sum of Opponents' Scores
```

**Quando usar:**
- ✅ Grandes grupos (50-500 jogadores)
- ✅ Tempo limitado
- ✅ Máxima fairness necessária
- ✅ Campeonatos regionais

### 3️⃣ Group + Knockout Hybrid (Fase de Grupos + Eliminação)

**Descrição:**
- Fase 1: Grupos com Round Robin (todos jogam com todos)
- Fase 2: Knockout com jogadores do topo dos grupos
- Melhor balance entre fairness e drama

**Exemplo Visual:**
```
FASE 1: GRUPOS (Round Robin)
  
  GRUPO A          GRUPO B
  P1 vs P2 ✓       P5 vs P6 ✓
  P1 vs P3 ✓       P5 vs P7 ✓
  P2 vs P3 ✓       P6 vs P7 ✓
  
  Final Grupo A:   Final Grupo B:
  1º: P1 (2-0)     1º: P5 (2-0)
  2º: P2 (1-1)     2º: P6 (1-1)
  3º: P3 (0-2)     3º: P7 (0-2)

CLASSIFICAÇÃO: Top 2 de cada grupo para knockouts

FASE 2: KNOCKOUT (Eliminação Simples)
  
  SEMIFINAIS
  P1 (Gr.A) vs P6 (Gr.B) → P1 vence
  P5 (Gr.B) vs P2 (Gr.A) → P5 vence
  
  FINAL
  P1 vs P5 → P1 é campeão

  3º LUGAR (opcional)
  P6 vs P2 → P2 é terceiro
```

**Características de Dados:**
```python
class GroupKnockoutHybrid:
    TOTAL_MATCHES = (round_robin_matches) + (knockout_matches)
                  = grupos × (players_per_group × (players_per_group-1) / 2) + (players_in_ko - 1)
    FAIRNESS = "muito alto"
    DRAMA = "muito alto"
    SCHEDULING = "longo"  # Semanas/meses
    TIEBREAKER_RR = "head-to-head, point diff"
```

**Quando usar:**
- ✅ Campeonatos nacionais (Copa Sudeste, Brasil Open)
- ✅ Torneios de temporada
- ✅ Máxima audience/excitement
- ✅ 20-500+ jogadores

### 📊 Tabela Comparativa

| Aspecto | Single Elimination | Swiss System | Group+KO |
|---------|-------------------|--------------|----------|
| **Fairness** | Baixa | Média-Alta | Muito Alta |
| **Drama** | Muito Alto | Médio | Muito Alto |
| **# Matches** | n-1 | n/2 × rounds | rr + ko |
| **Tempo** | Curto | Médio | Longo |
| **Melhor para** | <20 jogadores | 50-500 | 20-500+ |
| **Complexidade** | Baixa | Média | Alta |
| **Scheduling** | Fácil | Médio | Complexo |

---

## 5. Modelos de Dados

### 📐 Evento com Tipo de Torneio

```python
# models/event.py

from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, JSON

class TipoTorneio(PyEnum):
    SINGLE_ELIMINATION = "single_elimination"
    SWISS_SYSTEM = "swiss_system"
    GROUP_KNOCKOUT_HYBRID = "group_knockout_hybrid"

class Evento(Base):
    __tablename__ = "eventos"
    
    id = Column(Integer, primary_key=True)
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=False)
    
    # Informações básicas
    nome = Column(String(255), nullable=False)
    descricao = Column(String(1000))
    data_criacao = Column(DateTime, default=datetime.utcnow)
    
    # Tipo de torneio
    tipo_torneio = Column(Enum(TipoTorneio), default=TipoTorneio.SINGLE_ELIMINATION)
    
    # Configuração do torneio (JSON)
    config = Column(JSON, default={})
    # Exemplos:
    # Single Elim: {"seed_method": "random"}
    # Swiss: {"num_rounds": 5, "tiebreaker": "SOS"}
    # Group+KO: {"groups": 2, "per_group": 4, "advance": 2}
    
    # Status
    status = Column(String(50), default="planejamento")  # planejamento, ativo, finalizado
    data_inicio = Column(DateTime)
    data_fim = Column(DateTime)
    
    # Soft delete
    ativo = Column(Boolean, default=True)
    
    # Relacionamentos
    grupo = relationship("Grupo", back_populates="eventos")
    partidas = relationship("Partida", back_populates="evento", cascade="all, delete-orphan")
    memberships = relationship("Membership", back_populates="evento")
    
    def __repr__(self):
        return f"<Evento {self.nome} ({self.tipo_torneio})>"


# Exemplo de criação

# Single Elimination
evento_se = Evento(
    nome="Campeonato Rápido",
    tipo_torneio=TipoTorneio.SINGLE_ELIMINATION,
    config={
        "seed_method": "random",  # ou "by_rating"
        "qual_players": 8
    }
)

# Swiss System
evento_swiss = Evento(
    nome="Liga Sudeste",
    tipo_torneio=TipoTorneio.SWISS_SYSTEM,
    config={
        "num_rounds": 5,
        "tiebreaker": "SOS",  # Sum of Opponent's Scores
        "bye_handling": "skip"  # Como lidar com odds
    }
)

# Group + Knockout
evento_hybrid = Evento(
    nome="Copa Brasil",
    tipo_torneio=TipoTorneio.GROUP_KNOCKOUT_HYBRID,
    config={
        "group_stage": {
            "num_groups": 4,
            "per_group": 5,  # 5 jogadores por grupo
            "format": "round_robin"
        },
        "knockout_stage": {
            "advance_per_group": 2,  # Top 2 de cada grupo
            "format": "single_elimination"
        }
    }
)
```

### 📝 Tabela de Partidas

```python
# models/match.py (melhorado)

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean

class Partida(Base):
    __tablename__ = "partidas"
    
    id = Column(Integer, primary_key=True)
    
    # Identificação
    evento_id = Column(Integer, ForeignKey("eventos.id"), nullable=False)
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=False)
    
    # Jogadores
    jogador_1_id = Column(Integer, ForeignKey("jogadores.id"), nullable=False)
    jogador_2_id = Column(Integer, ForeignKey("jogadores.id"), nullable=False)
    vencedor_id = Column(Integer, ForeignKey("jogadores.id"), nullable=False)
    
    # Resultado
    pontos_j1 = Column(Integer)
    pontos_j2 = Column(Integer)
    
    # ELO antes/depois
    elo_j1_antes = Column(Float)
    elo_j1_depois = Column(Float)
    elo_j2_antes = Column(Float)
    elo_j2_depois = Column(Float)
    
    # Timeline
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Soft delete
    ativo = Column(Boolean, default=True)
    
    # Relacionamentos
    evento = relationship("Evento", back_populates="partidas")
    grupo = relationship("Grupo", back_populates="partidas")
    jogador_1 = relationship("Jogador", foreign_keys=[jogador_1_id])
    jogador_2 = relationship("Jogador", foreign_keys=[jogador_2_id])
    vencedor = relationship("Jogador", foreign_keys=[vencedor_id])
    
    def __repr__(self):
        return f"<Partida {self.jogador_1} vs {self.jogador_2}>"
```

### ⭐ Rating do Jogador (Novo)

```python
# models/rating.py (NOVO)

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Index

class JogadorRating(Base):
    __tablename__ = "jogador_ratings"
    
    id = Column(Integer, primary_key=True)
    
    # Identificação
    jogador_id = Column(Integer, ForeignKey("jogadores.id"), nullable=False)
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=False)
    evento_id = Column(Integer, ForeignKey("eventos.id"), nullable=True)
    
    # Rating
    rating = Column(Float, default=1200)
    desvio = Column(Float, default=350)  # Uncertainty (Glicko-2 concept)
    
    # Histórico
    rating_anterior = Column(Float)
    mudanca_rating = Column(Float)
    
    # Contadores
    num_partidas = Column(Integer, default=0)
    num_vitorias = Column(Integer, default=0)
    num_derrotas = Column(Integer, default=0)
    
    # Timeline
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Índices para performance
    __table_args__ = (
        Index('idx_jogador_grupo_evento', 'jogador_id', 'grupo_id', 'evento_id'),
        Index('idx_grupo_rating', 'grupo_id', 'rating'),
    )
    
    # Relacionamentos
    jogador = relationship("Jogador", back_populates="ratings")
    grupo = relationship("Grupo", back_populates="ratings")
    evento = relationship("Evento")
    
    def __repr__(self):
        return f"<Rating {self.jogador} = {self.rating:.1f}>"
```

---

## 6. Fluxo de Implementação

### 📅 Sprint 1: Fundação ELO (2 semanas)

**Tarefas:**

```
BACKEND:
  ☐ Criar classe ELOCalculator (utils/elo.py)
  ☐ Criar modelo JogadorRating
  ☐ Criar migrations de banco de dados
  ☐ Implementar POST /api/v1/partidas com cálculo ELO
  ☐ Criar índices para performance
  ☐ Testes unitários (ELO math)
  ☐ Testes integração (API + DB)

FRONTEND:
  ☐ Criar componente de resultado de partida
  ☐ Mostrar mudança de rating (+22.8)
  ☐ Testes de UX

QA:
  ☐ Validar cálculos ELO
  ☐ Testar edge cases (ratings extremos)
  ☐ Performance com 1000+ partidas
```

### 📅 Sprint 2: Membership Lifecycle (2 semanas)

**Tarefas:**

```
BACKEND:
  ☐ Criar modelo Membership com estados
  ☐ Migrations para data_entrada/saida
  ☐ Implementar transições de estado
  ☐ POST /api/v1/memberships/{id}/accept
  ☐ POST /api/v1/memberships/{id}/leave
  ☐ Validar: só jogadores ativos podem jogar
  ☐ Testes de state machine

FRONTEND:
  ☐ UI para aceitar/rejeitar convites
  ☐ UI para sair do grupo
  ☐ Timeline visual (entrada/saída)

QA:
  ☐ Testar todas as transições
  ☐ Validar histórico preservado
```

### 📅 Sprint 3: Tipos de Torneio (3 semanas)

**Tarefas:**

```
BACKEND:
  ☐ Criar modelo Evento com tipo_torneio
  ☐ Single Elimination bracket generator
  ☐ Swiss System pairing algorithm
  ☐ Group+KO bracket logic
  ☐ POST /api/v1/eventos/{id}/start-bracket
  ☐ Validações por tipo
  ☐ Testes de brackets

FRONTEND:
  ☐ UI para criar evento com tipo
  ☐ Visualizar bracket (SE + Swiss)
  ☐ Componente de partidas próximas

QA:
  ☐ Testar bracket generation
  ☐ Validar fairness (Swiss pairings)
  ☐ Teste com 20, 50, 100 jogadores
```

### 📅 Sprint 4: Polish & Performance (2 semanas)

**Tarefas:**

```
BACKEND:
  ☐ Cache de rankings (Redis)
  ☐ Otimizar queries de ranking
  ☐ Monitoramento de ELO
  ☐ Cleanup de dados antigos
  ☐ Testes de performance (load test)

FRONTEND:
  ☐ Animações de ranking updates
  ☐ Real-time updates (WebSocket?)
  ☐ Responsivo em mobile

QA:
  ☐ Performance com 10k+ partidas
  ☐ Teste de carga
  ☐ E2E completo (Feature 1)
```

---

## ✅ Checklist de Finalização

- [x] Fórmula ELO especificada (K-factor, expected score)
- [x] Frequência real-time com cache
- [x] Ciclo de vida membership (5 estados)
- [x] Tipos de torneio (SE, Swiss, Group+KO)
- [x] Modelos de dados (Evento, JogadorRating, Membership)
- [x] Roadmap (4 sprints, 9 semanas)
- [ ] Implementação iniciada
- [ ] Testes passando
- [ ] Deploy para produção

---

**Próximo:** Feature 2 (Usuários e RBAC) ou iniciar Sprint 1?

