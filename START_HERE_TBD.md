# 🎯 TRUNK-BASED DEVELOPMENT - PRÓXIMOS PASSOS

**Status**: Setup Concluído ✅  
**Data**: 2025-11-02  
**Pronto para**: Começar Sprint 1

---

## 🚀 HOJE - Execute Agora (15-30 min)

### 1. Setup Local
```powershell
# Windows - Execute uma vez
.\scripts\setup-dev.bat
```

```bash
# Mac/Linux - Execute uma vez
bash scripts/setup-dev.sh
```

✅ Isso vai:
- Criar virtual environment
- Instalar todas as dependências
- Criar .env files
- Configurar pre-commit hooks

### 2. Valide Setup
```bash
# Backend
cd backend
source venv/bin/activate
flake8 .
pytest

# Frontend
cd ../frontend
npm run lint
npm run build

# Resultado esperado: Tudo sem erros
```

### 3. Inicie Localmente
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev

# Abra: http://localhost:5173
```

✅ Pronto! App rodando localmente.

---

## 📚 HOJE/HOJE - Leia Documentação (30 min)

### Priority 1: Todos devem ler
1. **TBD_QUICK_START.md** (5 min)
   - Comece em 5 minutos
   - Workflow básico

2. **TRUNK_BASED_DEV_GUIDE.md** (15 min)
   - Workflow completo
   - Troubleshooting

### Priority 2: Devs devem ler
3. **COMMIT_CONVENTIONS.md** (10 min)
   - Padrão de commits obrigatório
   - Exemplos práticos

### Priority 3: Tech Leads
4. **.github/BRANCH_PROTECTION_RULES.md** (5 min)
   - Como configurar no GitHub
   - Regras recomendadas

---

## 📋 AMANHÃ - GitHub Configuration (5 min)

**Quem**: Alguém com acesso admin  
**Onde**: https://github.com/hirohaya/ping-champions/settings/branches

### Passo a Passo
1. Clique em "Add rule"
2. Branch name pattern: `main`
3. Ative as seguintes opções:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - ✅ Require code reviews before merging (1 minimum)
   - ✅ Dismiss stale pull request approvals
   - ✅ Include administrators

4. Select status checks:
   - ✅ Validate Code
   - ✅ Validate Frontend

5. Clique "Create"

✅ Pronto! GitHub protegido.

---

## 🏆 SPRINT 1 - Tarefas Críticas (Comece agora!)

### T001: Fix SFC Error (15-30 min)
```bash
git checkout -b fix/T001-sfc-error
# Editar: frontend/src/views/EventsView.vue
# Remover CSS fora da tag <style>
git add .
git commit -m "fix(views): remove CSS outside style block"
git push origin fix/T001-sfc-error
# Abrir PR → Esperar checks → Merge
```

### T003: Fix ORM Cascade (10-20 min)
```bash
git checkout -b fix/T003-orm-cascade
# Editar: backend/models/player.py
# Remover linha que redefine Event.players
git add .
git commit -m "fix(models): preserve ORM cascade configuration"
git push origin fix/T003-orm-cascade
# Abrir PR → Esperar checks → Merge
```

### T004: Trailing Slashes (20-30 min)
```bash
git checkout -b fix/T004-trailing-slashes
# Editar: backend/routers/events.py, players.py, matches.py
# Remover trailing slashes (/ no final)
git add .
git commit -m "fix(api): standardize endpoint paths"
git push origin fix/T004-trailing-slashes
# Abrir PR → Esperar checks → Merge
```

### T002: Remove Obsolete Services (10-15 min)
```bash
git checkout -b chore/T002-cleanup-services
# Deletar: frontend/src/services/jogadores.js, jogos.js
git add .
git commit -m "chore(services): remove obsolete service files"
git push origin chore/T002-cleanup-services
# Abrir PR → Esperar checks → Merge
```

### T005: Decide Delete Strategy (5-10 min, discussão)
```bash
# Discussão em PR comentário
# Decidir: soft delete vs hard delete
# Documentar decisão em QUICK_REFERENCE.md
```

**Tempo Total Sprint 1**: 1-2 dias  
**Bloqueadores**: Nenhum  
**Deploy Impact**: Alto (fixes críticos)

---

## 📊 WORKFLOW PADRÃO (Diário)

```
Morning (5 min)
├─ git checkout main
└─ git pull origin main

Work (Horas)
├─ git checkout -b fix/T00X-description
├─ [Editar, testar, etc]
├─ git add .
└─ git commit -m "fix(scope): description"

Push (5 min)
├─ git push origin fix/T00X-description
├─ GitHub cria PR automaticamente
└─ Clique no link

CI/CD (Automático)
├─ Linting (flake8, black, isort)
├─ Testes (pytest)
├─ Build (Vite)
└─ Coverage report

Review (1-4 horas)
├─ Aguardar review de alguém
├─ Responder comentários se houver
└─ Após aprovação: Clique "Squash and merge"

Done! (1 min)
└─ Seu código está no main! 🎉
```

---

## 🎯 PADRÃO DE COMMITS (OBRIGATÓRIO)

Toda mensagem de commit deve seguir:

```
<type>(<scope>): <subject>
```

### Exemplos ✅ Corretos
```
fix(views): remove CSS outside style block
feat(events): add date filter
refactor(api): simplify validation
test(players): add unit tests
docs: update setup guide
chore: update dependencies
ci: add coverage reporting
```

### Exemplos ❌ Errados
```
fixed bug
T001 done
WIP
update
debug
```

### Types
- `feat` — Nova funcionalidade
- `fix` — Correção de bug
- `refactor` — Mudança estrutural
- `test` — Testes
- `docs` — Documentação
- `chore` — Deps, build, etc
- `ci` — CI/CD
- `perf` — Performance
- `style` — Formatação

### Scopes
- Backend: `events`, `players`, `matches`, `ranking`, `api`, `db`, `models`
- Frontend: `views`, `components`, `services`, `router`
- Infra: `ci`, `docker`, `config`

Referência completa: `COMMIT_CONVENTIONS.md`

---

## 📞 DÚVIDAS? CONSULTE

| Pergunta | Arquivo |
|----------|---------|
| Como começo? | `TBD_QUICK_START.md` |
| Qual é o workflow? | `TRUNK_BASED_DEV_GUIDE.md` |
| Qual o padrão de commits? | `COMMIT_CONVENTIONS.md` |
| Como configuro GitHub? | `.github/BRANCH_PROTECTION_RULES.md` |
| Como faço setup? | `TRUNK_BASED_DEV_CHECKLIST.md` |
| Erro X, como resolvido? | `TRUNK_BASED_DEV_GUIDE.md` → Troubleshooting |
| Qual a tarefa próxima? | `docs/TASKS.md` |

---

## 📊 CHECKLIST: PRIMEIRA SEMANA

### Dia 1: Setup
- [ ] Clone repositório
- [ ] Execute `setup-dev.bat` ou `setup-dev.sh`
- [ ] Valide backend (flake8, pytest)
- [ ] Valide frontend (npm run lint)
- [ ] Inicie ambos localmente
- [ ] Leia `TBD_QUICK_START.md`

### Dia 2: Learning
- [ ] Leia `TRUNK_BASED_DEV_GUIDE.md`
- [ ] Leia `COMMIT_CONVENTIONS.md`
- [ ] Configure GitHub branch protections
- [ ] Estude `TBD_SETUP_COMPLETE.md`

### Dia 3-5: Sprint 1
- [ ] T001: Fix SFC error
- [ ] T003: Fix ORM cascade
- [ ] T004: Trailing slashes
- [ ] T002: Remove obsolete services
- [ ] T005: Decide delete strategy

### Validações
- [ ] Todos os commits seguem padrão
- [ ] Todos os PRs têm descrição
- [ ] Todos os checks passam (CI/CD)
- [ ] Todos os merges são squash
- [ ] Branches deletados após merge

---

## 🚨 IMPORTANTE: Regras Obrigatórias

### 1. Commit Message Format
- ✅ DEVE seguir: `type(scope): description`
- ❌ NÃO pode ser genérico
- Pre-commit hook valida automaticamente

### 2. Branch Duration
- ✅ DEVE ser < 1 dia
- ❌ NÃO deve ficar aberto > 2 dias
- Se durar > 2 dias: refactor/split

### 3. Pull Request Review
- ✅ DEVE ter ≥ 1 approval
- ✅ DEVE passar em todos os checks
- ✅ DEVE ser atualizado com main
- ❌ NÃO pode ter conflitos

### 4. Code Quality
- ✅ DEVE passar em linting
- ✅ DEVE passar em testes
- ✅ DEVE buildar sem erros
- ❌ NÃO aceita erros de CI/CD

---

## 🎁 O que você vai ganhar

✅ **Integração Contínua** — Código integrado rápido  
✅ **Feedback Automático** — Erros descobertos em horas  
✅ **Confiabilidade** — Testes obrigatórios  
✅ **Rastreabilidade** — Commits bem documentados  
✅ **Deploy Frequente** — Pronto quando necessário  
✅ **Sem Conflitos** — Branches curtos  
✅ **Equipe Produtiva** — Menos overhead  

---

## 📈 Roadmap Próximas Semanas

### Sprint 1 (Esta semana): Bugs críticos
- T001-T005 (4-5 horas total)
- Foco: Bugs P0, P1

### Sprint 2 (Próxima): Schemas
- T006-T009 (6-8 horas)
- Foco: Validação, API consistency

### Sprint 3 (Seguinte): Testing & Infra
- T010-T017 (8-10 horas)
- Foco: Tests, CI/CD, Docker

### Sprint 4+: Features & Polish
- T018-T024 (8+ horas)
- Foco: New features, refinements

---

## 📖 Referências Úteis

- **Trunk-Based Development**: https://trunkbaseddevelopment.com/
- **Conventional Commits**: https://www.conventionalcommits.org/
- **GitHub Flow**: https://guides.github.com/introduction/flow/
- **Pytest**: https://docs.pytest.org/
- **Git**: https://git-scm.com/book/

---

## 🏁 Resumo Final

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│  🟢 TRUNK-BASED DEVELOPMENT SETUP COMPLETO         │
│                                                      │
│  ✅ Infrastructure (CI/CD, Git, Protections)      │
│  ✅ Documentation (7 guides)                        │
│  ✅ Scripts (Setup + Helpers)                       │
│  ✅ Configuration (All tools)                       │
│  ✅ Committed to GitHub                             │
│  ✅ Ready for Sprint 1                              │
│                                                      │
│  Próxima ação:                                       │
│  1. Execute setup-dev.*                              │
│  2. Ler TBD_QUICK_START.md                           │
│  3. Começar T001                                     │
│                                                      │
│  Tempo estimado: 15-30 min setup                     │
│                30 min leitura                        │
│                1-2 dias Sprint 1                     │
│                                                      │
│  Total: 2-3 dias pronto para produção! 🚀           │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## 🎓 Mentalidade TBD

> "Integração frequente, confiança em automação, documentação clara, deploy confiante"

- 🌳 Uma linha (main) de desenvolvimento
- ⚡ Branches curtos (horas, não dias)
- 🔄 Múltiplos merges por dia
- 🤖 CI/CD forte e confiável
- 📖 Commits bem documentados
- ✅ Testes obrigatórios
- 🚀 Deploy frequente

---

**Status**: ✅ Pronto para Sprint 1  
**Versão**: 1.0  
**Próximo**: Comece T001 hoje! 🚀

---

_Prepare-se para desenvolvimento ágil e confiável!_
