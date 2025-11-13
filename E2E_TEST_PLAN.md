# 🧪 E2E TESTS PLAN - Session 19 (Test Fixes)

**Data:** 20 de Novembro de 2025  
**Branch:** test-fixes-e2e  
**Objetivo:** Corrigir localStorage issues e validar todos E2E tests em 2 ambientes  

---

## 📊 Status Atual

### ✅ Testes Passando (45/45)
- Unit Tests: 17/17 ✅
- Integration Tests: 14/14 ✅
- E2E Tests: 14/14 ✅ (Tournament, mas outros não validados)

### ⏳ Testes Pendentes/Com Issues
- **i18n E2E (22 testes):** localStorage SecurityError
- **Events E2E (4 testes):** Não validados
- **Matches E2E:** Não validados
- **Players E2E:** Não validados
- **Ranking E2E:** Não validados

---

## 🎯 Estratégia de Testes

### Ambiente 1: Localhost
- **URL:** `http://localhost:5173`
- **Status:** Local development server
- **Teste:** Validação rápida, debugging

### Ambiente 2: ngrok (Produção simulada)
- **URL:** `https://unserialised-sherie-convocational.ngrok-free.dev/`
- **Status:** Public URL via ngrok
- **Teste:** Validação de funcionalidade em produção

---

## 📋 Testes a Executar

### 1. Testes i18n com localStorage (FIX)
**Problema:** SecurityError ao acessar localStorage em sandbox Playwright
**Solução:** Usar `page.addInitScript()` ao invés de acesso direto

**Testes:**
```
frontend/e2e/i18n.spec.js
├─ Language detection
├─ Language switching
├─ Translations loading
└─ localStorage persistence (REFATORADO)
```

### 2. Testes de Eventos
**Arquivo:** `frontend/e2e/events.spec.js`

**Testes:**
```
├─ List events
├─ Create event
├─ Edit event
└─ Delete event
```

### 3. Testes de Matches
**Arquivo:** `frontend/e2e/matches.spec.js`

**Testes:**
```
├─ List matches
├─ Create match
├─ Record result
└─ Update match
```

### 4. Testes de Players
**Arquivo:** `frontend/e2e/players.spec.js`

**Testes:**
```
├─ List players
├─ Add player to event
├─ Update player
└─ Remove player
```

### 5. Testes de Ranking
**Arquivo:** `frontend/e2e/ranking.spec.js`

**Testes:**
```
├─ View rankings
├─ ELO calculations
├─ Ranking updates
└─ Membership ranking
```

### 6. Testes de Tournament (Validação)
**Arquivo:** `frontend/e2e/tournaments.spec.js`

**Testes:** (Já passando, apenas validação)
```
├─ Create tournament
├─ Generate bracket
├─ Advance rounds
└─ Complete tournament
```

---

## 🔧 Processo de Teste

### Fase 1: Ficar localStorage Issue (1 dia)
1. [ ] Revisar `frontend/e2e/i18n.spec.js`
2. [ ] Identificar todas as chamadas diretas de localStorage
3. [ ] Refatorar para usar `page.addInitScript()`
4. [ ] Testar em localhost
5. [ ] Testar em ngrok

### Fase 2: Validar Todos E2E Tests em Localhost (0.5 dias)
1. [ ] Events tests
2. [ ] Matches tests
3. [ ] Players tests
4. [ ] Ranking tests
5. [ ] Tournaments tests (validação)

### Fase 3: Validar Todos E2E Tests em ngrok (0.5 dias)
1. [ ] Events tests
2. [ ] Matches tests
3. [ ] Players tests
4. [ ] Ranking tests
5. [ ] Tournaments tests (validação)

### Fase 4: Relatório e Commit (0.5 dias)
1. [ ] Documentar resultados
2. [ ] Corrigir bugs encontrados
3. [ ] Fazer commit com resultados

---

## 🛠️ Ferramentas

### Playwright MCP
- Usar `mcp_microsoft_pla_browser_*` para interações com UI
- Vantagem: Captura de screenshots, console logs, snapshots
- Procedimento: Navigate → Wait → Snapshot → Interact → Verify

### URLs de Teste
- **Localhost:** `http://localhost:5173`
- **ngrok:** `https://unserialised-sherie-convocational.ngrok-free.dev/`

---

## 📝 Checklist de Execução

### Preparação
- [ ] Branch criada: `test-fixes-e2e`
- [ ] Backend rodando (porta 8000)
- [ ] Frontend rodando (porta 5173)
- [ ] ngrok rodando (se disponível)

### Fase 1: localStorage Fix
- [ ] Diagnosticar erro em i18n.spec.js
- [ ] Refatorar testes
- [ ] Validar em localhost
- [ ] Validar em ngrok

### Fase 2: Testes Localhost
- [ ] i18n (22 testes)
- [ ] Events (4 testes)
- [ ] Matches tests
- [ ] Players tests
- [ ] Ranking tests
- [ ] Tournaments (14 testes)

### Fase 3: Testes ngrok
- [ ] i18n (22 testes)
- [ ] Events (4 testes)
- [ ] Matches tests
- [ ] Players tests
- [ ] Ranking tests
- [ ] Tournaments (14 testes)

### Fase 4: Finalização
- [ ] Documentação de resultados
- [ ] Commit com fixos
- [ ] Merge para main

---

## 📊 Métrica de Sucesso

**Objetivo:** 100% de testes E2E passando em ambos os ambientes

```
Esperado:
├─ i18n: 22/22 ✅
├─ Events: 4/4 ✅
├─ Matches: N/N ✅
├─ Players: N/N ✅
├─ Ranking: N/N ✅
└─ Tournaments: 14/14 ✅
   ────────────────────
   TOTAL: 70+/70+ ✅ (100%)
```

---

## 🎯 Próximos Passos

1. Corrigir localStorage issue em i18n tests
2. Rodar todos os E2E tests em localhost com Playwright MCP
3. Rodar todos os E2E tests em ngrok com Playwright MCP
4. Documentar resultados
5. Fazer commit

**Estimativa:** 2-3 dias

---

**Status:** 🟡 Em Progresso  
**Branch:** test-fixes-e2e  
**Criado:** 20 de Novembro de 2025
