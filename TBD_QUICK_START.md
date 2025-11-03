# 🚀 Quick Start - Trunk-Based Development

**Comece em 5 minutos!**

---

## 1️⃣ Setup Inicial (Primeira Vez)

### Windows
```powershell
.\scripts\setup-dev.bat
```

### Mac/Linux
```bash
bash scripts/setup-dev.sh
```

✅ Pronto! Venv criada, deps instaladas, .env criado.

---

## 2️⃣ Inicie os Servidores

### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate  # ou: .\venv\Scripts\activate (Windows)
uvicorn main:app --reload
```

→ Acesse: http://localhost:8000/docs

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

→ Acesse: http://localhost:5173

---

## 3️⃣ Faça Seu Primeiro Commit

```bash
# 1. Criar branch
git checkout -b fix/T001-fix-sfc

# 2. Fazer mudanças no código...
# (editar arquivo EventsView.vue, etc)

# 3. Adicionar mudanças
git add .

# 4. Commit com padrão
git commit -m "fix(views): remove CSS outside style block"

# 5. Push
git push origin fix/T001-fix-sfc

# 6. Abrir PR no GitHub
# GitHub vai sugerir abrir PR quando você fizer push
```

---

## 4️⃣ Code Review & Merge

1. Descrever mudanças no PR
2. Aguardar checks do GitHub Actions (automático)
3. Solicitar review de alguém
4. Após aprovação: **Squash and merge**
5. Deletar branch

---

## 📚 Documentação Importante

| Arquivo | Para quem | Tempo |
|---------|-----------|-------|
| `TRUNK_BASED_DEV_GUIDE.md` | Todos | 15 min |
| `COMMIT_CONVENTIONS.md` | Quem commita | 10 min |
| `TRUNK_BASED_DEV_CHECKLIST.md` | Team lead | 20 min |
| `.github/BRANCH_PROTECTION_RULES.md` | GitHub admin | 5 min |

---

## 🎯 Padrão de Commits (Obrigatório)

```
<type>(<scope>): <subject>

<optional body>

<optional footer>
```

### Exemplos

✅ `fix(views): remove CSS outside style block`  
✅ `feat(events): add date filter`  
✅ `refactor(api): simplify validation`  
✅ `chore: update dependencies`  

❌ `fixed bug`  
❌ `T001 completed`  
❌ `WIP`  

### Types Disponíveis
- `feat` — nova feature
- `fix` — correção de bug
- `refactor` — refactor sem mudança
- `docs` — documentação
- `test` — testes
- `chore` — deps, build
- `ci` — CI/CD
- `perf` — performance

### Scopes Disponíveis
- `events`, `players`, `matches`, `ranking` (backend)
- `views`, `components`, `services` (frontend)
- `api`, `db`, `models` (genérico)

---

## ⚡ Comandos Úteis

```bash
# Sync com main
git checkout main
git pull origin main --rebase

# Ver branches locais
git branch -v

# Ver commits não-pushados
git log origin/main..HEAD --oneline

# Limpar branches deletados remotamente
git fetch origin --prune

# Ver diffs antes de commit
git diff

# Ver staged changes
git diff --cached

# Desfazer mudanças (último commit)
git reset --soft HEAD~1  # Manter mudanças
git reset --hard HEAD~1  # Deletar mudanças
```

---

## 🚨 Problemas Comuns

### "Your branch is behind"
```bash
git fetch origin
git rebase origin/main
git push origin <branch> --force-with-lease
```

### "Conflicto de merge"
```bash
git fetch origin
git rebase origin/main
# Resolver conflitos manualmente no editor
# git rebase --continue
```

### "Permission denied" (pre-commit hook)
```bash
chmod +x .git/hooks/pre-commit
```

### CI/CD failure
- Ver logs no GitHub Actions (Actions tab)
- Executar `flake8`, `black`, `pytest` localmente
- Fixar erros antes de pushear

---

## 📊 GitHub Setup (Uma Vez)

1. Vá para: **Settings** → **Branches**
2. Clique **Add rule**
3. Branch: `main`
4. Ativar:
   - [x] Require pull request
   - [x] Require status checks
   - [x] Require reviews

Mais detalhes: `.github/BRANCH_PROTECTION_RULES.md`

---

## 🔄 Workflow Típico

```
1. git checkout main
2. git pull origin main
3. git checkout -b fix/T001-xxx

   ← TRABALHAR (horas)

4. git add .
5. git commit -m "fix(xxx): ..."
6. git push origin fix/T001-xxx

   ← GitHub CI/CD roda automaticamente
   ← Code review solicitado

7. Após aprovação: Clique "Squash and merge"
8. Branch é deletado
9. Seu código está no main! 🎉
```

---

## ✅ Checklist: Primeira Semana

- [ ] Executou `scripts/setup-dev.*`
- [ ] Backend e frontend rodando localmente
- [ ] Leu `TRUNK_BASED_DEV_GUIDE.md`
- [ ] Leu `COMMIT_CONVENTIONS.md`
- [ ] Criou primeira branch: `fix/T001-xxx`
- [ ] Fez primeiro commit com padrão
- [ ] Fez primeiro push
- [ ] Abriu primeira PR
- [ ] Recebeu primeira review
- [ ] Fez primeiro merge

---

## 📞 Precisa de Help?

1. **Dúvida sobre workflow?** → `TRUNK_BASED_DEV_GUIDE.md`
2. **Dúvida sobre commits?** → `COMMIT_CONVENTIONS.md`
3. **Setup com problemas?** → `TRUNK_BASED_DEV_CHECKLIST.md`
4. **GitHub config?** → `.github/BRANCH_PROTECTION_RULES.md`
5. **Task específica?** → `docs/TASKS.md`

---

## 🎯 TBD em Uma Frase

> **Uma branch por tarefa, merge rápido, CI/CD confiável, integração contínua.**

---

**Última atualização**: 2025-11-02  
**Próximo passo**: Execute `setup-dev.*` e comece a trabalhar! 🚀
