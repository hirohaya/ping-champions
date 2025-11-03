# 🚀 Action Plan — Próximas 4 Semanas

## Semana 1: Sprint 1 — Quick Wins (1-2 dias | P0/P1)

**Objetivo**: Remover bloqueadores críticos de build e API.

### Segunda-feira (hoje)
- [ ] **T001** (15m, P0, Backend): Corrigir SFC em `EventsView.vue`
  - Ação: Mover CSS para `<style scoped>` no final do arquivo.
  - Validação: `npm run build` sem erros.

- [ ] **T003** (10m, P0, Backend): Corrigir ORM em `models/player.py`
  - Ação: Remover reatribuição de `Event.players`.
  - Validação: Sem warnings em imports.

### Terça-feira
- [ ] **T004** (20m, P1, Backend): Standardizar trailing slashes
  - Ação: Remover `/` final de todas as rotas FastAPI.
  - Ação: Atualizar `frontend/src/services/` para bater.
  - Validação: `POST /events/create` sem 307 redirect.

- [ ] **T002** (15m, P1, Frontend): Remover serviços redundantes
  - Ação: Deletar `jogadores.js`; decidir `jogos.js`.
  - Validação: Nenhum import quebrado; `npm run dev` sem errors.

### Quarta-feira (meia manhã)
- [ ] **T005** (30m, P2, Backend): Decidir delete strategy (soft vs hard)
  - Ação: Documento `docs/DELETE_STRATEGY.md` com decisão.
  - Ação: Alinhar modelos e rotas.
  - Validação: Todos os deletes comportam-se consistentemente.

**Saída da Semana 1**: ✅ Build limpo, API consistente, código sem erros críticos.

---

## Semana 2: Sprint 2 — Contratos & Validação (2-3 dias | P1)

**Objetivo**: Estabilizar API com schemas Pydantic.

### Segunda-feira
- [ ] **T006** (1h, P1, Backend): Criar schemas para Events
  - Ação: `backend/schemas.py` com `EventCreate`, `EventRead`, `EventUpdate`.
  - Ação: Validação de data (YYYY-MM-DD) via Pydantic.
  - Ação: Atualizar `backend/routers/events.py`.
  - Validação: Swagger em `/docs` exibe schemas.

### Terça-feira (paralelo)
- [ ] **T007** (1h, P1, Backend): Criar schemas para Players
  - Ação: `EventCreate`, `EventRead`, `EventUpdate` em `schemas.py`.
  - Ação: Atualizar `routers/players.py` para usar body JSON.
  - Validação: `POST /players` aceita body JSON; testes passam.

- [ ] **T008** (1h, P1, Backend): Criar schemas para Matches
  - Ação: `MatchCreate`, `MatchRead`, `MatchUpdate` em `schemas.py`.
  - Ação: Validação: `player1_id ≠ player2_id`; winner é um dos dois.
  - Validação: Swagger completo.

### Quarta-feira
- [ ] **T009** (30m, P1, Backend): Adicionar `GET /events/{id}`
  - Ação: Nova rota retorna `EventRead`.
  - Ação: Atualizar `Breadcrumbs.vue` para usar novo endpoint.
  - Validação: Sem overfetch; breadcrumb funciona.

**Saída da Semana 2**: ✅ API estável com contratos Pydantic, swagger documentado, frontend integrado.

---

## Semana 3: Sprint 3 — Infra & Testes (2-3 dias | P2)

**Objetivo**: Setup de qualidade, linting, testes, migrações.

### Segunda-feira (paralelo: 4 devs / 2 pares idealmente)
- [ ] **T010** (45m, P2, Backend): Config via `.env`
  - Ação: Criar `.env.example` e `.gitignore`.
  - Ação: Atualizar `database.py` e `main.py` para ler env.
  - Validação: `CORS_ORIGINS` configurable.

- [ ] **T011** (1h, P2, Backend): Setup Alembic
  - Ação: `alembic init migrations`.
  - Ação: Gerar primeira migração.
  - Ação: Atualizar README.

- [ ] **T012** (45m, P2, Backend): Ruff + Black
  - Ação: Instalar; criar `pyproject.toml`.
  - Ação: `ruff check . && black .`.
  - Validação: 0 erros.

- [ ] **T013** (45m, P2, Frontend): ESLint + Prettier
  - Ação: Instalar; criar `.eslintrc.json` + `.prettierrc.json`.
  - Ação: `npm run lint && npm run format`.
  - Validação: 0 erros.

### Terça-feira (após T006, T007)
- [ ] **T014** (2h, P2, Backend): Pytest testes
  - Ação: `tests/conftest.py`, `tests/test_events.py`, `tests/test_players.py`.
  - Ação: Cobertura: create, list, delete, 404, validação.
  - Validação: `pytest tests/ -v` → todos passam.

### Quarta-feira (após T001)
- [ ] **T015** (1.5h, P3, Frontend): Vitest testes
  - Ação: Mocks de axios; testes de services.
  - Ação: `npm run test` → todos passam.
  - Validação: Cobertura de eventsService, playersService.

**Saída da Semana 3**: ✅ Linting automático, testes funcionando, migrações de banco, `.env` configurável.

---

## Semana 4: Sprint 4 — Documentação (1-2 dias | P1-P2)

**Objetivo**: Documentação e DX para onboarding.

### Segunda-feira
- [ ] **T016** (1h, P1, Backend): `docs/ENDPOINTS.md`
  - Ação: Tabela com todos os endpoints, métodos, exemplos, cURL.
  - Ação: Aprox. 15-20 endpoints documentados.
  - Validação: Legível e testável via exemplos.

### Terça-feira
- [ ] **T017** (45m, P2, Backend): `docs/ARCHITECTURE.md`
  - Ação: ERD simples (ASCII/Mermaid), fluxo de dados, camadas.
  - Validação: Novo dev consegue entender estrutura em 5 min.

- [ ] **T018** (45m, P1, Backend+Frontend): Atualizar READMEs
  - Ação: Adicionar scripts + checklist em ambos os READMEs.
  - Ação: Mencionar `.env`, migrações, lint, testes.
  - Validação: Setup completo em <15 min.

- [ ] **T019** (30m, P3, Backend): `docs/CONTRIBUTING.md`
  - Ação: Fluxo de branch, padrões de código, commits, PRs.
  - Validação: Claro e seguível.

**Saída da Semana 4**: ✅ Documentação completa, onboarding de novos devs facilitado, contratos de API documentados.

---

## Após 4 Semanas: Status Esperado

```
✅ Build: Verd (npm run build, uvicorn main:app)
✅ Lint: Verde (ruff, black, eslint, prettier)
✅ Testes: Verde (pytest, vitest)
✅ API: Documentada e estável (Swagger, ENDPOINTS.md)
✅ Config: Flexível (.env, sem hardcodes)
✅ Onboarding: Fácil (READMEs, docs/, setup <15 min)
✅ Banco: Migrações (Alembic)

Pronto para: Sprint 5 (Camada de serviços + Pontuação/Ranking)
```

---

## Semana 5+: Sprint 5 — Domínio & Negócio

### T020 (2-3h): Camada de serviços
- Backend: `services/events.py`, `services/players.py`, `services/matches.py`
- Rotas delegam para serviços
- Testes de serviços com transações

### T021 (1.5h): Scoring & Ranking
- `MatchService.finish_match()` atualiza score
- `GET /ranking?event_id=X` ordena por score
- Testes end-to-end

---

## Checklist de Decisão (antes de começar)

Responda estas perguntas **antes de começar Sprint 1**:

- [ ] **Delete Strategy** (T005): soft delete (marcar inativo) ou hard delete (remover)?
  - _Decisão_: ___________
  
- [ ] **Versionamento de API** (futuro): começar com `/api/v1` agora ou depois?
  - _Recomendação_: depois (Sprint 5+)
  - _Decisão_: ___________

- [ ] **Autenticação** (T022): JWT simples ou Auth0/serviço externo?
  - _Recomendação_: JWT simples (Sprint 6)
  - _Decisão_: ___________

- [ ] **Observabilidade** (futuro): logging/métricas desde agora ou depois?
  - _Recomendação_: depois (Sprint 5+, básico)
  - _Decisão_: ___________

- [ ] **Equipe disponível**: Quantos devs para Sprint 1–4?
  - _Sugestão_: 1–2 devs (serial) ou 2–3 devs (paralelo em Sprint 3)
  - _Decisão_: ___________

---

## Comunicação & Status

### Diariamente
- [ ] Standup breve: T### em progresso, bloqueadores.
- [ ] Usar labels do GitHub (status/in-progress, status/blocked).

### Semanalmente
- [ ] Revisar progresso em `docs/TASKS_QUICK_VIEW.md`.
- [ ] Atualizar status de tasks concluídas.
- [ ] Reajustar Sprint se necessário (é normal).

### Ao final de cada Sprint
- [ ] Review técnico (code + testes).
- [ ] Retro: o que funcionou, o que pode melhorar.
- [ ] Decida: prosseguir com próximo sprint ou ajustar prioridades?

---

## Links Rápidos

- **Detalhes das tarefas**: `docs/TASKS.md`
- **Dashboard**: `docs/TASKS_QUICK_VIEW.md`
- **Resumo executivo**: `docs/README_ASSESSMENT.md`
- **Setup do GitHub**: `docs/GITHUB_ISSUE_TEMPLATES.md`
- **Índice completo**: `docs/INDEX.md`

---

## TL;DR — Se tiver apenas 5 min

1. Leia `docs/README_ASSESSMENT.md`.
2. Veja `docs/TASKS_QUICK_VIEW.md` (tabela + cronograma).
3. Comece **hoje com Sprint 1**: T001, T002, T003, T004, T005 (total ~1.5h).
4. Próxima semana: Sprint 2 schemas (~4h).
5. Semana 3: infra + testes (em paralelo, ~7h).
6. Semana 4: docs (~3h).
7. **Resultado**: projeto pronto para crescer com confiança. ✅

---

**Boa sorte!** 🚀

**Data**: 2025-11-02  
**Status**: Pronto para ação  
**Próximo passo**: Abrir primeira issue (T001) no GitHub.
