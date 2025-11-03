# Commit Conventions - Trunk-Based Development

Guia de padrão de commits para este projeto.

## 📝 Formato de Commit

Usaremos **Conventional Commits** para manter histórico limpo e automatizar versionamento.

### Estrutura

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Exemplo Completo

```
feat(events): add event filtering by date

- Implement date range filter in GET /events endpoint
- Add validation for date format
- Update EventsView component to use new filter

Closes #T001
```

---

## 🏷️ Types de Commit

| Type | Descrição | Exemplo |
|------|-----------|---------|
| `feat` | Nova feature | `feat(players): add ranking score` |
| `fix` | Correção de bug | `fix(events): remove cascade orphan` |
| `refactor` | Mudança sem alterar comportamento | `refactor(api): simplify validation` |
| `perf` | Melhoria de performance | `perf(ranking): cache query results` |
| `test` | Adicionar/alterar testes | `test(players): add registration tests` |
| `docs` | Apenas documentação | `docs: update README setup steps` |
| `style` | Formatação, espaçamento, etc | `style: format imports with black` |
| `chore` | Dependências, build, CI/CD | `chore: update requirements.txt` |
| `ci` | Mudanças em CI/CD | `ci: add linting workflow` |

---

## 🎯 Scopes Aceitos

Para este projeto:

### Backend
- `events` — Tudo relacionado a eventos
- `players` — Tudo relacionado a jogadores
- `matches` — Tudo relacionado a partidas
- `ranking` — Tudo relacionado a ranking
- `api` — Configuração geral da API (CORS, auth, etc)
- `db` — Database e ORM
- `models` — Data models
- `routers` — Route handlers

### Frontend
- `components` — Vue components
- `views` — Page components
- `services` — API services
- `router` — Vue Router
- `assets` — CSS, images
- `ui` — UI library/styling

### Infra
- `docker` — Docker files
- `ci` — GitHub Actions
- `deps` — Dependências

### Transversal
- `docs` — Documentação
- `build` — Build setup
- `config` — Configuração geral

---

## 📋 Regras Importantes

### 1️⃣ Subject (Primeira linha)

```
❌ ERRADO: Fixed the bug with events not showing up
✅ CORRETO: fix(events): display events on page load

❌ ERRADO: feat: T001 and T002 completed
✅ CORRETO: feat(events): add filtering; feat(players): validate email

❌ ERRADO: fix(api): bug fixes
✅ CORRETO: fix(api): handle null timestamps gracefully
```

**Regras**:
- Imperative: "add", "fix", "refactor" (não "adds", "added", "fixing")
- Minúsculo (exceto nomes próprios)
- Sem ponto final
- Máximo 50 caracteres
- Específico (não genérico)

### 2️⃣ Body (Opcional, mas recomendado)

```
- Explique O QUÊ foi mudado e POR QUÊ
- Máximo 72 caracteres por linha
- Deixe linha em branco entre subject e body
- Use bullet points para múltiplas mudanças
```

### 3️⃣ Footer (Para referências)

```
Closes #123          (fecha a issue)
Fixes #456           (corrige a issue)
Related-To #789      (relacionado com)
Co-Authored-By: Name <email>  (co-autor)
Breaking-Change: descrição (breaking change)
```

---

## 🔄 Exemplo Real - Trunk-Based Dev

### Sprint 1 - Task T001: Fix SFC Error

```bash
# Branch de curta duração
git checkout -b fix/T001-sfc-error

# Commit 1: Identificar o problema
git commit -m "fix(views): remove misplaced CSS in EventsView

CSS was outside <style> block causing SFC parser error
Moving CSS to proper <style> block"

# Commit 2: Limpar outros arquivos se necessário
git commit -m "chore(frontend): clean up commented code

Remove old CSS comments from EventsView"

# Push e criar PR
git push origin fix/T001-sfc-error
# [Abrir PR no GitHub]

# Após aprovação e reviews resolvidos
git switch main
git pull origin main
git merge --squash fix/T001-sfc-error
git commit -m "fix(views): remove misplaced CSS in EventsView

CSS was outside <style> block causing SFC parser error
Fixes #T001"

git push origin main
git branch -d fix/T001-sfc-error
git push origin --delete fix/T001-sfc-error
```

### Sprint 1 - Task T004: Trailing Slashes

```bash
git checkout -b fix/T004-trailing-slashes

# Múltiplos commits, cada um refactorando um router
git commit -m "fix(routers): standardize trailing slashes in events

Remove trailing slash from /events/create/ → /events/create
Update all DELETE endpoints for consistency"

git commit -m "fix(routers): standardize trailing slashes in players

Apply /players endpoint consistency
Remove trailing slash from POST endpoints"

git commit -m "fix(routers): standardize trailing slashes in matches

Standardize /matches endpoints"

git commit -m "fix(services): update frontend URLs for new endpoints

Update axios calls to match new endpoint paths"

# Push com todos os commits
git push origin fix/T004-trailing-slashes
# [Abrir PR, reviews, etc]

# Após merge: squash final
git merge --squash fix/T004-trailing-slashes
git commit -m "fix(api): standardize trailing slashes across endpoints

- Events: /events/create → /events/create
- Players: remove trailing slashes from DELETE
- Matches: standardize naming
- Services: update frontend URLs

Fixes #T004"

git push origin main
```

---

## 🚀 Ferramentas Auxiliares

### Pre-commit Hook (Automático)

Crie `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Check commit message format

MSG=$(cat "$1")
PATTERN="^(feat|fix|refactor|perf|test|docs|style|chore|ci)(\(.+\))?!?: .+"

if ! echo "$MSG" | grep -qE "$PATTERN"; then
    echo "❌ Commit message não segue Conventional Commits!"
    echo "Padrão: <type>(<scope>): <subject>"
    exit 1
fi

if echo "$MSG" | head -1 | grep -qE ".{51,}"; then
    echo "❌ Primeira linha deve ter ≤ 50 caracteres"
    exit 1
fi
```

### VSCode Extension

Instale: **Conventional Commits** por vivaxy

```json
// settings.json
"conventionalCommits.scopes": [
  "events",
  "players",
  "matches",
  "ranking",
  "api",
  "db",
  "models",
  "routers",
  "components",
  "views",
  "services",
  "router",
  "assets",
  "docs",
  "ci"
]
```

---

## 📊 Benefícios do Padrão

✅ **Histórico legível** — Fácil entender o que foi feito  
✅ **Changelog automático** — Gerar releases automaticamente  
✅ **Versionamento semântico** — `feat` = minor, `fix` = patch  
✅ **Busca no git** — `git log --grep="feat(players)"`  
✅ **Integração com CI/CD** — Automações baseadas em tipo  

---

## 🔗 Referências

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Angular Commit Guidelines](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit)
- [Commitizen (CLI tool)](http://commitizen.github.io/cz-cli/)
