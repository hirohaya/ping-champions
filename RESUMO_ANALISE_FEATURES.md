# Resumo Executivo - Análise de Features

**Data:** 13 de novembro de 2025  
**Revisão:** Crítica Construtiva + Avaliação Técnica

---

## 📌 TL;DR (Resumo Ultra-Curto)

- **Feature 1**: Boa visão, mas incompleta em detalhes (ranking, tipos de torneio)
- **Feature 2**: Muito vaga, precisa RBAC explícito e permissões granulares
- **Feature 3**: Homepage boa ideia, requer clareza em quais dados mostrar por grupo
- **Tempo estimado**: 8-12 semanas (com complexidade alta)

---

## 🚨 Problemas Críticos por Feature

### Feature 1: Organização de Partidas

**❌ Problema 1: Cálculo de Ranking Indefinido**
- Qual algoritmo? (ELO, Pontos, Win Rate?)
- Quando recalcula? (a cada partida, diariamente, sob demanda?)
- Impacta performance se 10k+ jogadores

**✅ Solução:**
```yaml
Configuração por Grupo:
  formula: "elo"  # elo, points, winrate
  k_factor: 32
  atualiza_em: "batch_diario"  # ou realtime com cache
  minimo_partidas_qualificar: 5
```

---

**❌ Problema 2: Tipos de Torneio Vagos**
- "Eliminatório simples por chaves" = 8, 16, 32 chaves?
- "Fase de grupos + eliminatório" = Como sorteia grupos?
- "Rodada Suíça" = Muito complexo, precisa algoritmo específico

**✅ Solução:**
```python
TIPOS_TORNEIO = {
    "SIMPLES": {
        "descricao": "1v1 direto",
        "config": {"minimo_jogadores": 2}
    },
    "ELIMINATORIO": {
        "descricao": "Árvore binária (8, 16, 32, 64 jogadores)",
        "config": {"tamanho_chave": [8, 16, 32, 64]}
    },
    "FASE_GRUPOS": {
        "descricao": "Grupos → Playoffs",
        "config": {
            "tamanho_grupo": 4,  # 4 jogadores por grupo
            "qualificam": 2,     # top 2 avançam
            "total_grupos": "auto"  # calculado automaticamente
        }
    },
    "SUICA": {
        "descricao": "Pareamento dinâmico (complexo)",
        "config": {"algoritmo": "dutch_system", "rodadas": 5}
    }
}
```

---

**❌ Problema 3: Memberships Sem Timeline**
- Jogador sai do grupo em março, mas tem eventos em janeiro
- Ranking dele deve contar ou não?
- Precisa `data_entrada` e `data_saida`

**✅ Solução:**
```sql
ALTER TABLE grupo_membership ADD COLUMN data_entrada DATETIME DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE grupo_membership ADD COLUMN data_saida DATETIME NULL;
ALTER TABLE grupo_membership ADD COLUMN status ENUM('ativo', 'inativo', 'suspenso');
```

---

### Feature 2: Usuários e RBAC

**❌ Problema 1: Roles Pouco Claros**
- "Administrado" parece typo
- Qual é a diferença entre Admin Global vs Admin do Grupo?

**✅ Solução:**
```python
class RoleEnum(str, Enum):
    SUPERADMIN = "superadmin"        # 🔑 Controla tudo (1-2 pessoas)
    ADMIN_GRUPO = "admin_grupo"      # Gerencia 1 grupo
    ORGANIZADOR = "organizador"      # Cria eventos (dentro do grupo)
    JOGADOR = "jogador"              # Participa
```

---

**❌ Problema 2: Permissões Não Especificadas**
- Um jogador pode se remover de um evento iniciado?
- Organizador pode deletar evento?
- Precisa matriz explícita

**✅ Solução:**
```python
# use django-guardian ou similar
@requires_permission("evento", "criar", escopo="grupo")
def criar_evento(grupo_id):
    pass

# ou matrix explícita:
PERMISSIONS = {
    "jogador": ["se_inscrever_evento", "ver_ranking"],
    "organizador": ["criar_evento", "registrar_partida"],
    "admin_grupo": ["deletar_evento", "editar_ranking"],
    "superadmin": ["tudo"]
}
```

---

**❌ Problema 3: Autenticação Não Mencionada**
- JWT? Sessions? OAuth?
- Refresh tokens?
- SSO (Single Sign-On)?

**✅ Solução (Recomendada):**
```python
# JWT com refresh tokens (padrão moderno)
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "senha": "..."
}

Response:
{
  "access_token": "eyJ...",      # válido por 15 min
  "refresh_token": "eyJ...",     # válido por 7 dias
  "usuario": { "id": 1, "nome": "...", "role": "..." }
}
```

---

### Feature 3: Homepage

**❌ Problema: Qual Informação Mostrar?**
- Rankings de TODOS os grupos ou apenas do grupo selecionado?
- Eventos de qual grupo?
- Isso afeta muito o design

**✅ Solução:**
```vue
<!-- Modelo proposto -->
<template>
  <div class="dashboard">
    <!-- Seletor de Grupo (novo) -->
    <GroupSelector :grupos="meus_grupos" @selectar="grupo_ativo = $event" />
    
    <!-- Próximos Eventos (do grupo selecionado) -->
    <ProximosEventos :grupo_id="grupo_ativo" />
    
    <!-- Meu Ranking (só deste grupo) -->
    <MeuRanking :grupo_id="grupo_ativo" />
    
    <!-- Se Organizador: Ações de Gestão -->
    <ActualizarOrganizador v-if="eh_organizador" :grupo_id="grupo_ativo" />
  </div>
</template>
```

---

## 📊 Matriz de Decisão

| Aspecto | Status | Próximo Passo |
|--------|--------|--------------|
| Hierarquia Grupo→Evento | ✅ Bom | Implementar |
| Cálculo de Ranking | ⚠️ Incompleto | Definir em Sprint 1 |
| Tipos de Torneio | ⚠️ Vago | Detalhar configurações |
| Memberships | ⚠️ Sem timeline | Adicionar data_entrada/data_saida |
| RBAC | ❌ Vago | Criar matriz de permissões |
| Autenticação | ❌ Não mencionada | Implementar JWT |
| Homepage | ✅ Bom | Desenvolver componentes |

---

## 🗂️ Ordem de Implementação Sugerida

### Sprint 1: Foundation (2 semanas)
- [ ] Criar tabelas: Grupos, GrupoMembership, UsuarioGrupoRole
- [ ] Implementar JWT + refresh tokens
- [ ] Setup Django-Guardian ou similar para permissões
- [ ] Testes de RBAC

### Sprint 2: Core Features (2 semanas)
- [ ] Endpoints CRUD para Grupos
- [ ] Endpoints CRUD para Eventos (com tipo_torneio)
- [ ] Sistema de ranking básico (ELO)
- [ ] Auditoria (AuditLog)

### Sprint 3: Frontend (2 semanas)
- [ ] GroupSelector.vue
- [ ] EventosProximos.vue
- [ ] RankingResumido.vue
- [ ] Nova Homepage

### Sprint 4: Tipos de Torneio (2 semanas)
- [ ] Algoritmo Eliminatório
- [ ] Algoritmo Fase de Grupos
- [ ] Algoritmo Rodada Suíça (opcional)
- [ ] Testes E2E

---

## 💡 Quick Wins (Implementar Rápido)

1. **Adicionar `data_entrada` a memberships** (5 min)
   - Quebra compatibilidade? Não, é nullable
   
2. **Criar enum ROLE_HIERARCHY** (15 min)
   - Clarifica visão de usuários
   
3. **Documentar matriz de permissões** (1 hora)
   - Guia para desenvolvimento
   
4. **Criar arquivo de configuração de torneios** (2 horas)
   - Tipos de torneio em YAML/JSON

---

## 📚 Documentação Necessária

- [ ] Especificação técnica completa (14 páginas já criadas)
- [ ] Diagrama ER (Models)
- [ ] Diagrama de fluxo (Usuários, Permissões)
- [ ] API Specification (OpenAPI/Swagger)
- [ ] Guia de Desenvolvimento (como adicionar novo tipo de torneio)
- [ ] Plano de Migração (manter dados atuais)

---

## 🎯 Conclusão

As features têm **visão excelente**, mas precisam:
1. **Clareza em detalhes** (ranking, permissões, tipos de torneio)
2. **Especificação técnica** (que já foi criada)
3. **Implementação em fases** (não tudo ao mesmo tempo)

**Risco principal:** Implementar Feature 2 (RBAC) de forma incompleta → problemas de segurança depois.

**Recomendação final:** Começar por Sprint 1, validar com stakeholders, depois seguir sprints.
