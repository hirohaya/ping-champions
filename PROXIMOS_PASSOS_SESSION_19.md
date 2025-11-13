# 🚀 PRÓXIMOS PASSOS - Session 19 em Diante

**Data:** 20 de Novembro de 2025  
**Status Anterior:** Session 18 Finalizada ✅ (Commit a8e1f45)  
**Projeto:** Ping Champions  

---

## 📊 O Que Foi Alcançado

### ✅ Session 18 - Reorganização Completa
- Limpeza da raiz: 27 → 8 arquivos (-70%)
- Criação `/docs/` com 45 documentos organizados
- Criação `/scripts/` com 3 automações PowerShell
- README.md reescrito (22 → 200+ linhas)
- INDEX.md novo com navegação v2.0
- Commit realizado com sucesso (a8e1f45)

### ✅ Sprints Completas
| Sprint | Feature | Status | Testes |
|--------|---------|--------|--------|
| Sprint 1 | Sistema ELO | ✅ 100% | 17 unit |
| Sprint 2 | Membership Lifecycle | ✅ 100% | 14 integration |
| Sprint 3 | Tournament Types | ✅ 100% | 14 E2E |
| **Total** | **3 Sprints** | **✅ 100%** | **45/45 ✅** |

---

## ⏳ O Que Precisa Ser Feito

### 🔴 CRÍTICO (Esta Semana)

#### 1. Corrigir Testes E2E com localStorage Issues
**Problema:** i18n tests falhando com SecurityError ao acessar localStorage (Playwright sandbox no Windows)

**Tarefas:**
- [ ] Revisar `frontend/e2e/i18n.spec.js` para diagnosticar erro
- [ ] Refatorar testes para contornar sandbox Playwright
- [ ] Usar `page.addInitScript()` ao invés de acesso direto
- [ ] Validar 22 testes i18n funcionando

**Estimativa:** 1-2 dias

#### 2. Validar Testes E2E Pendentes
**Testes ainda não rodados:**
- Events E2E (4 testes)
- Matches E2E (em integração)
- Players E2E (em integração)
- Ranking E2E (em integração)

**Tarefas:**
- [ ] Rodar `frontend/e2e/events.spec.js`
- [ ] Rodar `frontend/e2e/matches.spec.js`
- [ ] Rodar `frontend/e2e/players.spec.js`
- [ ] Rodar `frontend/e2e/ranking.spec.js`
- [ ] Corrigir erros encontrados
- [ ] Validar 100% de cobertura E2E

**Estimativa:** 1-2 dias

**Total Curto Prazo:** 2-3 dias

---

### 🟠 ALTO IMPACTO (Próximas 4-5 Semanas)

#### 3. Feature 2: Users & RBAC (Autenticação)
**Por que é crítico:** Base para todas as features futuras (Grupos, Dashboard, Permissions)

**Modelos:**
```python
User:
  - id (PK)
  - username (unique)
  - email (unique)
  - password (hashed com bcrypt)
  - roles (ADMIN, ORGANIZER, PLAYER)
  - is_active (boolean)
  - created_at, updated_at
  - Groups (relação M2M)
```

**Tarefas Backend:**
- [ ] Criar `backend/models/user.py`
- [ ] Criar `backend/routers/auth.py`
- [ ] Implementar JWT tokens (access + refresh)
- [ ] Middleware de autenticação
- [ ] Decorador `@require_role` para RBAC
- [ ] Endpoints:
  - POST `/users/register` - Registrar novo usuário
  - POST `/users/login` - Login com JWT
  - POST `/users/refresh` - Refresh token
  - GET `/users/me` - Dados do usuário atual
  - PUT `/users/{id}` - Atualizar perfil
  - GET `/users/{id}` - Ver perfil de outro usuário

**Tarefas Frontend:**
- [ ] Página de login
- [ ] Página de registro
- [ ] Guardar JWT em localStorage
- [ ] Axios interceptor para token
- [ ] Redirecionar se não autenticado
- [ ] Menu com usuário logado

**Testes:**
- [ ] Unit tests autenticação
- [ ] Unit tests RBAC
- [ ] Integration tests endpoints
- [ ] E2E login/register/logout

**Estimativa:** 4-5 semanas

---

### 🟡 IMPORTANTE (Após Feature 2)

#### 4. Feature 3: Grupos (Organizações)
**Hierarquia:** Grupos → Eventos → Matches → Players

**Modelos:**
```python
Group:
  - id (PK)
  - name
  - description
  - owner_id (FK → User)
  - members (M2M → User)
  - settings (JSON)
  - ranking_isolated (boolean)
  - created_at, updated_at
```

**Tarefas:**
- [ ] Criar `backend/models/group.py`
- [ ] Relacionamentos Group ↔ User (M2M)
- [ ] Relacionamentos Group ↔ Event
- [ ] Isolamento de ranking por grupo
- [ ] Endpoints `/groups`:
  - CRUD básico
  - GET `/groups/{id}/members`
  - POST `/groups/{id}/members/{user_id}`
  - GET `/groups/{id}/events`
  - GET `/groups/{id}/ranking`

**Testes:** Unit + Integration + E2E

**Estimativa:** 2-3 semanas

---

### 🟢 COMPLEMENTAR (Depois)

#### 5. Feature 4: Dashboard & UI Polish
**Objetivos:**
- Homepage refatorada
- Dashboard do usuário
- Próximos eventos
- Histórico de partidas

**Estimativa:** 2 semanas

---

## 📅 Timeline Completa

```
Semana 1 (AGORA):
├─ Corrigir i18n E2E tests
├─ Validar Events/Matches/Players/Ranking E2E
└─ Branch: test-fixes-e2e

Semana 2-6 (Próximas 4-5 semanas):
├─ Feature 2: Users & RBAC
├─ JWT + Autenticação
├─ RBAC com roles
└─ Branch: feature-2-users-rbac

Semana 7-9:
├─ Feature 3: Grupos (Organizações)
├─ Isolamento de ranking
└─ Branch: feature-3-grupos

Semana 10-11:
├─ Feature 4: Dashboard
└─ Branch: feature-4-dashboard

Semana 12+:
├─ Testes finais
├─ Deploy em staging
└─ Documentação final
```

---

## 🎯 Recomendação

### ✅ COMECE COM: Corrigir E2E Tests (OPÇÃO A)

**Motivo:**
1. ⚡ Rápido (2-3 dias)
2. 🎯 Valida tudo que foi implementado
3. 🏗️ Estabelece base sólida
4. 🚀 Prepara para próximas features

**Passos:**
```bash
# 1. Criar branch para testes
git checkout -b test-fixes-e2e

# 2. Revisar erro de localStorage
cat frontend/e2e/i18n.spec.js

# 3. Refatorar para contornar sandbox
# Usar page.addInitScript() ao invés de acesso direto

# 4. Rodar testes
npm run test:e2e

# 5. Validar cobertura E2E completa
```

### 🚀 DEPOIS: Feature 2 (Autenticação)

Feature 2 (Users & RBAC) é **crítico** porque:
- Base para autorização em features futuras
- Necessário para isolamento de dados por grupo
- Pré-requisito para permissões granulares

**Passos:**
```bash
# 1. Criar branch
git checkout -b feature-2-users-rbac

# 2. Criar modelo User
# backend/models/user.py

# 3. Implementar autenticação JWT
# backend/routers/auth.py

# 4. Adicionar middleware
# backend/dependencies.py

# 5. RBAC com decoradores
# backend/routers/*.py
```

---

## 📚 Documentação de Referência

Para mais informações, consulte:

| Documento | Conteúdo |
|-----------|----------|
| `docs/PROXIMOS_PASSOS.md` | Detalhado com checklist técnico |
| `docs/features/REFINAMENTO_FEATURE_1.md` | Especificação Tournament Types (PRONTO) |
| `docs/tecnico/DIAGRAMAS_TECNICOS.md` | Arquitetura e ERD |
| `docs/GIT_COMMIT_GUIDE.md` | Como fazer commits |
| `README.md` | Overview do projeto |

---

## ✨ Checklist de Preparação

Antes de começar Feature 2:

- [ ] Testes E2E com localStorage 100% funcionando
- [ ] Especificação de User bem documentada
- [ ] JWT flow diagrama pronto
- [ ] Decidir bcrypt vs passlib para hash
- [ ] Setup de refresh token strategy

---

## 🔗 Próxima Ação

**Clique em um:**

1. **Corrigir E2E Tests** (Recomendado)
   ```bash
   git checkout -b test-fixes-e2e
   # Revisar frontend/e2e/i18n.spec.js
   ```

2. **Começar Feature 2** (Se preferir)
   ```bash
   git checkout -b feature-2-users-rbac
   # Planejar modelo User
   ```

3. **Revisar Documentação** (Se quiser se aprofundar)
   ```bash
   cat docs/PROXIMOS_PASSOS.md
   ```

---

**Status:** 🟢 Pronto para próxima fase  
**Data:** 20 de Novembro de 2025  
**Commit:** a8e1f45 ✅
