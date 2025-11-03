# Ping Champions — Avaliação de Arquitetura (2025-11-02)

Este documento avalia: (1) grau de complexidade, (2) níveis de abstração, (3) número de responsabilidades dos métodos, (4) potencial de crescimento, (5) facilidade de manutenção, e (6) facilidade de onboarding de novos desenvolvedores.

## Visão geral

- Monorepo simples com `backend/` (FastAPI + SQLAlchemy + SQLite) e `frontend/` (Vue 3 + Vite + axios + vue-router).
- Código pequeno e direto, com boa separação por domínio (events, players, matches).
- Documentação inicial OK, porém com algumas inconsistências e pontos a melhorar.

## 1) Grau de complexidade

- Backend: baixo. Rotas CRUD simples, sem camada de serviços, poucos modelos e sem regras de negócio complexas implementadas ainda (ranking e atualização de pontuação não acoplados aos matches).
- Frontend: baixo. Rotas declarativas, serviços axios finos, poucas páginas, sem estado global complexo.

Conclusão: complexidade baixa (positivo para manutenção inicial e onboarding), com alguns pontos de inconsistência que podem gerar bugs.

## 2) Níveis de abstração

- Backend: 2 camadas explícitas — API (routers FastAPI) e persistência (modelos SQLAlchemy). Falta uma camada de domínio/serviços para encapsular regras (p.ex.: finalizar partida e atualizar score/ ranking com transação). Falta padronização de schemas Pydantic para requests e responses (apenas `EventCreate` existe).
- Frontend: componentes de página (views), componentes reutilizáveis (components) e camada de serviços (axios). Não há gerenciamento de estado global (o que é bom neste tamanho).

Conclusão: Abstrações mínimas e suficientes para o porte atual, mas será importante introduzir uma camada de serviços no backend e schemas Pydantic conforme o domínio crescer.

## 3) Responsabilidade dos métodos

- Rotas curtas e focadas (bom). Porém:
  - `events.create_event` implementa parsing de data + persistência → aceitável, mas ideal mover validação para schema Pydantic.
  - Endpoints de `players` usam query params em vez de body JSON para criação/atualização, misturando responsabilidades de validação e persistência.
  - Não há validações de consistência (ex.: winner do match precisa ser um dos jogadores, existência do event_id, duplicidade de nomes conforme regra, etc.).

Conclusão: Boa coesão em geral, mas falta padronizar a entrada (schemas) e mover regras para serviços para reduzir acoplamento nas rotas.

## 4) Potencial de crescimento

Potencial médio/alto, desde que alguns pontos base sejam endereçados:
- Adotar migrações (Alembic) e ambiente (.env) permite evolução do schema com segurança.
- Introduzir uma camada de domínio/serviços dá espaço para regras de negócio (pontuação, ranking, pareamento) sem inflar as rotas.
- Versionar API (v1) e padronizar contratos (slashes, body vs query) viabiliza evoluções sem quebrar o frontend.

## 5) Facilidade de manutenção

Hoje: média.

Pontos positivos:
- Código curto e organizado em pastas claras (models/routers/services/views).
- Comentários explicativos ajudam o leitor inicial.

Pontos a melhorar (impacto direto na manutenção):
- Backend: relação duplicada/ sobrescrita entre `Event` e `Player` em `models/player.py` (redefinição de `Event.players`) pode apagar `cascade` configurado em `models/event.py` → bug sutil.
- Backend: inconsistência de soft delete (Event usa boolean `active`; Player usa `active` como int mas `DELETE` faz hard delete).
- Backend: tipos inteiros para flags booleanas (`Match.finished`, `Player.active`).
- Backend: `Event.date` (DateTime) + `Event.time` (String). Unificar em um `datetime` seria mais simples.
- Backend: inconsistência de trailing slash nas rotas (pode causar 307 em POST) e uso misto de body vs query params.
- Backend: CORS hardcoded; deveria vir de env/ config.
- Frontend: `src/views/EventsView.vue` contém CSS fora de `<style>` → quebra de SFC e risco de falha de build.
- Frontend: serviços/arquivos redundantes (`jogadores.js` vazio, `jogos.js` stub). Misto de inglês/português no código e nos serviços → consistência e i18n.
- Frontend: `Breadcrumbs` faz fetch da lista de eventos e procura o nome por ID (overfetch). Melhor: endpoint `GET /events/{id}`.

## 6) Onboarding de novos desenvolvedores

Hoje: médio.

- Pros: Estrutura clara, READMEs básicos com passos de execução.
- Contras: documentação em PT/EN misturada; endpoints no README backend não batem 100% com os caminhos reais; falta `.env.example`, migrações, scripts de conveniência, e um mapa de endpoints.

Ajustes simples (abaixo) podem elevar para "alto" rapidamente.

---

## Quality gates — triagem rápida

- Backend — Build: PASS (não há build; por inspeção está ok para `uvicorn main:app`).
- Frontend — Build: FAIL (risco) devido a `EventsView.vue` com CSS fora de `<style>`.
- Lint/Typecheck: FAIL (não configurado em ambos os lados).
- Tests: FAIL (inexistentes).

Observação: não executado em CI; é uma avaliação estática. Recomenda-se configurar jobs mínimos de lint e testes.

---

## Recomendações priorizadas (1–2 dias)

1. Corrigir `EventsView.vue`: mover CSS para `<style scoped>` e remover trechos fora de bloco.
2. Limpar arquivos mortos: remover `src/services/jogadores.js` e alinhar `jogos.js` (ou remover até existir backend de matches).
3. Backend: corrigir o relacionamento duplicado. Remover em `models/player.py` a linha que reatribui `Event.players = relationship(...)`; manter a definição única em `models/event.py` e a contraparte `Player.event` com `back_populates`.
4. Padronizar API: remover barras finais de rotas, usar body JSON para criação/atualização, alinhar services do frontend para evitar 307/redirect em POST.
5. Converter flags para `Boolean` (`Player.active`, `Match.finished`) e unificar o conceito de soft delete (ou hard delete) de forma consistente.
6. Criar schemas Pydantic para requests/ responses: `EventCreate/Read`, `PlayerCreate/Update/Read`, `MatchCreate/Update/Read`; mover validações para os schemas.
7. Expor `GET /events/{id}` e usar no `Breadcrumbs` (evitar overfetch da lista inteira).
8. Configuração via `.env` (DB URL, CORS origins) e leitura centralizada. Adicionar `.env.example`.
9. Introduzir Alembic para migrações do banco.
10. Adicionar lint/format:
    - Python: Ruff + Black + isort; opcional mypy.
    - Frontend: ESLint + Prettier.
11. Testes mínimos:
    - Backend: `pytest` para `events` e `players` (happy path + erro 404/400).
    - Frontend: `vitest` com mocks de axios para `services/`.
12. Documentação: `docs/` com tabela de endpoints (contratos), diagrama simples (ERD) e checklist de scripts.

## Roadmap (4–8 semanas)

- Camada de serviços no backend para encapsular regras (pontuação, ranking, pareamento) com transações atômicas.
- Atualizar `score`/`ranking` ao finalizar `Match` (gatilho/serviço, não na rota diretamente).
- Paginação e filtros nas listagens (players, matches, events).
- Autenticação de administrador (FastAPI + JWT) e autorização básica.
- Versionamento da API (`/api/v1`).
- Observabilidade: logging estruturado (pydantic-logging/ structlog), correlação de requisições.
- Scripts DX: `make`/`Invoke`/`npm` scripts para dev/ test/ lint.

## Indicadores qualitativos

- Complexidade: baixa (bom).
- Abstração: mínima (2 camadas); precisa de camada de domínio quando crescer.
- Responsabilidade dos métodos: curta/única em geral; carece de schemas/ serviços.
- Crescimento: médio/alto após ajustes de base (migrations/ serviços/ contratos).
- Manutenção: média → pode virar alta com as correções acima.
- Onboarding: médio → tende a alto com documentação e scripts.

## Pequenas inconsistências específicas (para referência rápida)

- `backend/models/player.py`: reatribui `Event.players` após a classe — remove a configuração `cascade` existente em `models/event.py` (corrigir removendo a reatribuição).
- `backend/routers/events.py`: `POST /events/create/` tem barra final; frontend chama `/events/create` (padronizar).
- `backend/routers/players.py`: usa query params para criar/atualizar; padronizar para body JSON.
- `frontend/src/views/EventsView.vue`: CSS fora de `<style>` (corrigir).
- `frontend/src/services/jogadores.js`: arquivo vazio; `jogos.js` é stub — decidir manter/ remover.
- `frontend/src/components/Breadcrumbs.vue`: busca toda a lista para achar um evento; preferir `GET /events/{id}`.

---

## Checklist de DX (sugestão)

- `backend/.env.example` com `DATABASE_URL`, `CORS_ORIGINS`.
- `backend` scripts: `uvicorn main:app --reload`, `pytest`, `alembic upgrade head`, `ruff check`, `black .`.
- `frontend` scripts: `npm run dev`, `npm run build`, `npm run test`, `npm run lint`.
- `docs/ENDPOINTS.md` com contratos e exemplos.
