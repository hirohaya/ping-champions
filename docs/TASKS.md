# Tarefas e Issues Priorizadas — Ping Champions

## Sobre este documento

Este é um tracker de tarefas priorizadas com base na avaliação de arquitetura. Cada tarefa inclui:
- **ID**: referência única (T001, T002, etc.)
- **Prioridade**: P0 (crítico), P1 (alta), P2 (média), P3 (baixa)
- **Sprint**: semana/intervalo sugerido
- **Escopo**: descrição concisa
- **Critérios de aceite**: definição objetiva de "pronto"
- **Dependências**: tarefas que devem ser feitas antes

---

## Sprint 1 — Quick Wins (1–2 dias)

Correções de risco alto e baixo esforço que desbloqueiam sprints posteriores.

### T001: Corrigir SFC inválido em EventsView.vue
**Prioridade**: P0 (build está em risco)  
**Sprint**: 1 (hoje)  
**Escopo**:
- Mover CSS fora de `<style>` para um bloco `<style scoped>` válido no final do componente.
- Remover trechos Python ou código morto não pertencente a Vue.

**Critérios de aceite**:
- [ ] `npm run build` roda sem erros ou avisos de SFC.
- [ ] `npm run dev` carrega a página de eventos sem console errors.
- [ ] Componente exibe corretamente com estilos aplicados.

**Arquivo**: `frontend/src/views/EventsView.vue`

**Esforço**: 15 min  
**Dependências**: nenhuma

---

### T002: Remover serviços redundantes
**Prioridade**: P1 (limpeza de código)  
**Sprint**: 1  
**Escopo**:
- Deletar `frontend/src/services/jogadores.js` (arquivo vazio).
- Decidir: manter ou remover `frontend/src/services/jogos.js` (stub).
  - Se remover: atualizar imports em `views/` que referenciam jogos.
  - Se manter: adicionar comentário que será implementado quando backend de matches ficar pronto.

**Critérios de aceite**:
- [ ] `jogadores.js` removido.
- [ ] `jogos.js` tem status claro (comentário tipo `// TODO: Implement when matches backend is ready`).
- [ ] Nenhum arquivo frontend importa `jogadores.js`.
- [ ] Não há erros de import em `npm run dev`.

**Arquivos afetados**:
- `frontend/src/services/jogadores.js` (remover)
- `frontend/src/services/jogos.js` (decidir)
- `frontend/src/views/HomeView.vue` (usa `jogosService`)

**Esforço**: 15 min  
**Dependências**: nenhuma

---

### T003: Corrigir relacionamento Event-Player (ORM)
**Prioridade**: P0 (bug de cascata)  
**Sprint**: 1  
**Escopo**:
- Em `backend/models/player.py`, remover a linha que reatribui `Event.players = relationship(...)`.
- Manter a definição única em `backend/models/event.py` com `cascade="all, delete-orphan"`.
- Verificar que `Player.event` tem `back_populates="event"`.

**Critérios de aceite**:
- [ ] `backend/models/player.py` não contém reatribuição de `Event.players`.
- [ ] `Player.event` tem `back_populates="event"`.
- [ ] `Event.players` ainda tem `cascade="all, delete-orphan"` em `event.py`.
- [ ] Teste manual: deletar um evento no banco remove seus jogadores (se implementado hard delete) ou marca como inativo (se soft delete).

**Arquivo**: `backend/models/player.py`, `backend/models/event.py`

**Esforço**: 10 min  
**Dependências**: nenhuma

---

### T004: Standardizar trailing slashes e métodos HTTP
**Prioridade**: P1 (consistência de API)  
**Sprint**: 1  
**Escopo**:
- Backend: remover trailing slashes das rotas. Ex.: `POST /events/create/` → `POST /events/create`.
- Verificar que todos os endpoints usam barra inicial: `/events`, `/players`, etc.
- Frontend: atualizar `src/services/*.js` para bater com as rotas (sem slash final).

**Critérios de aceite**:
- [ ] Todas as rotas em `backend/routers/` não têm barra final.
- [ ] `frontend/src/services/events.js` chama `/events`, `/events/create` (sem `/`).
- [ ] `npm run dev` + backend rodando sem erros HTTP 307 (redirect).
- [ ] Postman/curl: `POST http://localhost:8000/events/create` (sem /) retorna 201/200 sem redirect.

**Arquivos afetados**:
- `backend/routers/events.py`
- `backend/routers/players.py`
- `backend/routers/matches.py`
- `backend/routers/ranking.py`
- `frontend/src/services/events.js`
- `frontend/src/services/players.js`

**Esforço**: 20 min  
**Dependências**: nenhuma

---

### T005: Unificar estratégia de soft/hard delete
**Prioridade**: P2 (consistência, não urgente)  
**Sprint**: 1  
**Escopo**:
- Decidir: soft delete (marcar inativo) ou hard delete (remover do banco)?
- Aplicar uniformemente em Events, Players, Matches.
- Atualizar rotas e modelos conforme.

**Critérios de aceite**:
- [ ] Documento `docs/DELETE_STRATEGY.md` explica a decisão.
- [ ] Todos os modelos usam a mesma estratégia (soft ou hard).
- [ ] Testes: `DELETE /players/{id}` e `DELETE /events/{id}` comportam-se de forma consistente.

**Arquivos**: `backend/models/`, `backend/routers/`

**Esforço**: 30 min  
**Dependências**: nenhuma (preparatória)

---

## Sprint 2 — Camada de Contrato e Validação (2–3 dias)

Estabelecer contratos de API estáveis e validações via Pydantic.

### T006: Criar schemas Pydantic para Events
**Prioridade**: P1 (base para API estável)  
**Sprint**: 2  
**Escopo**:
- Criar `backend/schemas.py` (ou `backend/schemas/events.py`).
- Definir:
  - `EventCreate` (name: str, date: str, time: str, com validação).
  - `EventRead` (id, name, date, time, active, created_at).
  - `EventUpdate` (opcionalmente: name, time).
- Mover validação de data para o schema (validador Pydantic).
- Atualizar `backend/routers/events.py` para usar schemas.

**Critérios de aceite**:
- [ ] `backend/schemas.py` contém `EventCreate`, `EventRead`, `EventUpdate`.
- [ ] Schema `EventCreate.date` valida formato YYYY-MM-DD (ex.: "2025-11-02") e rejeita inválidos com mensagem clara.
- [ ] Rota `POST /events/create` aceita body JSON com schema `EventCreate` e retorna `EventRead`.
- [ ] `GET /events` retorna `list[EventRead]`.
- [ ] Swagger em `/docs` exibe schemas corretamente.

**Arquivo**: `backend/schemas.py`, `backend/routers/events.py`

**Esforço**: 1 hora  
**Dependências**: T004

---

### T007: Criar schemas Pydantic para Players
**Prioridade**: P1  
**Sprint**: 2  
**Escopo**:
- Adicionar a `backend/schemas.py`:
  - `PlayerCreate` (name: str, event_id: int).
  - `PlayerUpdate` (name: str).
  - `PlayerRead` (id, name, event_id, score, ranking, active).
- Validar: `name` não vazio, `event_id` existe.
- Atualizar `backend/routers/players.py` para usar schemas (body JSON, não query params).

**Critérios de aceite**:
- [ ] `POST /players` aceita body `{ "name": "João", "event_id": 1 }` e retorna `PlayerRead`.
- [ ] `PUT /players/{id}` aceita body `{ "name": "João Silva" }`.
- [ ] `GET /players?event_id=1` retorna `list[PlayerRead]`.
- [ ] Request sem `event_id` ou nome vazio retorna 400 com mensagem de validação clara.
- [ ] Swagger exibe os schemas e exemplos.

**Arquivo**: `backend/schemas.py`, `backend/routers/players.py`

**Esforço**: 1 hora  
**Dependências**: T006

---

### T008: Criar schemas Pydantic para Matches
**Prioridade**: P1  
**Sprint**: 2  
**Escopo**:
- Adicionar a `backend/schemas.py`:
  - `MatchCreate` (event_id, player1_id, player2_id, best_of: int = 5).
  - `MatchUpdate` (winner_id: int | None, finished: bool).
  - `MatchRead` (id, event_id, player1_id, player2_id, winner_id, best_of, finished).
- Validar: player1_id ≠ player2_id, ambos existem, winner_id (se presente) é um dos dois jogadores.
- Atualizar `backend/routers/matches.py`.

**Critérios de aceite**:
- [ ] `POST /matches` aceita body `{ "event_id": 1, "player1_id": 1, "player2_id": 2, "best_of": 5 }` e retorna `MatchRead`.
- [ ] Validação: player1_id ≠ player2_id (erro 400 se iguais).
- [ ] Validação: winner_id deve ser player1_id ou player2_id (erro 400 se inválido).
- [ ] `PUT /matches/{id}` aceita `{ "winner_id": 1, "finished": true }`.
- [ ] `GET /matches?event_id=1` retorna `list[MatchRead]`.

**Arquivo**: `backend/schemas.py`, `backend/routers/matches.py`

**Esforço**: 1 hora  
**Dependências**: T006

---

### T009: Adicionar endpoint GET /events/{id}
**Prioridade**: P1  
**Sprint**: 2  
**Escopo**:
- Adicionar rota `GET /events/{id}` que retorna um único `EventRead`.
- Atualizar `frontend/src/components/Breadcrumbs.vue` para usar `GET /events/{id}` em vez de buscar a lista inteira.

**Critérios de aceite**:
- [ ] `GET /events/1` retorna `{ "id": 1, "name": "...", "date": "...", "time": "...", "active": true }` com status 200.
- [ ] `GET /events/99999` retorna 404.
- [ ] `Breadcrumbs.vue` chama `GET /events/{id}` (não mais a lista).
- [ ] Breadcrumb exibe nome do evento sem overfetch.

**Arquivo**: `backend/routers/events.py`, `frontend/src/components/Breadcrumbs.vue`

**Esforço**: 30 min  
**Dependências**: T006

---

## Sprint 3 — Configuração e Ferramentas (2–3 dias)

Ambiente, linting, testes e CI básicos.

### T010: Adicionar configuração via .env
**Prioridade**: P2 (necessário para produção, não urgente localmente)  
**Sprint**: 3  
**Escopo**:
- Criar `backend/.env.example` com:
  ```
  DATABASE_URL=sqlite:///pingchampions.db
  CORS_ORIGINS=http://localhost:5173,http://localhost:3000
  DEBUG=true
  ```
- Atualizar `backend/database.py` para ler `DATABASE_URL` de env (fallback para SQLite local).
- Atualizar `backend/main.py` para ler `CORS_ORIGINS` de env.
- Adicionar `python-dotenv` a `backend/requirements.txt`.
- Adicionar `.env` a `.gitignore`.

**Critérios de aceite**:
- [ ] `.env.example` documentado e versionado.
- [ ] `.env` ignorado pelo git.
- [ ] `backend/database.py` lê `DATABASE_URL` (com fallback).
- [ ] `backend/main.py` lê `CORS_ORIGINS` (com fallback).
- [ ] Testes: CORS ajusta dinamicamente conforme `.env`.

**Arquivos**: `backend/.env.example`, `backend/database.py`, `backend/main.py`, `backend/requirements.txt`, `.gitignore`

**Esforço**: 45 min  
**Dependências**: nenhuma (paralelo)

---

### T011: Configurar Alembic para migrações
**Prioridade**: P2  
**Sprint**: 3  
**Escopo**:
- Adicionar `alembic` e `sqlalchemy` a `backend/requirements.txt`.
- Inicializar Alembic: `alembic init migrations`.
- Configurar `alembic/env.py` para autogenerar migração inicial.
- Gerar primeira migração: `alembic revision --autogenerate -m "init"`.
- Documentar no README: como rodar migrações (`alembic upgrade head`).

**Critérios de aceite**:
- [ ] Diretório `backend/migrations/` existe com versions/.
- [ ] Primeira migração cria tabelas de eventos, players, matches.
- [ ] `alembic upgrade head` roda sem erros.
- [ ] `backend/main.py` remove `Base.metadata.create_all()` (usar migrações).
- [ ] README backend menciona `alembic upgrade head` antes de iniciar app.

**Arquivo**: `backend/requirements.txt`, `alembic/` (novo), `backend/main.py`, `backend/README.md`

**Esforço**: 1 hora  
**Dependências**: nenhuma (paralelo)

---

### T012: Adicionar Ruff e Black para Python
**Prioridade**: P2 (qualidade)  
**Sprint**: 3  
**Escopo**:
- Adicionar `ruff` e `black` a `backend/requirements.txt` (ou `dev-requirements.txt`).
- Criar `backend/pyproject.toml` com configurações (linha max: 100, etc.).
- Rodar: `ruff check . && black .` para verificar.
- Documentar scripts no README: `ruff check .` e `black .`.

**Critérios de aceite**:
- [ ] `ruff check backend/` retorna 0 erros (ou documentadas exclusões).
- [ ] `black --check backend/` aprova o código (ou rodou `black backend/` e passou).
- [ ] `pyproject.toml` está presente com config mínima.
- [ ] README backend menciona `ruff check && black .`.

**Arquivo**: `backend/requirements.txt`, `backend/pyproject.toml`, `backend/README.md`

**Esforço**: 45 min  
**Dependências**: nenhuma (paralelo)

---

### T013: Adicionar ESLint e Prettier para Frontend
**Prioridade**: P2  
**Sprint**: 3  
**Escopo**:
- Adicionar `eslint`, `prettier`, `eslint-plugin-vue` a `frontend/package.json`.
- Criar `frontend/.eslintrc.json` e `frontend/.prettierrc.json`.
- Executar: `npm run lint` e `npm run format`.
- Adicionar scripts ao `package.json`:
  ```json
  "lint": "eslint src/ --fix",
  "format": "prettier --write src/"
  ```

**Critérios de aceite**:
- [ ] `npm run lint` retorna 0 erros em `src/`.
- [ ] `npm run format` formata código sem erros.
- [ ] `.eslintrc.json` e `.prettierrc.json` estão versionados.
- [ ] README frontend menciona `npm run lint` e `npm run format`.

**Arquivo**: `frontend/package.json`, `frontend/.eslintrc.json`, `frontend/.prettierrc.json`, `frontend/README.md`

**Esforço**: 45 min  
**Dependências**: nenhuma (paralelo)

---

### T014: Adicionar testes pytest para backend
**Prioridade**: P2  
**Sprint**: 3  
**Escopo**:
- Adicionar `pytest` e `httpx` a `backend/requirements.txt`.
- Criar `backend/tests/` com:
  - `tests/conftest.py` (fixture para database de teste).
  - `tests/test_events.py` (testes básicos: create, list, delete, 404).
  - `tests/test_players.py` (testes básicos: create, list, update, delete, 404).
- Cobrir happy path e erros (400, 404).
- Documentar: `pytest backend/tests/` no README.

**Critérios de aceite**:
- [ ] `pytest backend/tests/ -v` roda todas as testes com sucesso.
- [ ] Cobertura: `EventCreate`, `list_events`, `delete_event` com sucesso e erro.
- [ ] Cobertura: `register_player`, `list_players`, `update_player`, `delete_player` com sucesso e erro.
- [ ] README backend menciona `pytest backend/tests/ -v`.

**Arquivo**: `backend/tests/`, `backend/requirements.txt`, `backend/README.md`

**Esforço**: 2 horas  
**Dependências**: T006, T007

---

### T015: Adicionar testes vitest para frontend
**Prioridade**: P3 (frontend tests menos crítico neste estágio)  
**Sprint**: 3  
**Escopo**:
- Adicionar `vitest` e `@vitest/ui` a `frontend/package.json`.
- Criar `frontend/tests/unit/services/` com testes para:
  - `services/events.js` (mock axios).
  - `services/players.js` (mock axios).
- Testar: list, create, delete, error handling.
- Adicionar script: `npm run test` e `npm run test:ui`.

**Critérios de aceite**:
- [ ] `npm run test` roda todos os testes com sucesso.
- [ ] Cobertura: `eventsService.list()`, `create()`, `delete()` com sucesso e erro.
- [ ] Cobertura: `playersService` análogo.
- [ ] Mocks de axios funcionam.

**Arquivo**: `frontend/tests/`, `frontend/package.json`, `frontend/README.md`

**Esforço**: 1.5 horas  
**Dependências**: nenhuma (paralelo após T001)

---

## Sprint 4 — Documentação e DX (1–2 dias)

Documentação de contratos, scripts e guias de contribuição.

### T016: Criar docs/ENDPOINTS.md com contratos de API
**Prioridade**: P1 (onboarding)  
**Sprint**: 4  
**Escopo**:
- Documento `docs/ENDPOINTS.md` com tabela ou lista de todos os endpoints.
- Para cada endpoint: método, rota, descrição, request body (JSON schema), response (JSON schema), exemplos com curl, status codes.
- Exemplo:
  ```markdown
  ### POST /events/create
  Criar um novo evento.
  
  **Request**:
  ```json
  {
    "name": "Torneio de Novembro",
    "date": "2025-11-15",
    "time": "19:00"
  }
  ```
  
  **Response** (201):
  ```json
  {
    "id": 1,
    "name": "Torneio de Novembro",
    "date": "2025-11-15T00:00:00",
    "time": "19:00",
    "active": true
  }
  ```
  
  **cURL**:
  ```bash
  curl -X POST http://localhost:8000/events/create \
    -H "Content-Type: application/json" \
    -d '{"name":"Torneio","date":"2025-11-15","time":"19:00"}'
  ```
  ```

**Critérios de aceite**:
- [ ] `docs/ENDPOINTS.md` lista todos os endpoints (events, players, matches, ranking).
- [ ] Cada endpoint tem: método, rota, descrição, exemplo request/response, cURL.
- [ ] Exemplos com dados realistas e testáveis.
- [ ] Arquivo é legível e fácil de navegar (índice com links).

**Arquivo**: `docs/ENDPOINTS.md`

**Esforço**: 1 hora  
**Dependências**: T006, T007, T008, T009

---

### T017: Criar docs/ARCHITECTURE.md com diagrama ERD e fluxo
**Prioridade**: P2 (onboarding)  
**Sprint**: 4  
**Escopo**:
- Documento `docs/ARCHITECTURE.md` com:
  - Diagrama simples ERD (texto ASCII ou ref a Mermaid).
  - Fluxo de dados: criar evento → adicionar jogadores → registrar partidas → atualizar ranking.
  - Camadas (API, ORM, banco).
  - Decisões de design (soft delete, integridade de dados).

**Critérios de aceite**:
- [ ] ERD mostra Events, Players, Matches e relacionamentos.
- [ ] Fluxo é claro e segue a sequência típica de uso.
- [ ] Decisões estão documentadas.

**Arquivo**: `docs/ARCHITECTURE.md`

**Esforço**: 45 min  
**Dependências**: nenhuma (paralelo)

---

### T018: Atualizar READMEs com scripts e checklist de start
**Prioridade**: P1 (DX crítico)  
**Sprint**: 4  
**Escopo**:
- Backend README:
  - Adicionar seção "Scripts úteis":
    ```bash
    # Dev
    uvicorn main:app --reload
    
    # Lint
    ruff check . && black .
    
    # Tests
    pytest tests/ -v
    
    # Migrations
    alembic upgrade head
    ```
  - Adicionar checklist "Primeira execução":
    ```
    - [ ] python -m venv venv
    - [ ] pip install -r requirements.txt
    - [ ] cp .env.example .env
    - [ ] alembic upgrade head
    - [ ] uvicorn main:app --reload
    - [ ] Verificar http://localhost:8000/docs
    ```

- Frontend README:
  - Adicionar seção "Scripts úteis":
    ```bash
    npm run dev
    npm run build
    npm run lint
    npm run format
    npm run test
    npm run test:ui
    ```
  - Adicionar checklist análoga.

**Critérios de aceite**:
- [ ] Backend README atualizado com scripts e checklist.
- [ ] Frontend README atualizado com scripts e checklist.
- [ ] Ambos READMEs mencionam `.env` / configuração.
- [ ] Ambos mencionam migrações (backend) ou build (frontend).

**Arquivo**: `backend/README.md`, `frontend/README.md`

**Esforço**: 45 min  
**Dependências**: T010, T012, T013, T014

---

### T019: Criar docs/CONTRIBUTING.md (guia de contribuição)
**Prioridade**: P3 (bom ter, não crítico)  
**Sprint**: 4  
**Escopo**:
- Documento `docs/CONTRIBUTING.md` com:
  - Como fazer fork/branch (`git checkout -b feat/xxx`).
  - Convenção de commits e PRs.
  - Padrões de código (PEP 8 backend, Vue 3 + ES6 frontend).
  - Como rodar testes antes de PR.
  - Processo de review.

**Critérios de aceite**:
- [ ] `docs/CONTRIBUTING.md` é claro e menciona fluxo de branch/PR.
- [ ] Padrões de código estão documentados.
- [ ] Mencionados: lint, testes, commit message.

**Arquivo**: `docs/CONTRIBUTING.md`

**Esforço**: 30 min  
**Dependências**: nenhuma (paralelo)

---

## Sprint 5 — Camada de Domínio e Negócio (1–2 semanas)

Introduzir serviços de domínio e regras de pontuação/ranking.

### T020: Criar camada de serviços no backend
**Prioridade**: P1 (base para crescimento)  
**Sprint**: 5  
**Escopo**:
- Criar `backend/services/` com `events.py`, `players.py`, `matches.py`.
- `EventService`: criar, listar, deletar com transações.
- `PlayerService`: registrar, atualizar nome, remover com validação.
- `MatchService`: registrar match, finalizar match com atualização de score/ranking.
- Mover lógica das rotas para serviços (dependency injection).

**Critérios de aceite**:
- [ ] `backend/services/` existe com 3+ serviços.
- [ ] Rotas injetam serviços e delegam lógica.
- [ ] `MatchService.finish_match()` atualiza `Player.score` e `Player.ranking` atomicamente.
- [ ] Testes passam (cobertura de serviços).

**Arquivo**: `backend/services/`, `backend/routers/`, `backend/tests/`

**Esforço**: 2–3 horas  
**Dependências**: T006, T014

---

### T021: Implementar lógica de pontuação e ranking
**Prioridade**: P1  
**Sprint**: 5  
**Escopo**:
- Em `MatchService.finish_match()`: somar pontos ao vencedor.
- Função `update_ranking()` que reordena players por score para cada evento.
- Atualizar endpoint `GET /ranking?event_id=X` para retornar players ordenados.

**Critérios de aceite**:
- [ ] `finish_match(match_id, winner_id)` incrementa score do vencedor.
- [ ] `GET /ranking?event_id=1` retorna jogadores por score DESC.
- [ ] Testes: finish match → score atualiza → ranking muda.

**Arquivo**: `backend/services/matches.py`, `backend/routers/ranking.py`, `backend/tests/`

**Esforço**: 1.5 horas  
**Dependências**: T020

---

## Sprint 6+ — Crescimento (Futuro)

Autenticação, paginação, observabilidade, CI/CD.

### T022: Adicionar autenticação JWT para admin
**Prioridade**: P3  
**Sprint**: 6  
**Escopo**:
- Backend: Adicionar `PyJWT` e `python-multipart`.
- Criar `backend/auth.py` com funções de login/token/verification.
- Proteger endpoints mutantes com decorator `@require_admin`.
- Armazenar admin credentials em `.env` (hardcoded ou BD simples).

**Esforço**: 2–3 horas  
**Dependências**: T010

---

### T023: Adicionar paginação nas listagens
**Prioridade**: P2  
**Sprint**: 6  
**Escopo**:
- Adicionar `skip` e `limit` como query params em `/events`, `/players`, `/matches`.
- Backend: usar `.offset().limit()` no SQLAlchemy.
- Atualizar schemas para incluir `total` e `page_info`.

**Esforço**: 1.5 horas  
**Dependências**: T006

---

### T024: Configurar CI básica (GitHub Actions)
**Prioridade**: P2  
**Sprint**: 6  
**Escopo**:
- `.github/workflows/ci.yml` com:
  - Lint (ruff, black, eslint).
  - Testes (pytest, vitest).
  - Build frontend.
- Rodar em cada push/PR.

**Esforço**: 1 hora  
**Dependências**: T012, T013, T014, T015

---

## Resumo de Dependências (Grafo)

```
T001 (SFC fix) — independente
  └─ Depende: nenhuma

T002 (serviços redundantes) — independente
  └─ Depende: nenhuma

T003 (ORM relacionamento) — independente
  └─ Depende: nenhuma

T004 (trailing slashes) — independente
  └─ Depende: nenhuma

T005 (delete strategy) — independente
  └─ Depende: nenhuma

T006 (schemas Events) — depende de T004
  └─ Bloqueia: T007, T008, T009, T016, T020

T007 (schemas Players) — depende de T006
  └─ Bloqueia: T020

T008 (schemas Matches) — depende de T006
  └─ Bloqueia: T021

T009 (GET /events/{id}) — depende de T006
  └─ Bloqueia: nenhuma (melhoria)

T010 (.env config) — independente
  └─ Bloqueia: T011, T022

T011 (Alembic) — independente
  └─ Bloqueia: nenhuma (infra)

T012 (Ruff/Black) — independente
  └─ Bloqueia: T014, T024

T013 (ESLint/Prettier) — independente
  └─ Bloqueia: T015, T024

T014 (pytest tests) — depende de T006, T007
  └─ Bloqueia: T020, T024

T015 (vitest tests) — depende de T001 (idealmente)
  └─ Bloqueia: T024

T016 (ENDPOINTS.md) — depende de T006, T007, T008, T009
  └─ Bloqueia: nenhuma (docs)

T017 (ARCHITECTURE.md) — independente
  └─ Bloqueia: nenhuma (docs)

T018 (README updates) — depende de T010, T012, T013, T014
  └─ Bloqueia: nenhuma (docs)

T019 (CONTRIBUTING.md) — independente
  └─ Bloqueia: nenhuma (docs)

T020 (Services layer) — depende de T006, T014
  └─ Bloqueia: T021

T021 (Scoring/Ranking) — depende de T020
  └─ Bloqueia: nenhuma (feature)

T022 (JWT Auth) — depende de T010
  └─ Bloqueia: nenhuma (feature)

T023 (Pagination) — depende de T006
  └─ Bloqueia: nenhuma (feature)

T024 (CI/CD) — depende de T012, T013, T014, T015
  └─ Bloqueia: nenhuma (infra)
```

---

## Como usar este documento

1. **Para PM/Product**: Use as prioridades e sprints para planejar roadmap.
2. **Para devs**: Pegue uma tarefa, confira dependências, e abra uma issue com o número (T001, etc.).
3. **Para QA**: Use os "Critérios de aceite" para validar.
4. **Para feedback**: Adicione observações (esforço real, bloqueadores) em issues.

---

## Template de Issue (copiar para GitHub/Jira)

```markdown
## T00X: [Título da tarefa]

**Prioridade**: P[0-3]  
**Sprint**: [Sprint N]  
**Esforço**: [Xh ou Xy]  
**Status**: [ ] Não iniciada [ ] Em progresso [ ] Concluída

### Escopo
[Descrição concisa]

### Critérios de aceite
- [ ] Critério 1
- [ ] Critério 2
- [ ] Critério 3

### Arquivos envolvidos
- `path/to/file1.py`
- `path/to/file2.vue`

### Dependências
- T00Y (se aplicável)

### Observações
[Qualquer contexto adicional]
```

---

**Última atualização**: 2025-11-02  
**Versão**: 1.0
