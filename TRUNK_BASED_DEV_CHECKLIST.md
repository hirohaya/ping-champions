# 🌳 Trunk-Based Development - Setup Checklist

Checklist completo para implementar Trunk-Based Development no projeto.

---

## ✅ Fase 1: Setup Local (Seu Computador)

### Git Configuration
- [ ] Clonar repositório: `git clone https://github.com/hirohaya/ping-champions.git`
- [ ] Navegar para pasta: `cd ping-champions`
- [ ] Verificar remotes: `git remote -v` (deve mostrar origin)
- [ ] Checkout main: `git checkout main`
- [ ] Atualizar: `git pull origin main`

### Git Aliases (Opcional mas recomendado)
```bash
git config --global alias.co checkout
git config --global alias.sync 'pull --rebase origin main'
```
- [ ] Configurar aliases

### Backend Setup
- [ ] Criar venv: `python -m venv backend/venv`
- [ ] Ativar venv (Windows): `backend\venv\Scripts\activate`
- [ ] Ativar venv (Mac/Linux): `source backend/venv/bin/activate`
- [ ] Instalar deps: `pip install -r backend/requirements.txt`
- [ ] Instalar dev deps: `pip install -r backend/requirements-dev.txt`
- [ ] Criar `.env` (copiar de `ENV_TEMPLATE.md`)

### Frontend Setup
- [ ] Verificar Node.js: `node -v` (precisa 18+)
- [ ] Instalar deps: `cd frontend && npm install`
- [ ] Criar `.env.local` (copiar de `ENV_TEMPLATE.md`)

### Pre-commit Hooks
- [ ] Copiar script: `cp scripts/pre-commit.sh .git/hooks/pre-commit`
- [ ] Tornar executável: `chmod +x .git/hooks/pre-commit` (Mac/Linux)

### Test Local Dev
- [ ] Backend: `cd backend && uvicorn main:app --reload` (porta 8000)
- [ ] Frontend: `cd frontend && npm run dev` (porta 5173)
- [ ] Testar em http://localhost:5173

---

## ✅ Fase 2: Setup GitHub (Repositório)

### Branch Protection
1. Ir para: GitHub → Settings → Branches
2. Clique em "Add rule"
3. Branch name pattern: `main`

Configure:
- [ ] ✅ Require a pull request before merging
- [ ] ✅ Require approvals (mínimo 1)
- [ ] ✅ Dismiss stale pull request approvals
- [ ] ✅ Require status checks to pass before merging
- [ ] ✅ Require branches to be up to date before merging
- [ ] ✅ Include administrators
- [ ] ✅ Restrict who can push to matching branches (code owners)

### Status Checks
- [ ] Selecionar: "Validate Code"
- [ ] Selecionar: "Validate Frontend"

### Merge Settings
- [ ] Allow merge commits (default)
- [ ] Allow squash merging ✅
- [ ] Allow rebase merging ✅
- [ ] Default to squash merging (recomendado para TBD)

### Additional Config
- [ ] Require conversation resolution before merging ✅
- [ ] Require deployments to succeed (skip por agora)

---

## ✅ Fase 3: Documentação & Padrões

### Ler Documentação
- [ ] `TRUNK_BASED_DEV_GUIDE.md` — Guia completo de workflow
- [ ] `COMMIT_CONVENTIONS.md` — Padrão de commits
- [ ] `.github/BRANCH_PROTECTION_RULES.md` — Proteções do branch

### Setup VSCode Extensions (Opcional)
- [ ] Instalar: **Conventional Commits** (vivaxy)
- [ ] Instalar: **Git Graph** (mhutchie)
- [ ] Instalar: **Pylance** (Python)
- [ ] Instalar: **Volar** (Vue)

### Configure VSCode Settings
- [ ] Abrir: `.vscode/settings.json` (ou criar)
- [ ] Adicionar:
```json
{
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

---

## ✅ Fase 4: Primeira Sprint (Prática)

### T001: Fix SFC Error
- [ ] Criar branch: `git checkout -b fix/T001-sfc-error`
- [ ] Editar: `frontend/src/views/EventsView.vue`
- [ ] Commit: `git commit -m "fix(views): remove CSS from template"`
- [ ] Push: `git push origin fix/T001-sfc-error`
- [ ] Abrir PR no GitHub
- [ ] Aguardar reviews & checks
- [ ] Merge → Squash
- [ ] Deletar branch: `git branch -d fix/T001-sfc-error`

### T003: Fix ORM Cascade
- [ ] Criar branch: `git checkout -b fix/T003-orm-cascade`
- [ ] Editar: `backend/models/player.py`
- [ ] Remover: linha que redefine `Event.players` relationship
- [ ] Commit: `git commit -m "fix(models): preserve ORM cascade config"`
- [ ] Push & PR
- [ ] Merge

### T004: Trailing Slashes
- [ ] Criar branch: `git checkout -b fix/T004-trailing-slashes`
- [ ] Editar: `backend/routers/events.py`, `players.py`, `matches.py`
- [ ] Remover trailing slashes
- [ ] Commit: `git commit -m "fix(api): standardize endpoint paths"`
- [ ] Push & PR
- [ ] Merge

---

## ✅ Fase 5: Automação & CI/CD

### GitHub Actions
- [ ] Verificar: `.github/workflows/trunk-based-dev.yml` existe
- [ ] Trigger automático em push/PR

### Workflows
- [ ] Validação rodando no GitHub (Python 3.9, 3.10, 3.11)
- [ ] Linting (flake8, black, isort)
- [ ] Testes (pytest)
- [ ] Frontend build (npm run build)

### Coverage
- [ ] Codecov integration (opcional para Sprint 2)

---

## ✅ Fase 6: Team & Governance

### Team Structure (Se aplicável)
- [ ] Criar GitHub Team: "Backend"
- [ ] Criar GitHub Team: "Frontend"
- [ ] Adicionar members

### Code Owners
- [ ] Criar `.github/CODEOWNERS`:
```
backend/     @backend-team
frontend/    @frontend-team
docs/        *
```

### Labels
- [ ] Criar labels no GitHub:
  - `priority/P0`, `priority/P1`, `priority/P2`, `priority/P3`
  - `type/bug`, `type/feature`, `type/docs`
  - `sprint/1`, `sprint/2`, `sprint/3`
  - `status/ready`, `status/in-progress`, `status/review`
  - `area/backend`, `area/frontend`, `area/infra`

---

## ✅ Fase 7: Scripts & Utilities

### Setup Scripts
- [ ] Windows: `scripts\setup-dev.bat` (executar uma vez)
- [ ] Mac/Linux: `bash scripts/setup-dev.sh` (executar uma vez)

### Dev Commands
- [ ] Source: `source scripts/dev.sh`
- [ ] Comandos disponíveis:
  - `dev.sh backend` — Inicia backend
  - `dev.sh frontend` — Inicia frontend
  - `dev.sh lint-backend` — Lint backend
  - `dev.sh format-backend` — Format backend
  - `dev.sh sync` — Sync com main

---

## ✅ Fase 8: Makefile (Opcional)

Para simplificar (em root `Makefile`):

```makefile
.PHONY: setup backend frontend lint format test sync

setup:
	bash scripts/setup-dev.sh

backend:
	cd backend && source venv/bin/activate && uvicorn main:app --reload

frontend:
	cd frontend && npm run dev

lint:
	cd backend && black --check . && isort --check-only . && flake8 .

format:
	cd backend && black . && isort .

test:
	cd backend && pytest

sync:
	git checkout main && git pull origin main --rebase
```

- [ ] Criar `Makefile`
- [ ] Testar: `make backend`, `make frontend`, etc

---

## ✅ Checkup Final

### Local
- [ ] Backend roda em `http://localhost:8000`
- [ ] Frontend roda em `http://localhost:5173`
- [ ] Ambos conectam sem erros
- [ ] Lint passa localmente: `cd backend && flake8 .`
- [ ] Tests passam: `cd backend && pytest`

### GitHub
- [ ] Branch protection configurada para `main`
- [ ] CI/CD workflow rodando
- [ ] Labels criadas
- [ ] CODEOWNERS configurado (se aplicável)

### Documentation
- [ ] Leu: `TRUNK_BASED_DEV_GUIDE.md`
- [ ] Entende: padrão de commits (Conventional Commits)
- [ ] Sabe criar: branches de curta duração
- [ ] Sabe fazer: PRs com descrição clara

### Ready to Start
- [ ] Primeira tarefa identificada (T001, T002, etc)
- [ ] Branch criada: `fix/T00X-...`
- [ ] Primeiro commit feito
- [ ] Primeiro push para GitHub

---

## 📋 Daily Standup Checklist

Ao começar o dia:

```bash
# 1. Sync com main
git checkout main
git pull origin main

# 2. Ver o que foi merged
git log --oneline -n 10

# 3. Criar nova branch
git checkout -b fix/T00X-description

# 4. Desenvolvair & testar
# (seu trabalho aqui)

# 5. Ao fim do dia
git push origin fix/T00X-description
# Abrir PR no GitHub
```

---

## 🚨 Troubleshooting

### Erro: "Your branch is behind main"
```bash
git fetch origin
git rebase origin/main
git push origin <seu-branch> --force-with-lease
```

### Erro: "Permission denied" (pre-commit hook)
```bash
chmod +x .git/hooks/pre-commit
```

### Erro: "Conflicto de merge"
```bash
git fetch origin
git rebase origin/main
# Resolver conflitos manualmente
# Depois: git rebase --continue
```

---

## 📞 Support

Dúvidas? Consulte:
1. `TRUNK_BASED_DEV_GUIDE.md` → Workflow detail
2. `COMMIT_CONVENTIONS.md` → Commit patterns
3. `.github/BRANCH_PROTECTION_RULES.md` → GitHub setup
4. `docs/TASKS.md` → Tarefas e escopo

---

**Status**: ⏳ Setup em progresso  
**Próximo**: Começar Sprint 1 após checklist completo  
**Referência**: Trunk-Based Development at https://trunkbaseddevelopment.com/
