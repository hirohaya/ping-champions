# 🧪 E2E TESTS COM PLAYWRIGHT MCP - Execução

**Data:** 20 de Novembro de 2025  
**Branch:** test-fixes-e2e  
**Objetivo:** Testar em http://localhost:5173 e https://unserialised-sherie-convocational.ngrok-free.dev/

---

## 📋 Cronograma de Testes

### ✅ Fase 1: Correção de localStorage (PRONTO)
- [x] Corrigido i18n.spec.js
- [x] Mudado porta de 5174 para 5173
- [x] Refatorado para usar addInitScript() ao invés de page.evaluate()

### ⏳ Fase 2: Testes com Playwright MCP (AGORA)

---

## 🎯 Testes a Executar com Playwright MCP

### Teste 1: Validação básica em localhost (http://localhost:5173)

**Objetivo:** Verificar se a aplicação carrega corretamente

```
1. Navigate to http://localhost:5173/
2. Wait for page load
3. Take snapshot
4. Verify main page elements (h1, selects, etc)
5. Take screenshot
```

### Teste 2: Verificar i18n localStorage fix

**Objetivo:** Confirmar que localStorage agora funciona sem SecurityError

```
1. Navigate to http://localhost:5173/
2. Switch language to Portuguese (pt-BR)
3. Refresh page
4. Verify language persisted
5. Verify console has no localStorage errors
```

### Teste 3: Events E2E (4 testes)

**Objetivo:** Validar funcionalidade de eventos

```
frontend/e2e/events.spec.js
├─ List events
├─ Create event
├─ Edit event
└─ Delete event
```

### Teste 4: Matches E2E

**Objetivo:** Validar funcionalidade de partidas

```
frontend/e2e/matches.spec.js
├─ List matches
├─ Create match
├─ Record result
└─ Update match
```

### Teste 5: Players E2E

**Objetivo:** Validar funcionalidade de jogadores

```
frontend/e2e/players.spec.js
├─ List players
├─ Add player to event
├─ Update player
└─ Remove player
```

### Teste 6: Ranking E2E

**Objetivo:** Validar funcionalidade de ranking

```
frontend/e2e/ranking.spec.js
├─ View rankings
├─ ELO calculations
├─ Ranking updates
└─ Membership ranking
```

### Teste 7: Tournaments E2E (Validação)

**Objetivo:** Confirmar Sprint 3 ainda funciona

```
frontend/e2e/tournaments.spec.js
├─ Create tournament
├─ Generate bracket
├─ Advance rounds
└─ Complete tournament
```

### Teste 8: Testes em ngrok URL

**Objetivo:** Validar em ambiente de produção simulado

```
Repetir todos os testes acima usando:
https://unserialised-sherie-convocational.ngrok-free.dev/

Garantir que:
- UI funciona via ngrok
- API funciona via ngrok
- localStorage funciona via ngrok (HTTPS)
- Performance é aceitável
```

---

## 🛠️ Usando Playwright MCP

### Padrão de Teste com MCP

```
1. mcp_microsoft_pla_browser_navigate(url)
   └─ Ir para a URL

2. mcp_microsoft_pla_browser_wait_for(time)
   └─ Esperar carregamento

3. mcp_microsoft_pla_browser_snapshot()
   └─ Tirar snapshot (acessibilidade)

4. mcp_microsoft_pla_browser_take_screenshot()
   └─ Tirar screenshot visual

5. mcp_microsoft_pla_browser_click(element, ref)
   └─ Clicar em elemento

6. mcp_microsoft_pla_browser_fill_form(fields)
   └─ Preencher formulário

7. mcp_microsoft_pla_browser_select_option(element, ref, values)
   └─ Selecionar opção

8. mcp_microsoft_pla_browser_wait_for(text)
   └─ Esperar texto aparecer
```

---

## 📊 Checklist de Execução

### Preparação
- [ ] Backend rodando (porta 8000)
- [ ] Frontend rodando (porta 5173)
- [ ] ngrok rodando (se testando na URL ngrok)
- [ ] i18n.spec.js corrigido ✅

### Testes Localhost (http://localhost:5173)
- [ ] Validação básica de carregamento
- [ ] localStorage fix em i18n
- [ ] Events (4 testes)
- [ ] Matches
- [ ] Players
- [ ] Ranking
- [ ] Tournaments (14 testes)

### Testes ngrok (https://unserialised-sherie-convocational.ngrok-free.dev/)
- [ ] Validação básica de carregamento
- [ ] localStorage fix em i18n
- [ ] Events (4 testes)
- [ ] Matches
- [ ] Players
- [ ] Ranking
- [ ] Tournaments (14 testes)

### Finalização
- [ ] Documentar resultados
- [ ] Corrigir bugs encontrados
- [ ] Fazer commit

---

## 📝 Template para Relatório de Testes

```markdown
# Relatório de E2E Tests - Session 19

## Ambiente: Localhost (http://localhost:5173)

### Testes Passando
- i18n: X/22 ✅
- Events: X/4 ✅
- Matches: X/X ✅
- Players: X/X ✅
- Ranking: X/X ✅
- Tournaments: 14/14 ✅

**Total Localhost:** X/70+ ✅

## Ambiente: ngrok (https://unserialised-sherie-convocational.ngrok-free.dev/)

### Testes Passando
- i18n: X/22 ✅
- Events: X/4 ✅
- Matches: X/X ✅
- Players: X/X ✅
- Ranking: X/X ✅
- Tournaments: 14/14 ✅

**Total ngrok:** X/70+ ✅

## Conclusão
[Status dos testes]
[Bugs encontrados]
[Próximos passos]
```

---

## 🚀 Próximos Passos

1. [x] Corrigir localStorage issue em i18n.spec.js
2. [ ] Testar com Playwright MCP em localhost
3. [ ] Testar com Playwright MCP em ngrok
4. [ ] Documentar resultados
5. [ ] Fazer commit

---

**Status:** 🟡 Fase 2 em progresso  
**Branch:** test-fixes-e2e  
**Próxima Ação:** Começar testes com Playwright MCP
