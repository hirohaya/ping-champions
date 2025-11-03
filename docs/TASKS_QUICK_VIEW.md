# Mapa Rápido de Tarefas — Ping Champions

## Status Dashboard

| ID | Título | Prioridade | Sprint | Esforço | Status | Bloqueadores |
|----|--------|-----------|--------|---------|--------|--------------|
| T001 | Corrigir SFC em EventsView.vue | P0 | 1 | 15m | ⬜ Não iniciada | — |
| T002 | Remover serviços redundantes | P1 | 1 | 15m | ⬜ Não iniciada | — |
| T003 | Corrigir ORM Event-Player | P0 | 1 | 10m | ⬜ Não iniciada | — |
| T004 | Standardizar trailing slashes | P1 | 1 | 20m | ⬜ Não iniciada | — |
| T005 | Unificar delete strategy | P2 | 1 | 30m | ⬜ Não iniciada | — |
| T006 | Schemas Pydantic: Events | P1 | 2 | 1h | ⬜ Não iniciada | T004 |
| T007 | Schemas Pydantic: Players | P1 | 2 | 1h | ⬜ Não iniciada | T006 |
| T008 | Schemas Pydantic: Matches | P1 | 2 | 1h | ⬜ Não iniciada | T006 |
| T009 | Adicionar GET /events/{id} | P1 | 2 | 30m | ⬜ Não iniciada | T006 |
| T010 | Config via .env | P2 | 3 | 45m | ⬜ Não iniciada | — |
| T011 | Setup Alembic | P2 | 3 | 1h | ⬜ Não iniciada | — |
| T012 | Ruff + Black | P2 | 3 | 45m | ⬜ Não iniciada | — |
| T013 | ESLint + Prettier | P2 | 3 | 45m | ⬜ Não iniciada | — |
| T014 | Pytest testes | P2 | 3 | 2h | ⬜ Não iniciada | T006, T007 |
| T015 | Vitest testes | P3 | 3 | 1.5h | ⬜ Não iniciada | T001 |
| T016 | docs/ENDPOINTS.md | P1 | 4 | 1h | ⬜ Não iniciada | T006-009 |
| T017 | docs/ARCHITECTURE.md | P2 | 4 | 45m | ⬜ Não iniciada | — |
| T018 | Atualizar READMEs | P1 | 4 | 45m | ⬜ Não iniciada | T010,012,013,014 |
| T019 | docs/CONTRIBUTING.md | P3 | 4 | 30m | ⬜ Não iniciada | — |
| T020 | Camada de serviços | P1 | 5 | 2-3h | ⬜ Não iniciada | T006, T014 |
| T021 | Scoring/Ranking | P1 | 5 | 1.5h | ⬜ Não iniciada | T020 |
| T022 | JWT Auth | P3 | 6 | 2-3h | ⬜ Não iniciada | T010 |
| T023 | Paginação | P2 | 6 | 1.5h | ⬜ Não iniciada | T006 |
| T024 | CI/CD | P2 | 6 | 1h | ⬜ Não iniciada | T012-015 |

---

## Por Sprint

### Sprint 1 — Quick Wins (1–2 dias | Esforço total: ~1.5 horas)
- **T001**: Corrigir SFC em EventsView.vue (15m)
- **T002**: Remover serviços redundantes (15m)
- **T003**: Corrigir ORM Event-Player (10m)
- **T004**: Standardizar trailing slashes (20m)
- **T005**: Unificar delete strategy (30m)

**Saída esperada**: código limpo, sem erros de build, API consistente.

---

### Sprint 2 — Contratos & Validação (2–3 dias | Esforço total: ~4 horas)
- **T006**: Schemas Pydantic: Events (1h) — bloqueador de T007, T008, T009, T016, T020
- **T007**: Schemas Pydantic: Players (1h) — bloqueado por T006
- **T008**: Schemas Pydantic: Matches (1h) — bloqueado por T006
- **T009**: Adicionar GET /events/{id} (30m) — bloqueado por T006

**Saída esperada**: API com contratos estáveis, validações Pydantic, Swagger documentado.

---

### Sprint 3 — Ferramentas & Testes (2–3 dias | Esforço total: ~7 horas)

**Independentes (fazer em paralelo)**:
- **T010**: Config via .env (45m)
- **T011**: Setup Alembic (1h)
- **T012**: Ruff + Black (45m) → bloqueador de T014, T024
- **T013**: ESLint + Prettier (45m) → bloqueador de T015, T024

**Bloqueados**:
- **T014**: Pytest testes (2h) — bloqueado por T006, T007 → bloqueador de T020, T024
- **T015**: Vitest testes (1.5h) — bloqueado por T001 → bloqueador de T024

**Saída esperada**: linting automático, testes unitários, migrações de banco, ambiente configurável.

---

### Sprint 4 — Documentação (1–2 dias | Esforço total: ~3 horas)
- **T016**: docs/ENDPOINTS.md (1h) — bloqueado por T006-009
- **T017**: docs/ARCHITECTURE.md (45m) — independente
- **T018**: Atualizar READMEs (45m) — bloqueado por T010, T012, T013, T014
- **T019**: docs/CONTRIBUTING.md (30m) — independente

**Saída esperada**: onboarding simplificado, documentação de contratos, guia de contribuição.

---

### Sprint 5 — Domínio & Negócio (1–2 semanas | Esforço total: ~4-5 horas)
- **T020**: Camada de serviços (2-3h) — bloqueado por T006, T014 → bloqueador de T021
- **T021**: Scoring/Ranking (1.5h) — bloqueado por T020

**Saída esperada**: lógica de negócio encapsulada, pontuação e ranking funcionais.

---

### Sprint 6+ — Crescimento (Futuro)
- **T022**: JWT Auth (2-3h) — bloqueado por T010
- **T023**: Paginação (1.5h) — bloqueado por T006
- **T024**: CI/CD (1h) — bloqueado por T012-015

**Saída esperada**: autenticação, escalabilidade, automação.

---

## Recomendação de priorização

### Para a primeira semana (Sprint 1 + 2):
1. Fazer **Sprint 1** (1-2 dias): remove bloqueadores críticos.
2. Fazer **Sprint 2** (2-3 dias): estabiliza contratos de API.
3. Validar: `npm run build`, `uvicorn main:app --reload`, swagger em `/docs`.

### Para a segunda semana (Sprint 3):
1. Fazer tarefas de infra em paralelo: T010, T011, T012, T013 (1-2 dias).
2. Fazer T014, T015 (testes) após schemas (bloqueadores resolvidos).
3. Validar: `pytest backend/tests/ -v`, `npm run test`, `ruff check`, lint passa.

### Para a terceira semana (Sprint 4):
1. Fazer **Sprint 4** (1-2 dias): documentação (baixo risco, alto valor de DX).
2. Pronto para onboarding de novos devs.

### Futuro (Sprint 5+):
1. Priorizar T020 e T021 (regras de negócio) conforme roadmap.
2. Adicionar autenticação, paginação, CI/CD conforme necessário.

---

## Quick Links

- **Detalhes completos**: veja `docs/TASKS.md`
- **Architecture Review**: veja `ARCHITECTURE_REVIEW.md`
- **Endpoints (em progresso)**: veja `docs/ENDPOINTS.md` (após T016)

---

**Status geral**: 🔴 Não iniciado | Recomendação: começar Sprint 1 hoje.
