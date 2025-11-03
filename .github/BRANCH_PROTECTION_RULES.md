# Branch Protection Rules for Main

Este arquivo documenta as regras de proteção do branch `main` que devem ser configuradas no GitHub.

## 🔒 Configuração Recomendada para Trunk-Based Development

### 1. Regra Base
- **Branch**: `main`
- **Aplicar a**: Repositório inteiro

### 2. Requisitos de Pull Request

#### ✅ Requer Pull Requests
- [x] Requer pull request antes de merge
- [x] Dismiss stale pull request approvals when new commits are pushed
- [x] Require approval of the most recent reviewable push
- [ ] Require code owners approval (configurar se tiver CODEOWNERS)

#### ✅ Requisitos de Status
- [x] Require branches to be up to date before merging
- [x] Require status checks to pass before merging

**Status Checks Obrigatórios**:
- `Validate Code` (Python 3.9, 3.10, 3.11)
- `Validate Frontend` (Node.js)
- `Build success`
- `All tests passing`

### 3. Restrições Administrativas

- [x] Include administrators
  - Mesmo admins devem seguir as regras de proteção
  
- [x] Restrict who can push to matching branches
  - Apenas code owners podem fazer push para PRs

- [x] Allow force pushes
  - [ ] Não permitir (recomendado para trunk-based dev)
  
- [x] Allow deletions
  - [ ] Não permitir (proteger contra acidentes)

### 4. Configuração de Merge

- [x] Allow merge commits (com squash/rebase como alternativas)
- [ ] Require linear history (para manter histórico limpo)
- [x] Require conversation resolution before merging
- [x] Require deployments to succeed before merging (opcional)

### 5. Dismissal Rules

- [x] Require dismissal of stale pull request reviews
- [x] Restrict who can dismiss
  - Apenas: repo maintainers + authors

---

## 🔧 Como Configurar via GitHub UI

1. Vá para: **Settings** → **Branches**
2. Clique em **Add rule**
3. Branch name pattern: `main`
4. Configure cada opção conforme acima
5. Clique em **Create**

---

## 📋 Checklist de Setup

- [ ] Configurar regras de proteção via GitHub UI
- [ ] Adicionar pelo menos 1 code owner (CODEOWNERS)
- [ ] Criar GitHub Teams (Frontend, Backend, DevOps)
- [ ] Configurar notificações de PR reviews
- [ ] Treinar time no workflow trunk-based

---

## 📝 Workflow Esperado

```
1. Developer cria branch de curta duração
   → git checkout -b feature/T001-fix-sfc

2. Faz commits pequeninhos com mensagens claras
   → git commit -m "fix: remove CSS from template in EventsView"

3. Push para GitHub e abre Pull Request
   → git push origin feature/T001-fix-sfc

4. GitHub Actions roda automaticamente
   ✅ Lint
   ✅ Tests
   ✅ Build
   ✅ Coverage

5. Code review aprovado
   → Comentários resolvidos
   → Pelo menos 1 aprovação

6. Merge automático ou manual
   → PR é squashed/rebased no main
   → Branch de feature é deletado

7. Deploy automático (em Sprint 6)
   → Status checks no main
   → Deploy para staging/prod
```

---

## 🚨 Por que Trunk-Based Development?

| Aspecto | Trunk-Based | Git-Flow |
|--------|------------|----------|
| **Frequência de Merge** | Múltiplos x por dia | Quando feature termina |
| **Duração de branch** | Horas | Dias/Semanas |
| **Integração** | Contínua | Periódica |
| **Complexidade** | Baixa | Alta |
| **Confiança em CI/CD** | Alta (necessária) | Baixa (opcional) |
| **Ideal para** | Equipes ágeis | Releases predefinidos |

---

## 📚 Referências

- [Trunk-Based Development](https://trunkbaseddevelopment.com/)
- [GitHub Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
- [Conventional Commits](https://www.conventionalcommits.org/)
