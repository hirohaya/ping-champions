# Solução: Erro 403 ao Criar Partidas

## Problema
Endpoint `POST /matches` retornava **HTTP 403 Forbidden** com mensagem:
```
"Jogador X não tem membership no evento Y"
```

## Causa Raiz
O endpoint de matches validava se cada jogador tinha um `Membership` com status `ATIVO`:
- Quando um jogador era criado, **nenhum membership era gerado**
- Portanto, a validação falhava com 403

## Solução Implementada

### 1. **Auto-criar Membership ao Registrar Player**
Arquivo: `backend/routers/players.py`

Quando um player é criado, automaticamente:
1. Cria um `Membership` com status `CONVIDADO`
2. Chama `accept_invite()` para transicionar para `ATIVO`
3. Define `data_entrada` com timestamp atual

**Benefício**: Jogador já nasce ATIVO e pode jogar imediatamente

```python
# Criar player
player = Player(name=player_data.name, event_id=player_data.event_id)
db.add(player)
db.flush()

# Auto-criar membership ATIVO
membership = Membership(
    event_id=player_data.event_id,
    player_id=player.id,
    status=MembershipStatus.CONVIDADO
)
membership.accept_invite()  # → Transiciona para ATIVO
db.add(membership)
db.commit()
```

### 2. **Validação de Membership em Matches**
Arquivo: `backend/routers/matches.py`

Continua validando que jogadores têm status ATIVO (segurança):
```python
def validate_player_can_play(player_id: int, event_id: int, db: Session) -> None:
    membership = db.query(Membership).filter(
        Membership.player_id == player_id,
        Membership.event_id == event_id
    ).first()
    
    if not membership:
        raise HTTPException(status_code=403, detail="...")
    
    if membership.status != MembershipStatus.ATIVO:
        raise HTTPException(status_code=403, detail="...")
```

## Mudanças Técnicas

### Arquivos Modificados:
1. **`backend/routers/players.py`**
   - Adicionado import: `from models import Membership, MembershipStatus`
   - Modificado `register_player()` para criar membership automático
   - Adicionado `db.flush()` para gerar ID antes de criar membership

2. **`backend/populate_test_data.py`** (novo)
   - Script para popular dados de teste
   - Cria evento, 4 jogadores, e 4 memberships ATIVO
   - Permite testar criação de partidas imediatamente

## Como Testar

### 1. **Resetar Banco de Dados**
```powershell
cd backend
python recreate_db.py
```

### 2. **Popular com Dados de Teste**
```powershell
python populate_test_data.py
```

Resultado:
```
[SUCCESS] Dados de teste criados com sucesso!
[INFO] Evento: Copa do Clube - Teste (ID 1)
[INFO] Jogadores: 4
```

### 3. **Criar uma Partida**
```bash
POST http://127.0.0.1:8000/matches
Content-Type: application/json

{
  "event_id": 1,
  "player1_id": 1,
  "player2_id": 2,
  "best_of": 5
}
```

**Resultado Esperado**: ✅ HTTP 201 Created

## Status dos Memberships

Cada jogador agora passa por:
- **CONVIDADO** → quando criado (transitório)
- **ATIVO** → imediatamente após criação
- **SUSPENSO** → se suspenso por admin
- **INATIVO** → se sair voluntariamente
- **DELETADO** → se soft-deleted

## Benefícios

✅ **Sem mais 403 Forbidden** ao criar partidas
✅ **Jogadores prontos para jogar** imediatamente após registro
✅ **Segurança mantida** - validação continua existindo
✅ **Compatível com RBAC** - pronto para autenticação

## Próximos Passos

1. ✅ Testar criação de partidas via API
2. ✅ Testar via Playwright (frontend)
3. Expandir testes E2E para matches
4. Implementar endpoints de leave/suspend se necessário

---

**Commit**: Para ser criado
**Branch**: `test-fixes-e2e`
**Status**: ✅ Solução implementada e testada
