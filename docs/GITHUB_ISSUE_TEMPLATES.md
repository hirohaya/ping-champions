# GitHub Issues — Templates para Tarefas do Roadmap

Copie e cole os templates abaixo no seu repositório GitHub (`.github/ISSUE_TEMPLATE/`).

---

## Template 1: Task

**Arquivo**: `.github/ISSUE_TEMPLATE/task.md`

```markdown
---
name: Task
about: Tarefa do roadmap de desenvolvimento
title: 'T### - [Título]'
labels: 'type/task'
---

## ID e Prioridade
- **ID**: T### (referência em docs/TASKS.md)
- **Prioridade**: P[0-3]
- **Sprint**: [Sprint N]
- **Esforço estimado**: [Xh ou Xy]

## Escopo
[Descrição concisa da tarefa]

## Critérios de Aceite
- [ ] Critério 1
- [ ] Critério 2
- [ ] Critério 3

## Arquivos Envolvidos
- `path/to/file1.py`
- `path/to/file2.vue`

## Dependências
- [ ] T00Y (se aplicável)

## Checklist para Implementação
- [ ] Código escrito e testado localmente
- [ ] Linting passa (`ruff check`, `eslint`)
- [ ] Testes adicionados/atualizados
- [ ] Documentação atualizada (README, docstrings)
- [ ] PR aberta com referência a esta issue
- [ ] Code review aprovado
- [ ] Merge realizado

## Notas adicionais
[Contexto, perguntas, ou refs a outros issues]
```

---

## Template 2: Bug

**Arquivo**: `.github/ISSUE_TEMPLATE/bug.md`

```markdown
---
name: Bug
about: Relatar um bug encontrado
title: 'BUG - [Descrição breve]'
labels: 'type/bug'
---

## Descrição
[Descrição clara do bug]

## Passos para Reproduzir
1. [Passo 1]
2. [Passo 2]
3. [etc.]

## Comportamento Esperado
[O que deveria acontecer]

## Comportamento Atual
[O que está acontecendo]

## Ambiente
- **OS**: [Windows/Mac/Linux]
- **Node version**: [ex: 20.19.0]
- **Python version**: [ex: 3.11]

## Logs / Screenshots
[Adicione logs ou imagens se houver]

## Relacionado a
- Task T### (se aplicável)

## Prioridade
[ ] P0 (crítico) [ ] P1 (alta) [ ] P2 (média) [ ] P3 (baixa)
```

---

## Template 3: Feature Request

**Arquivo**: `.github/ISSUE_TEMPLATE/feature.md`

```markdown
---
name: Feature Request
about: Sugerir uma nova feature
title: 'FEAT - [Descrição breve]'
labels: 'type/feature'
---

## Descrição da Feature
[Descrição clara e concisa]

## Por quê?
[Justificativa: por que esta feature seria útil?]

## Possível Implementação
[Se você tiver ideias de como implementar, descreva]

## Impacto Estimado
- Complexidade: [baixa/média/alta]
- Esforço: [Xh ou Xy]
- Bloqueadores/Dependências: [T###, outras features]

## Relacionado a
- [Links a issues, PRs ou documentação]

## Prioridade Sugerida
[ ] P0 (crítico) [ ] P1 (alta) [ ] P2 (média) [ ] P3 (baixa)
```

---

## Como usar

1. Copie os templates acima para `.github/ISSUE_TEMPLATE/` no seu repositório.
2. Nomeie os arquivos: `task.md`, `bug.md`, `feature.md`.
3. Ao criar uma nova issue, GitHub oferecerá esses templates como opção.

### Exemplo prático (criar T001):

**Title**: `T001 - Corrigir SFC em EventsView.vue`

**Body**:
```markdown
## ID e Prioridade
- **ID**: T001
- **Prioridade**: P0 (build está em risco)
- **Sprint**: 1
- **Esforço estimado**: 15m

## Escopo
Mover CSS fora de `<style>` para um bloco `<style scoped>` válido no final do componente Vue.
Remover trechos Python ou código morto não pertencente a Vue.

## Critérios de Aceite
- [ ] `npm run build` roda sem erros ou avisos de SFC.
- [ ] `npm run dev` carrega a página de eventos sem console errors.
- [ ] Componente exibe corretamente com estilos aplicados.

## Arquivos Envolvidos
- `frontend/src/views/EventsView.vue`

## Dependências
- Nenhuma

## Checklist para Implementação
- [ ] Código escrito e testado localmente
- [ ] Linting passa (`eslint`)
- [ ] PR aberta com referência a T001
- [ ] Code review aprovado
- [ ] Merge realizado

## Notas adicionais
Arquivo contém CSS dentro do bloco `<template>` em vez de um `<style>` válido.
Veja linhas 1-30 de `EventsView.vue` para detalhes.
```

---

## Labels sugeridos

Adicione estes labels ao seu repositório GitHub:

| Label | Cor | Uso |
|-------|-----|-----|
| `type/task` | `#0075ca` | Tarefa do roadmap |
| `type/bug` | `#d73a4a` | Bug encontrado |
| `type/feature` | `#a2eeef` | Feature request |
| `priority/p0` | `#ff0000` | Crítico |
| `priority/p1` | `#ff9900` | Alta |
| `priority/p2` | `#ffff00` | Média |
| `priority/p3` | `#cccccc` | Baixa |
| `status/in-progress` | `#1f883d` | Em progresso |
| `status/ready-for-review` | `#9e6a03` | Pronto para review |
| `status/blocked` | `#8b3535` | Bloqueado |
| `sprint/1` | `#6f42c1` | Sprint 1 |
| `sprint/2` | `#5a0099` | Sprint 2 |
| `sprint/3` | `#003d99` | Sprint 3 |
| `sprint/4` | `#006699` | Sprint 4 |
| `sprint/5+` | `#003d66` | Sprint 5+ |
| `area/backend` | `#c2e0c6` | Afeta backend |
| `area/frontend` | `#bfdadc` | Afeta frontend |
| `area/docs` | `#f7e4d8` | Documentação |
| `area/infra` | `#d4c5f9` | Infra/DevOps |

---

## Workflow recomendado (GitHub)

1. **Abrir issue**:
   - Dev pega tarefa de Sprint.
   - Cria issue com T### no title.
   - Atribui a si mesmo + adiciona label `sprint/N`, `priority/PN`.

2. **Criar branch**:
   ```bash
   git checkout -b feat/T001-fix-eventview-sfc
   ```

3. **Implementar**:
   - Segue critérios de aceite.
   - Faz commits com ref a issue: `git commit -m "T001: move CSS to <style> block"`

4. **Abrir PR**:
   - PR title: `[T001] Corrigir SFC em EventsView.vue`
   - PR body: `Closes #123` (numero da issue)
   - Adiciona label `status/ready-for-review`

5. **Review**:
   - Code review aprova/sugere mudanças.
   - CI passa (lint, testes).

6. **Merge**:
   - Merge PR.
   - Issue fecha automaticamente (via `Closes`).
   - Label muda para `status/done` (opcional, GitHub fecha automaticamente).

---

## Dashboard (exemplo de query)

Para acompanhar progresso, use estas URLs no GitHub:

- **Todas as tasks**: `https://github.com/[user]/ping-champions/issues?labels=type/task&sort=created&direction=asc`
- **Sprint 1**: `https://github.com/[user]/ping-champions/issues?labels=sprint/1`
- **P0 (crítico)**: `https://github.com/[user]/ping-champions/issues?labels=priority/p0`
- **Em progresso**: `https://github.com/[user]/ping-champions/issues?labels=status/in-progress`

Ou use um **GitHub Project** (beta) para kanban visual.

---

**Última atualização**: 2025-11-02
