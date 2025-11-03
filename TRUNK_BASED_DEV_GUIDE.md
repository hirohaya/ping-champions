# 🌳 Trunk-Based Development - Setup Completo

Guia completo para trabalhar com Trunk-Based Development neste projeto.

---

## 📚 Índice

1. [O que é Trunk-Based Development](#o-que-é)
2. [Setup do Repositório](#setup)
3. [Fluxo de Trabalho Diário](#fluxo)
4. [Padrões de Branch](#branches)
5. [Padrões de Commit](#commits)
6. [Code Review](#review)
7. [Deploy](#deploy)
8. [Troubleshooting](#troubleshooting)

---

## O que é Trunk-Based Development {#o-que-é}

**Trunk-Based Development (TBD)** é um padrão de versionamento onde:

- ✅ **Uma única linha de desenvolvimento** (branch `main`)
- ✅ **Branches de curta duração** (< 1 dia)
- ✅ **Múltiplos merges por dia**
- ✅ **Integração contínua** (CI/CD forte)
- ✅ **Confiança no automático** (testes, builds, deploys)

### Quando usar TBD?

| ✅ Ideal para | ❌ Não ideal para |
|--------------|------------------|
| Equipes pequenas (<20) | Grandes times (50+) |
| Deploy frequente | Releases agendadas |
| Microserviços | Monolitos com muitas dependências |
| Ágil/Scrum | Waterfall/Planejamento fixo |
| Confiança em QA automática | Muita dependência de QA manual |

**Este projeto**: ✅ TBD é ideal (pequena equipe, ágil, MVP)

---

## Setup do Repositório {#setup}

### 1. Configuração Git Local

```bash
# Configurar user global (se ainda não fez)
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@github.com"

# Clonar o repositório
git clone https://github.com/hirohaya/ping-champions.git
cd ping-champions

# Verificar remotes
git remote -v
# origin  https://github.com/hirohaya/ping-champions.git (fetch)
# origin  https://github.com/hirohaya/ping-champions.git (push)

# Garantir no branch main
git checkout main
git pull origin main
```

### 2. Configuração GitHub (Settings)

**Vá para: Settings → Branches → Branch protection rule**

**Configurar para branch `main`**:

- [x] Require a pull request before merging
- [x] Require status checks to pass before merging
- [x] Require branches to be up to date before merging
- [x] Require code reviews before merging (1 reviewer mínimo)
- [x] Dismiss stale pull request approvals
- [x] Include administrators

**Status checks obrigatórios**:
- `Validate Code` (todos os Pythons)
- `Validate Frontend`

### 3. Setup Local: Pre-commit Hooks

```bash
# Criar script de pre-commit
mkdir -p .git/hooks

# Criar arquivo
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
set -e

echo "🔍 Running pre-commit checks..."

# Lint Python
if [ -d "backend" ]; then
    echo "  → Checking Python syntax..."
    python -m py_compile backend/**/*.py 2>/dev/null || true
fi

# Lint Node
if [ -d "frontend" ]; then
    echo "  → Checking Node syntax..."
    cd frontend && npm run lint 2>/dev/null || true; cd ..
fi

echo "✅ Pre-commit checks passed!"
exit 0
EOF

chmod +x .git/hooks/pre-commit
```

### 4. Setup Local: Git Aliases (Recomendado)

```bash
# Adicionar aliases úteis
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual 'log --graph --oneline --all'
git config --global alias.sync 'pull --rebase origin main'

# Usar: git sync (ao invés de git pull --rebase origin main)
```

---

## Fluxo de Trabalho Diário {#fluxo}

### 📍 Começar o Dia

```bash
# 1. Atualizar main local
git checkout main
git pull origin main

# 2. Ver o que foi merged desde ontem
git log --oneline -n 10

# 3. Escolher tarefa (ex: T001)
# Procurar em docs/TASKS.md ou GitHub Issues
```

### 🏗️ Criar Feature Branch

```bash
# Nomenclatura: <type>/<ticket-id>-<description>
# Types: feat, fix, refactor, docs, chore

# Exemplo 1: Feature
git checkout -b feat/T001-fix-sfc

# Exemplo 2: Bug fix
git checkout -b fix/T003-orm-cascade

# Exemplo 3: Refactor
git checkout -b refactor/T004-trailing-slashes

# Exemplo 4: Docs
git checkout -b docs/update-readme

# Verificar que está no branch correto
git branch -v
# * feat/T001-fix-sfc        18cccd8 Initial commit
#   main                     18cccd8 Initial commit
```

### ✏️ Trabalhar no Branch

```bash
# Fazer mudanças no código
# (editar arquivo, salvar, etc)

# Verificar status
git status

# Adicionar mudanças
git add <arquivo>          # Um arquivo
git add .                  # Todos (cuidado!)
git add backend/*.py       # Pattern

# Commit com mensagem conventional
git commit -m "fix(views): remove CSS outside style block

CSS was misplaced outside <style> tag, breaking SFC parser
Moved CSS to proper style block"

# Ou commitize (se tiver a extensão VSCode)
# Use Ctrl+Shift+P → Commit

# Ver commits locais não pushados
git log origin/main..HEAD --oneline
```

### 🚀 Push e Pull Request

```bash
# Push branch para GitHub
git push origin feat/T001-fix-sfc
# ou
git push -u origin feat/T001-fix-sfc  # -u: set upstream

# GitHub vai exibir prompt para criar PR
# Clique no link ou vá para: https://github.com/hirohaya/ping-champions/pull/new/feat/T001-fix-sfc

# Template de PR (será auto-preenchido):
#
# ## Description
# Fixes #T001
# 
# ### Changes
# - Removed CSS from outside style block
# - Updated EventsView.vue template
# 
# ### Type of Change
# - [x] Bug fix
# - [ ] New feature
# - [ ] Breaking change
# 
# ### Testing
# - [x] Tested locally
# - [x] No errors in console
# 
# ### Checklist
# - [x] My code follows the style guidelines
# - [x] I have updated documentation
# - [x] I have run tests locally
```

### 👀 Code Review

```bash
# Enquanto aguarda review:

# 1. Se receber pedido de mudanças:
#    → Fazer as mudanças no mesmo branch
#    → git add, git commit, git push
#    → Responder comentário no GitHub ("Done" ou detalhe)

# 2. Se tiver conflitos:
git fetch origin
git rebase origin/main

# Se conflito, resolver:
# - Abrir arquivo
# - Encontrar marcadores <<<<<<, ======, >>>>>>
# - Escolher qual versão manter
# - git add <arquivo>
# - git rebase --continue

# 3. Manter atualizado com main:
git fetch origin
git rebase origin/main
git push origin feat/T001-fix-sfc --force-with-lease
```

### ✅ Após Aprovação

```bash
# Opção 1: Squash (Recomendado para TBD)
# → GitHub faz automaticamente se configurado
# → Clique "Squash and merge"

# Opção 2: Manual (se preferir)
git checkout main
git pull origin main
git merge --squash feat/T001-fix-sfc
git commit -m "fix(views): remove CSS outside style block

CSS was misplaced outside <style> tag, breaking SFC parser
Moved CSS to proper style block

Fixes #T001"

git push origin main

# Opção 3: GitHub faz tudo
# → Clique "Merge pull request"
# → Clique "Confirm merge"
# → Clique "Delete branch"

# Depois, limpar localmente:
git checkout main
git pull origin main
git branch -d feat/T001-fix-sfc  # Delete local
# GitHub deletará o branch remoto automaticamente
```

---

## Padrões de Branch {#branches}

### Nomenclatura

```
<type>/<ticket-id>-<short-description>

Examples:
  feat/T001-fix-sfc
  fix/T003-orm-relationship
  refactor/T004-api-consistency
  docs/setup-guide
  chore/update-deps
```

### Duração de Branches

| Duração | Situação | Ação |
|---------|----------|------|
| < 4 horas | Normal | Continuar |
| 4-8 horas | Longo | Considerar split |
| 1 dia | Muito longo | ⚠️ Precisa refactor |
| > 2 dias | Crítico | 🚨 Está errado algo |

### Deletar Branches Antigos

```bash
# Ver branches locais mortos (não deletados)
git branch -v

# Deletar localmente
git branch -d <branch>
git branch -D <branch>  # Força

# Deletar no remoto
git push origin --delete <branch>

# Limpar branches deletados remotamente
git fetch origin --prune
# ou
git remote prune origin
```

---

## Padrões de Commit {#commits}

Ver **COMMIT_CONVENTIONS.md** para detalhes completos.

### Quick Reference

```
feat(scope): description    → Nova feature
fix(scope): description     → Bug fix
refactor(scope): description → Refactor sem mudança de comportamento
docs: description           → Apenas documentação
test: description           → Testes
chore: description          → Deps, build, etc
style: description          → Formatação
ci: description             → CI/CD
```

### Boas Práticas

✅ Commits pequenos (1 mudança por commit)  
✅ Mensagens descritivas  
✅ Imperative mood ("add", "remove", não "added", "removed")  
✅ Referencie issues: "Fixes #123"  
✅ Sem commits "wip", "debug", "temp"  

---

## Code Review {#review}

### Para Quem Submete PR

```markdown
# Pull Request Template

## Description
Breve descrição do que foi feito

## Related Issues
Fixes #T001
Related #T002

## Type of Change
- [x] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [x] Tested locally
- [ ] Added unit tests
- [ ] Manual testing done

## Checklist
- [x] Code follows style guidelines
- [x] No new warnings
- [x] Documentation updated
- [x] Tests passing
```

### Para Quem Revisa

```
✅ Sempre fazer review em <24h
✅ Deixar comentários construtivos
✅ Usar "Request changes" apenas para blockers
✅ Usar "Comment" para sugestões não-bloqueantes
✅ Fazer "Approve" quando OK
✅ Revisar: lógica, testes, segurança, performance
```

### Resolver Comentários

```
1. Se concorda: faz a mudança + push
2. Se discorda: explica no comentário (thread)
3. Após resolver: marca como "Resolved" no GitHub
4. Responde ao reviewer em cima do comentário
```

---

## Deploy {#deploy}

### Fase 1: Local (Sprint 1-4)

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate (Windows)
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (novo terminal)
cd frontend
npm install
npm run dev

# Teste em http://localhost:5173
```

### Fase 2: CI/CD (Sprint 5)

Configurado em `.github/workflows/trunk-based-dev.yml`

Runs automaticamente:
- ✅ Linting (flake8, eslint)
- ✅ Testes (pytest, jest)
- ✅ Build (Vite, Python)
- ✅ Coverage report

### Fase 3: Deploy Automático (Sprint 6)

Será configurado em:
- Staging automático no main
- Deploy em produção com aprovação manual

---

## Troubleshooting {#troubleshooting}

### Problema: "Your branch is behind..."

```bash
git fetch origin
git rebase origin/main
git push origin <seu-branch> --force-with-lease
```

### Problema: Merge Conflict

```bash
# Ver conflitos
git status

# Abrir arquivo e resolver manualmente
# Procurar por: <<<<<<<, =======, >>>>>>>

# Após resolver
git add <arquivo>
git rebase --continue  # se em rebase
# ou
git commit            # se em merge
```

### Problema: Precisa voltar commits

```bash
# Ver commits
git log --oneline -n 5

# Voltar 1 commit (mantendo mudanças)
git reset --soft HEAD~1

# Voltar 1 commit (deletando mudanças)
git reset --hard HEAD~1

# Voltar para commit específico
git reset --hard <hash>
```

### Problema: Deletou branch por acidente

```bash
# Ver histórico de deletes
git reflog

# Recuperar
git checkout -b <branch> <hash-do-reflog>
```

### Problema: PR não pode fazer merge (conflito)

```bash
git checkout main
git pull origin main
git checkout seu-branch
git rebase origin/main
# Resolver conflitos
git rebase --continue
git push origin seu-branch --force-with-lease
# PR agora pode fazer merge
```

---

## 📋 Checklist: Primeira Semana

- [ ] Clonar repositório
- [ ] Configurar branch protection no GitHub
- [ ] Configurar git aliases localmente
- [ ] Ler COMMIT_CONVENTIONS.md
- [ ] Criar primeira branch: `feat/T001-fix-sfc`
- [ ] Fazer primeiro commit com padrão conventional
- [ ] Abrir primeira PR
- [ ] Receber primeira review
- [ ] Fazer primeira merge

---

## 📚 Referências

- [Trunk-Based Development](https://trunkbaseddevelopment.com/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Pro Git Book](https://git-scm.com/book/en/v2)

---

## ❓ Dúvidas?

Ver também:
- `COMMIT_CONVENTIONS.md` — Padrão de mensagens de commit
- `.github/workflows/trunk-based-dev.yml` — Automações CI/CD
- `docs/TASKS.md` — Tarefas priorizadas
- `README.md` → Links de documentação

**Última atualização**: 2025-11-02  
**Versão**: 1.0
