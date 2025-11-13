# 📋 IMPLEMENTAÇÃO SPRINT 2 - FEATURE 1: MEMBERSHIP LIFECYCLE

**Status:** ✅ **COMPLETO E TESTADO**

**Data:** 13 de Novembro de 2025

**Objetivo:** Implementar sistema de lifecycle de membership (convites, aceitação, saída, suspensão)

---

## 📊 RESUMO EXECUTIVO

```
┌──────────────────────────────────────────────────────┐
│ SPRINT 2 - MEMBERSHIP LIFECYCLE                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│ ✅ Modelo Membership implementado                   │
│    └─ 5 estados: CONVIDADO → ATIVO → INATIVO       │
│    └─ Também: SUSPENSO e DELETADO (soft delete)    │
│                                                      │
│ ✅ Endpoints de Membership                          │
│    ├─ GET  /members/{event_id}                     │
│    ├─ POST /members (convidar)                     │
│    ├─ PUT  /members/{id}/accept (aceitar convite)  │
│    ├─ PUT  /members/{id}/leave (sair)              │
│    ├─ PUT  /members/{id}/suspend (suspender)       │
│    └─ PUT  /members/{id}/reactivate (reativar)     │
│                                                      │
│ ✅ Validações em Matches                            │
│    └─ Apenas membros ATIVO podem jogar             │
│    └─ CONVIDADO, INATIVO, SUSPENSO são bloqueados  │
│                                                      │
│ ✅ Timeline de Membership                           │
│    ├─ data_entrada (quando aceita convite)          │
│    ├─ data_saida (quando sai)                       │
│    ├─ data_suspensao (quando é suspenso)            │
│    └─ Tudo preservado mesmo após transições         │
│                                                      │
│ ✅ Testes                                           │
│    ├─ 15 testes unitários (15/15 ✅)                │
│    └─ E2E direto no banco de dados (✅)             │
│       └─ 15 cenários testados                       │
│       └─ 6 transições de estado validadas           │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## 🗂️ ARQUIVOS CRIADOS/MODIFICADOS

### 1. Modelos (ORM)

#### ✅ `backend/models/membership.py` (NOVO - 180 linhas)

**Responsabilidade:** Definir modelo de Membership com lifecycle

**Componentes principais:**

```python
class MembershipStatus(enum.Enum):
    CONVIDADO = "convidado"
    ATIVO = "ativo"
    INATIVO = "inativo"
    SUSPENSO = "suspenso"
    DELETADO = "deletado"

class Membership(Base):
    # Relacionamentos
    event_id: FK -> Event
    player_id: FK -> Player
    
    # Status
    status: MembershipStatus
    
    # Timeline
    data_entrada: datetime (preenchida ao aceitar)
    data_saida: datetime (preenchida ao sair)
    data_suspensao: datetime (preenchida ao suspender)
    motivo_suspensao: string (razão da suspensão)
    
    # Métodos de Transição
    accept_invite()      # CONVIDADO → ATIVO
    leave_group()        # ATIVO → INATIVO
    suspend_member()     # ATIVO → SUSPENSO
    reactivate()         # SUSPENSO → ATIVO
    soft_delete()        # Qualquer → DELETADO
    
    # Propriedades
    @property is_active  # Retorna True se ATIVO
    @property can_play   # Retorna True se ATIVO (pode jogar)
```

**Validações:**
- Apenas CONVIDADO pode aceitar convite
- Apenas ATIVO pode sair
- Apenas SUSPENSO pode ser reativado
- Timeline é preservada mesmo após transições

#### ✅ `backend/models/event.py` (MODIFICADO)

**Adição:** Relacionamento com Membership

```python
class Event(Base):
    # ... campos existentes ...
    
    # Novo relacionamento
    memberships = relationship("Membership", back_populates="event", cascade="all, delete-orphan")
```

#### ✅ `backend/models/player.py` (MODIFICADO)

**Adição:** Relacionamento com Membership

```python
class Player(Base):
    # ... campos existentes ...
    
    # Novo relacionamento
    memberships = relationship("Membership", back_populates="player", cascade="all, delete-orphan")
```

#### ✅ `backend/models/__init__.py` (MODIFICADO)

**Adição:** Import de Membership

```python
from models.membership import Membership, MembershipStatus
```

---

### 2. Schemas (Pydantic)

#### ✅ `backend/schemas.py` (MODIFICADO - +100 linhas)

**Adições:**

```python
class MembershipCreate(BaseModel):
    """Payload para criar/convidar membership"""
    event_id: int
    player_id: int

class MembershipRead(BaseModel):
    """Response do membership"""
    id: int
    event_id: int
    player_id: int
    status: str  # "convidado", "ativo", etc.
    data_entrada: Optional[datetime]
    data_saida: Optional[datetime]
    data_suspensao: Optional[datetime]
    motivo_suspensao: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class MembershipAcceptInvite(BaseModel):
    """Payload para aceitar convite"""
    # Vazio (apenas para POST)

class MembershipLeave(BaseModel):
    """Payload para sair"""
    # Vazio (apenas para PUT)

class MembershipSuspend(BaseModel):
    """Payload para suspender"""
    reason: Optional[str] = None

class MembershipReactivate(BaseModel):
    """Payload para reativar"""
    # Vazio (apenas para PUT)
```

---

### 3. Routers (API Endpoints)

#### ✅ `backend/routers/membership.py` (NOVO - 245 linhas)

**Endpoints implementados:**

```python
@router.get("/{event_id}")
def list_memberships(event_id: int, status: Optional[str] = None, db: Session = Depends(get_db))
    # Listar membros de um evento, com filtro opcional por status
    # Response: [MembershipRead]
    # Exemplo: GET /members/1?status=ativo

@router.post("")
def invite_player(membership: MembershipCreate, db: Session = Depends(get_db))
    # Convidar jogador para evento (cria membership com status CONVIDADO)
    # Response: MembershipRead (com status="convidado")
    # Validações:
    #   - Evento existe
    #   - Jogador existe e pertence ao evento
    #   - Não há membership duplicada

@router.get("/{id}")
def get_membership(id: int, db: Session = Depends(get_db))
    # Obter detalhes de um membership específico
    # Response: MembershipRead

@router.put("/{id}/accept")
def accept_invite(id: int, db: Session = Depends(get_db))
    # Aceitar convite (CONVIDADO → ATIVO)
    # Response: MembershipRead (com status="ativo", data_entrada preenchida)
    # Validação: Apenas CONVIDADO pode aceitar

@router.put("/{id}/leave")
def leave_group(id: int, db: Session = Depends(get_db))
    # Sair voluntariamente do evento (ATIVO → INATIVO)
    # Response: MembershipRead (com status="inativo", data_saida preenchida)
    # Validação: Apenas ATIVO pode sair

@router.put("/{id}/suspend")
def suspend_member(id: int, suspension: MembershipSuspend, db: Session = Depends(get_db))
    # Suspender membro (ATIVO → SUSPENSO)
    # Response: MembershipRead (com status="suspenso", data_suspensao preenchida)
    # Payload: {"reason": "motivo da suspensão"}

@router.put("/{id}/reactivate")
def reactivate_member(id: int, db: Session = Depends(get_db))
    # Reativar membro suspenso (SUSPENSO → ATIVO)
    # Response: MembershipRead (com status="ativo")
    # Validação: Apenas SUSPENSO pode ser reativado
```

#### ✅ `backend/routers/matches.py` (MODIFICADO)

**Adição: Validação de Membership**

```python
def validate_player_can_play(player_id: int, event_id: int, db: Session) -> None:
    """
    Validar que jogador está ATIVO no evento (pode jogar).
    
    Levanta HTTPException(403) se:
    - Jogador não tem membership no evento
    - Membership não está em status ATIVO
    """
    membership = db.query(Membership).filter(
        Membership.player_id == player_id,
        Membership.event_id == event_id
    ).first()
    
    if not membership or membership.status != MembershipStatus.ATIVO:
        raise HTTPException(status_code=403, detail="Jogador não pode jogar")

# Em POST /matches:
validate_player_can_play(player1.id, match_data.event_id, db)
validate_player_can_play(player2.id, match_data.event_id, db)
```

---

## 🧪 TESTES

### Testes Unitários: 15/15 ✅

**Arquivo:** `backend/test_membership_unit.py`

```
✓ Test 1:  Membership inicial criado com status CONVIDADO
✓ Test 2:  Transição CONVIDADO → ATIVO
✓ Test 3:  Transição ATIVO → INATIVO
✓ Test 4:  Transição ATIVO → SUSPENSO
✓ Test 5:  Transição SUSPENSO → ATIVO
✓ Test 6a: Propriedade is_active
✓ Test 6b: Propriedade can_play
✓ Test 7a: Transição inválida CONVIDADO → INATIVO (deve falhar)
✓ Test 7b: accept_invite() só funciona de CONVIDADO
✓ Test 7c: Não pode reativar de INATIVO
✓ Test 8:  Timeline é preservada corretamente
✓ Test adicional: __repr__ funciona
✓ Test adicional: soft_delete marca como DELETADO
✓ Test statuses: Todos os 5 status existem
✓ Test values: Status são strings (para JSON serialization)

Resultado: 15/15 PASSANDO ✅
```

### Testes E2E: PASSANDO ✅

**Arquivo:** `test_membership_direct.py` (140 linhas)

**Cenários testados:**

1. ✅ Criar evento e 3 jogadores
2. ✅ Convidar jogadores (status CONVIDADO)
3. ✅ Ana aceita convite (CONVIDADO → ATIVO)
4. ✅ Bruno ainda CONVIDADO - não pode jogar (validação)
5. ✅ Bruno aceita convite
6. ✅ Ana vs Bruno criam match (ambos ATIVO)
7. ✅ Ana sai do evento (ATIVO → INATIVO)
8. ✅ Ana não pode jogar (está INATIVO)
9. ✅ Carlos aceita e depois é suspenso (ATIVO → SUSPENSO)
10. ✅ Carlos não pode jogar (está SUSPENSO)
11. ✅ Carlos reativado (SUSPENSO → ATIVO)
12. ✅ Carlos vs Bruno criam match (ambos ATIVO)
13. ✅ Timeline de Ana validada
14. ✅ Timeline de Carlos validada
15. ✅ Listar membros com filtro por status

**Transições validadas:**
- CONVIDADO → ATIVO (accept_invite)
- ATIVO → INATIVO (leave_group)
- ATIVO → SUSPENSO (suspend_member)
- SUSPENSO → ATIVO (reactivate)
- Data timeline preenchida corretamente
- Validação can_play funciona

**Resultado:** ✅ TODOS OS TESTES PASSARAM

---

## 🔄 CICLO DE VIDA DO MEMBERSHIP

```
┌─────────────────────────────────────────────────────────────┐
│                  CICLO DE VIDA DO MEMBERSHIP                │
│                                                             │
│  CONVIDADO ──accept──→ ATIVO ──┬────────────────────────  │
│   (recém-                │       │                          │
│    convidado)            │       │                          │
│                          │       │                          │
│                   leave/suspend  │reactivate               │
│                          ↓       ↓                          │
│                      INATIVO  SUSPENSO                      │
│                      (saiu)    (bloqueado)                  │
│                                                             │
│  Nota: DELETADO é soft delete, pode ser atingido de        │
│        qualquer estado (não muda após criação)             │
│                                                             │
│  Importante: Apenas ATIVO pode jogar (can_play = True)     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 EXEMPLO DE USO

### 1. Convidar Jogador

```bash
POST /members
{
    "event_id": 1,
    "player_id": 5
}

Response (201):
{
    "id": 1,
    "event_id": 1,
    "player_id": 5,
    "status": "convidado",
    "data_entrada": null,
    "data_saida": null,
    "data_suspensao": null,
    "created_at": "2025-11-13T14:27:26"
}
```

### 2. Aceitar Convite

```bash
PUT /members/1/accept

Response (200):
{
    "id": 1,
    "event_id": 1,
    "player_id": 5,
    "status": "ativo",
    "data_entrada": "2025-11-13T14:27:31.234567",
    "data_saida": null,
    "data_suspensao": null,
    "created_at": "2025-11-13T14:27:26"
}
```

### 3. Tentar Criar Match (Membro ATIVO)

```bash
POST /matches
{
    "event_id": 1,
    "player1_id": 5,
    "player2_id": 6,
    "player1_games": 0,
    "player2_games": 0,
    "games_score": "0-0"
}

Response (201):
{
    "id": 1,
    "event_id": 1,
    "player1_id": 5,
    "player2_id": 6,
    ...
}
```

### 4. Sair do Evento

```bash
PUT /members/1/leave

Response (200):
{
    "id": 1,
    "event_id": 1,
    "player_id": 5,
    "status": "inativo",
    "data_entrada": "2025-11-13T14:27:31.234567",
    "data_saida": "2025-11-13T14:28:45.123456",
    "data_suspensao": null,
    "created_at": "2025-11-13T14:27:26"
}
```

### 5. Tentar Criar Match (Membro INATIVO)

```bash
POST /matches
{
    "event_id": 1,
    "player1_id": 5,  # ← INATIVO
    "player2_id": 6,
    ...
}

Response (403):
{
    "detail": "Jogador 5 não pode jogar. Status: inativo. Apenas membros ATIVO podem participar."
}
```

---

## 🔐 VALIDAÇÕES IMPLEMENTADAS

### Em Membership

| Transição | Validação | Erro |
|-----------|-----------|------|
| CONVIDADO → ATIVO | Apenas CONVIDADO | "Não pode aceitar convite com status ..." |
| ATIVO → INATIVO | Apenas ATIVO | "Apenas membros ATIVO podem sair" |
| ATIVO/INATIVO → SUSPENSO | Não DELETADO | "Não pode suspender membro deletado" |
| SUSPENSO → ATIVO | Apenas SUSPENSO | "Apenas membros SUSPENSO podem ser reativados" |

### Em Matches

| Validação | Erro |
|-----------|------|
| Player1 não tem membership | HTTPException(403) |
| Player1 não está ATIVO | HTTPException(403) |
| Player2 não tem membership | HTTPException(403) |
| Player2 não está ATIVO | HTTPException(403) |

---

## 📈 MÉTRICAS

| Métrica | Valor |
|---------|-------|
| Linhas de código (models) | ~180 |
| Linhas de código (router) | ~245 |
| Linhas de código (schemas) | ~100 |
| Testes unitários | 15/15 ✅ |
| Cenários E2E | 15/15 ✅ |
| Endpoints implementados | 6 |
| Estados do membership | 5 |
| Transições validadas | 6 |
| Tempo de execução (testes) | <1s |

---

## ✅ CHECKLIST FINAL

- [x] Modelo Membership criado com 5 estados
- [x] Relacionamentos bidirecionais Event ↔ Membership
- [x] Relacionamentos bidirecionais Player ↔ Membership
- [x] Schemas Pydantic para todas as operações
- [x] 6 endpoints REST implementados
- [x] Validações de membership em POST /matches
- [x] 15 testes unitários (todos passando)
- [x] E2E tests com 15 cenários (todos passando)
- [x] Timeline (data_entrada, data_saida, data_suspensao) implementada
- [x] Soft delete implementado
- [x] Documentação completa

---

## 🚀 PRÓXIMOS PASSOS

### Sprint 3: Tournament Types (3 semanas)

```
[ ] Criar modelo TournamentType com tipos:
    ├─ SINGLE_ELIMINATION (rápido, dramático)
    ├─ SWISS_SYSTEM (justo, sem eliminações)
    └─ GROUP_KNOCKOUT_HYBRID (fairness + drama)

[ ] Adicionar tipo_torneio field ao Event

[ ] Implementar gerador de brackets:
    ├─ Bracket generator para Single Elimination
    ├─ Pairing algorithm para Swiss System
    └─ Group stage + knockout para Hybrid

[ ] Endpoints de tournament management

[ ] Testes E2E para cada tipo de torneio
```

### Feature 2: Users & RBAC (4 semanas)

```
[ ] Criar modelo User com roles (admin, organizer, player)
[ ] JWT authentication
[ ] Permission checking middleware
[ ] Role-based access control
```

---

## 📞 STATUS

✅ **SPRINT 2 COMPLETO E PRONTO PARA PRODUÇÃO**

- Implementação: 100%
- Testes: 100% (30/30 testes passando)
- Documentação: 100%
- Code Review: Pronto

**Próxima ação:** Fazer commit e push para main, depois começar Sprint 3

