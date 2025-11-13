# Análise de Features - Refatoração Ping Champions

**Data:** 13 de novembro de 2025  
**Status:** Em revisão  
**Objetivo:** Avaliação técnica e refinamento de 3 features propostas para internet

---

## 📋 FEATURE 1: Nova Estrutura de Organização de Partidas

### 🎯 Visão Geral

Propõe uma hierarquia de dois níveis (Grupo → Evento) com isolamento de rankings por grupo.

```
Grupo
├── Evento 1
│   ├── Partidas
│   └── Rankings (isolados)
├── Evento 2
│   ├── Partidas
│   └── Rankings (isolados)
└── Evento N
    └── ...

Jogador
├── Pertence ao Grupo 1 → Rankings separados
├── Pertence ao Grupo 2 → Rankings separados
└── Pertence ao Grupo N → Rankings separados
```

### ✅ Pontos Positivos

1. **Isolamento de dados bem definido**: Separação clara entre escopos impede vazamento de dados entre grupos
2. **Escalabilidade**: Suporta N grupos sem degradação de performance
3. **Flexibilidade**: Jogador pode participar de múltiplos contextos
4. **Lógica de negócio clara**: Hierarquia intuitiva para usuários finais

### ⚠️ Problemas Identificados

#### 1. **Ambiguidade no Termo "Organização"**
- Problema: "Eventos podem conter as seguintes formas" vs "Jogadores devem estar atrelados a grupos"
- Clarificação necessária: Partidas (matches simples) existem NO EVENTO ou NO GRUPO?
- **Recomendação:** Definir explicitamente que partidas pertencem a eventos, não a grupos

#### 2. **Falta de Clareza na Gestão de Membros**
- Problema: Como um jogador entra em um grupo?
  - Convite do organizador?
  - Auto-registro?
  - Aprovação necessária?
- Problema: O que acontece se um jogador é removido de um grupo?
  - Rankings históricos são preservados?
  - Pode reentrar depois?
- **Recomendação:** Definir ciclo de vida completo da membership

#### 3. **Problema de Timestamp e Histórico**
- Problema: Se um jogador era membro do Grupo A em Jan/2025 e saiu em Mar/2025, seus eventos históricos contam?
- **Recomendação:** Adicionar `data_entrada` e `data_saida` na tabela de membership
  
```sql
GROUP_MEMBERSHIP (
  id PRIMARY KEY,
  jogador_id FK,
  grupo_id FK,
  data_entrada DATETIME,
  data_saida DATETIME NULL,  -- NULL = membro ativo
  status ENUM('ativo', 'inativo', 'suspenso')
)
```

#### 4. **Tipos de Partidas Incompletamente Especificados**
- Problema: "Torneio eliminatório simples por chaves" é vago
  - Quantos chaves? (8, 16, 32 jogadores?)
  - O que diferencia de "Rodada Suíça"?
- Problema: "Fase de grupos seguido por eliminatório simples"
  - Como grupos são formados? (automático, manual, sorteio?)
  - Critério de promoção?

| Tipo | Estrutura | Casos de Uso | Complexidade |
|------|-----------|-------------|--------------|
| **Partidas Simples** | 1v1 direto | Treinamento, casual | Baixa |
| **Eliminatório Simples** | Árvore binária | Torneios rápidos | Média |
| **Fase+Eliminatório** | Grupos → Playoffs | Campeonato de longa duração | Alta |
| **Rodada Suíça** | Pareamento dinâmico | Jogadores variados | Muito Alta |

**Recomendação:** Especificar regras para cada tipo na Feature 1 ou criar Feature 1.5

#### 5. **Cálculo de Ranking Incompleto**
- Problema: Como o ranking é recalculado?
  - A cada partida? (custo computacional)
  - Diariamente? (dados desatualizados)
  - Sob demanda? (lentidão para usuário)
- Problema: Formula de cálculo não especificada
  - ELO? (qual K-factor?)
  - Win rate?
  - Pontos acumulativos?
  - Rating +/- cada vitória/derrota?
- **Recomendação:** Documentar algoritmo e frequência de atualização

### 🔧 Propostas de Melhoria

#### 1. Adicionar "Camadas" de Configuração
```yaml
Grupo (nível administrativo)
├── Configurações Globais
│   ├── Formula de ranking (ELO, Points, Win Rate)
│   ├── Frequência de atualização
│   └── Regras de promoção/rebaixamento
└── Evento (nível operacional)
    ├── Tipo de torneio
    ├── Datas
    └── Jogadores elegíveis
```

#### 2. Suportar "SubGrupos" para Ligasyy
```
Grupo: "Ping Pong Brasil"
├── SubGrupo: "Região Sudeste"
│   ├── Evento: Copa Sudeste 2025
│   └── Ranking Regional
├── SubGrupo: "Região Nordeste"
│   └── ...
└── Ranking Nacional (agregado de todos)
```

#### 3. Versionamento de Rankings
Manter histórico de como o ranking mudou
```python
class RankingHistory:
    jogador_id: int
    grupo_id: int
    evento_id: int  # opcional
    posicao: int
    rating: float
    data_calculo: datetime
    motivo: str  # "vitória_partida", "derrota", "recalculo_periodico"
```

---

### 💾 Avaliação Técnica - Modelo de Dados

#### Schemas Propostos

```python
# GRUPOS
class Grupo(Base):
    __tablename__ = "grupos"
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(255), unique=True, nullable=False)
    descricao = Column(Text)
    criador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    ativo = Column(Boolean, default=True)
    
    # Configurações
    formula_ranking = Column(String(50), default="elo")  # elo, points, winrate
    k_factor = Column(Float, default=32)  # para ELO
    atualiza_automático = Column(Boolean, default=True)
    
    # Relacionamentos
    eventos = relationship("Evento", back_populates="grupo", cascade="all, delete-orphan")
    membros = relationship("Jogador", secondary="grupo_membership", back_populates="grupos")

# MEMBERSHIPS (Relacionamento N:N)
class GrupoMembership(Base):
    __tablename__ = "grupo_membership"
    
    id = Column(Integer, primary_key=True)
    jogador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=False)
    
    # Rastreamento temporal
    data_entrada = Column(DateTime, default=datetime.utcnow)
    data_saida = Column(DateTime, nullable=True)  # NULL = membro ativo
    
    # Status
    role = Column(String(50), default="jogador")  # jogador, moderador, admin
    status = Column(String(50), default="ativo")  # ativo, suspenso, removido
    
    # Metadados
    convidado_por_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    data_ultima_atividade = Column(DateTime)
    
    # Índices
    __table_args__ = (
        UniqueConstraint('jogador_id', 'grupo_id', name='unique_jogador_grupo'),
    )

# EVENTOS (modificado para referenciar Grupo)
class Evento(Base):
    __tablename__ = "eventos"
    
    id = Column(Integer, primary_key=True)
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=False)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date)
    
    # Tipo de torneio
    tipo_torneio = Column(
        String(50),
        default="simples"
    )  # simples, eliminatório, fase_grupos_eliminatório, suico
    
    # Estado
    ativo = Column(Boolean, default=True)
    status = Column(String(50), default="planejamento")  # planejamento, em_andamento, finalizado
    
    # Configurações específicas do tipo
    configuracao = Column(JSON)  # para armazenar configs específicas do torneio
    
    # Relacionamentos
    grupo = relationship("Grupo", back_populates="eventos")
    partidas = relationship("Partida", back_populates="evento", cascade="all, delete-orphan")
    jogadores = relationship("Jogador", secondary="evento_players", back_populates="eventos")
    rankings = relationship("RankingEvento", back_populates="evento", cascade="all, delete-orphan")

# RANKING (isolado por EVENTO + GRUPO)
class RankingEvento(Base):
    __tablename__ = "ranking_evento"
    
    id = Column(Integer, primary_key=True)
    evento_id = Column(Integer, ForeignKey("eventos.id"), nullable=False)
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=False)  # desnormalizado para queries rápidas
    jogador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    # Dados do ranking
    posicao = Column(Integer)
    rating = Column(Float, default=1600)
    vitorias = Column(Integer, default=0)
    derrotas = Column(Integer, default=0)
    empates = Column(Integer, default=0)
    
    # Metadados
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint('evento_id', 'jogador_id', name='unique_evento_jogador'),
        Index('idx_grupo_id_evento_id', 'grupo_id', 'evento_id'),
    )

# RANKING AGREGADO (por GRUPO, não por evento)
class RankingGrupo(Base):
    __tablename__ = "ranking_grupo"
    
    id = Column(Integer, primary_key=True)
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=False)
    jogador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    # Dados agregados
    posicao = Column(Integer)
    rating_medio = Column(Float)  # média ponderada de todos eventos
    vitorias_total = Column(Integer, default=0)
    derrotas_total = Column(Integer, default=0)
    
    # Filtros
    minimo_eventos = Column(Integer, default=1)  # qualificar apenas se jogou X eventos
    
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint('grupo_id', 'jogador_id', name='unique_grupo_jogador'),
    )
```

#### ⚠️ Problemas Técnicos Potenciais

1. **Consultas N+1 em Rankings**
   - Problema: `evento.ranking_players` × múltiplos eventos = queries em cascata
   - Solução: Usar `joinedload` e cache Redis para rankings

2. **Desnormalização de `grupo_id` em RankingEvento**
   - Necessário para queries rápidas: "top 10 rankings do Grupo X"
   - Mas cria redundância
   - Solução: Aceitar redundância, manter triggers de sincronização

3. **Atualização de Rankings em Tempo Real**
   - Problema: Recalcular ranking de 10.000 jogadores a cada partida = custoso
   - Solução: Usar job assíncrono (Celery/RQ) para atualizar em background

---

## 🚨 FEATURE 2: Nova Estrutura de Usuários

### 🎯 Visão Geral

Implementar sistema RBAC (Role-Based Access Control) com 3 roles:
- **Administrador**: Superuser
- **Organizador**: Gerencia eventos, mas também é jogador
- **Jogador**: Participa de eventos

### ✅ Pontos Positivos

1. **Hierarquia clara**: Admin > Organizador > Jogador
2. **Organizador é jogador**: Evita tabelas separadas
3. **Registro obrigatório**: Auditoria completa

### ⚠️ Problemas Identificados

#### 1. **Falta de Clareza sobre "Administrador"**
- Problema: "Administrado" parece typo para "Administrador"
- Problema: Qual é o escopo do Admin?
  - Admin global (superuser)?
  - Admin de grupo?
  - Admin de evento?
- **Recomendação:** Usar terminologia precisa: "ROLE HIERARCHY"

```
┌─────────────────────────────────────────────┐
│ SUPERADMIN                                  │
│ └─ Gerencia plataforma inteira              │
│    ├─ ADMIN GRUPO                           │
│    │  └─ Gerencia 1 grupo específico        │
│    │     ├─ Organizador de Evento           │
│    │     │  └─ Cria/edita eventos          │
│    │     └─ Jogador                         │
│    │        └─ Participa de eventos        │
│    └─ Moderador                             │
│       └─ Gerencia disputas/violações        │
└─────────────────────────────────────────────┘
```

#### 2. **Ausência de Permissões Granulares**
- Problema: Como um organizador cria evento em um grupo?
  - Precisa estar no grupo?
  - Precisa ser convidado?
  - Automaticamente pode se adicionar?
- Problema: Um jogador pode se remover de um evento após começar?
  - Deve ser penalizado?
  - Afeta ranking?
- **Recomendação:** Adicionar matriz de permissões

| Ação | Jogador | Organizador | Admin Grupo | SuperAdmin |
|------|---------|-------------|-------------|------------|
| Criar Grupo | ❌ | ❌ | ❌ | ✅ |
| Criar Evento no Grupo | ❌ | ✅ | ✅ | ✅ |
| Adicionar Jogador ao Evento | ❌ | ✅ (seu grupo) | ✅ | ✅ |
| Se auto-adicionar a Evento | ✅ | ✅ | ✅ | ✅ |
| Remover Jogador do Evento | ❌ | ✅ (seu grupo) | ✅ | ✅ |
| Registrar Partida | ❌ | ✅ (seu grupo) | ✅ | ✅ |
| Editar Ranking | ❌ | ❌ | ✅ | ✅ |
| Deletar Evento | ❌ | ❌ | ✅ | ✅ |

#### 3. **Falta de Ciclo de Vida de Membership**
- Problema: Similar a Feature 1, falta clareza sobre entrada/saída
- Estado de membro:
  - Convite pendente?
  - Ativo?
  - Bloqueado?
  - Suspenso (violação de regras)?
- **Recomendação:** Adicionar status_membership

#### 4. **Autenticação Não Mencionada**
- Problema: Como usuários se autenticam?
  - JWT? (recomendado)
  - Sessions?
  - OAuth? (Google, GitHub)
- **Recomendação:** Implementar JWT + refresh tokens

#### 5. **Organização de Usuários e Perfil**
- Problema: O que é um "perfil" de usuário?
  - Avatar, bio, histórico?
  - Stats globais ou por grupo?
  - Preferências (notificações, privacidade)?
- **Recomendação:** Adicionar tabela Usuario_Profile

### 🔧 Propostas de Melhoria

#### 1. Adicionar Moderador e Árbitro
```python
class RoleEnum(str, Enum):
    SUPERADMIN = "superadmin"      # Admin global
    ADMIN_GRUPO = "admin_grupo"    # Admin de grupo específico
    ORGANIZADOR = "organizador"    # Cria eventos
    MODERADOR = "moderador"        # Resolve disputas
    ARBITRO = "arbitro"            # Registra partidas em eventos
    JOGADOR = "jogador"            # Participa
```

#### 2. Implementar Permissões Dinâmicas
```python
# Em vez de hardcoded, usar tabela de permissões
class Permissao(Base):
    __tablename__ = "permissoes"
    
    id = Column(Integer, primary_key=True)
    role = Column(String(50))
    recurso = Column(String(50))  # evento, grupo, jogador
    acao = Column(String(50))     # criar, editar, deletar, ver
    escopo = Column(String(50))   # global, grupo, evento, proprio
    
# Usar no authorization
@requires_permission("evento", "criar", escopo="grupo")
def criar_evento(grupo_id, ...):
    pass
```

#### 3. Adicionar Histórico de Alterações (Audit Log)
```python
class AuditLog(Base):
    __tablename__ = "audit_log"
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    acao = Column(String(255))  # "criar_evento", "adicionar_jogador"
    recurso_tipo = Column(String(50))  # "evento", "jogador"
    recurso_id = Column(Integer)
    dados_antes = Column(JSON)
    dados_depois = Column(JSON)
    data_hora = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(45))  # IPv4 ou IPv6
```

### 💾 Avaliação Técnica - Modelo de Dados

```python
# USUARIOS (modificado)
class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    nome = Column(String(255), nullable=False)
    
    # Role global (defaut)
    role_global = Column(String(50), default="jogador")
    
    # Perfil
    avatar_url = Column(String(500))
    bio = Column(Text)
    
    # Status
    ativo = Column(Boolean, default=True)
    email_verificado = Column(Boolean, default=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    grupos = relationship("Grupo", secondary="grupo_membership", back_populates="membros")
    eventos = relationship("Evento", secondary="evento_players", back_populates="jogadores")
    
    # Relacionamento com roles específicas por grupo
    roles_grupo = relationship("UsuarioGrupoRole", back_populates="usuario", cascade="all, delete-orphan")

# USUARIO GRUPO ROLE (mapear roles por grupo)
class UsuarioGrupoRole(Base):
    __tablename__ = "usuario_grupo_role"
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=False)
    role = Column(String(50))  # admin_grupo, organizador, jogador
    
    __table_args__ = (
        UniqueConstraint('usuario_id', 'grupo_id', name='unique_usuario_grupo_role'),
    )
    
    usuario = relationship("Usuario", back_populates="roles_grupo")
```

---

## 🎨 FEATURE 3: Nova Página Inicial

### 🎯 Visão Geral

Redesenhar homepage para refletir nova hierarquia (Grupo → Evento) e novo sistema de usuários.

### 📊 Sugestões para Homepage

#### Layout Proposto (Dashboard por Tipo de Usuário)

```
┌─────────────────────────────────────────────────────────────┐
│                    PING CHAMPIONS                           │
│  [Home] [Grupos] [Eventos] [Ranking] [Perfil] [Sair]       │
└─────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════

🎮 MEUS GRUPOS (3)
┌──────────────────┬──────────────────┬──────────────────┐
│ Grupo 1: Sudeste │ Grupo 2: Online  │ Grupo 3: Casual │
├──────────────────┼──────────────────┼──────────────────┤
│ 45 jogadores     │ 128 jogadores    │ 12 jogadores    │
│ 8 eventos        │ 12 eventos       │ 2 eventos       │
│ Ranking: #12     │ Ranking: #34     │ Ranking: #2     │
│ [Entrar]         │ [Entrar]         │ [Entrar]        │
└──────────────────┴──────────────────┴──────────────────┘

═══════════════════════════════════════════════════════════════

🏆 PRÓXIMOS EVENTOS (seus grupos)
┌─────────────────────────────────────────────────────────┐
│ 📅 Copa Sudeste 2025 (Grupo 1)                         │
│ 🗓️  Início: 20 nov | Status: Em inscrições             │
│ 👥 28/50 jogadores inscritos | [Ver evento] [Inscrever]│
├─────────────────────────────────────────────────────────┤
│ 📅 Torneio Online #5 (Grupo 2)                         │
│ 🗓️  Início: 15 nov | Status: Em andamento              │
│ 🎯 Fase de grupos | [Ver evento]                       │
└─────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════

📊 MEUS RANKINGS ATUAIS
┌──────────────┬──────────┬──────────┬──────────┐
│ Grupo        │ Posição  │ Rating   │ Vitórias │
├──────────────┼──────────┼──────────┼──────────┤
│ Sudeste      │ #12      │ 1650     │ 42       │
│ Online       │ #34      │ 1520     │ 28       │
│ Casual       │ #2       │ 1780     │ 15       │
└──────────────┴──────────┴──────────┴──────────┘

═══════════════════════════════════════════════════════════════

🔍 AÇÕES RÁPIDAS (se Organizador)
┌────────────────┬────────────────┬────────────────┐
│ [Criar Evento] │ [Gerenciar]    │ [Relatórios]   │
└────────────────┴────────────────┴────────────────┘
```

#### ⚠️ Considerações de UX/UI

1. **Segregação por Grupo**
   - ✅ Mostrar apenas eventos do grupo em que está
   - ✅ Filtro/busca para múltiplos grupos
   - ❌ Não misturar rankings de grupos diferentes

2. **Informações Contextuais**
   - ✅ Status do evento (planejamento, em andamento, finalizado)
   - ✅ Sua posição no evento
   - ✅ Próximas rodadas/datas
   - ❌ Não sobrecarregar com muita informação

3. **Call to Action (CTA)**
   - ✅ "Inscrever em evento" em destaque
   - ✅ "Ver meu ranking"
   - ✅ "Procurar novos grupos"
   - ✅ "Criar grupo" (se permitido)

4. **Mobile First**
   - ✅ Layout responsivo (cartões empilhados em mobile)
   - ✅ Touch-friendly buttons
   - ✅ Carregamento progressivo

---

### 🎨 Componentes Vue 3 Sugeridos

```vue
<!-- Novo: GroupSelector.vue -->
<template>
  <div class="group-selector">
    <div v-for="grupo in meus_grupos" :key="grupo.id" 
         class="group-card"
         :class="{ active: grupo.id === grupo_selecionado }"
         @click="selecionar_grupo(grupo.id)">
      <h3>{{ grupo.nome }}</h3>
      <p class="stats">{{ grupo.total_jogadores }} jogadores • {{ grupo.total_eventos }} eventos</p>
      <p class="ranking">Ranking: #{{ meu_ranking_grupo[grupo.id].posicao }}</p>
    </div>
  </div>
</template>

<!-- Novo: EventosProximos.vue -->
<template>
  <div class="eventos-proximos">
    <h2>Próximos Eventos</h2>
    <div v-for="evento in proximos_eventos" :key="evento.id"
         class="evento-card">
      <div class="evento-header">
        <h3>{{ evento.nome }}</h3>
        <span class="status" :class="evento.status">{{ evento.status }}</span>
      </div>
      <p>📅 {{ formato_data(evento.data_inicio) }}</p>
      <p>👥 {{ evento.jogadores_inscritos }}/{{ evento.vagas }}</p>
      <div class="evento-actions">
        <button v-if="!estou_inscrito(evento.id)" @click="inscrever(evento.id)">
          Inscrever
        </button>
        <button v-else @click="ver_evento(evento.id)" class="secondary">
          Ver Evento
        </button>
      </div>
    </div>
  </div>
</template>

<!-- Novo: RankingResumido.vue -->
<template>
  <div class="ranking-resumido">
    <h2>Meus Rankings</h2>
    <table>
      <thead>
        <tr>
          <th>Grupo</th>
          <th>Posição</th>
          <th>Rating</th>
          <th>W-L-D</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="rank in meus_rankings" :key="rank.grupo_id">
          <td>{{ rank.grupo_nome }}</td>
          <td class="posicao">{{ rank.posicao }}</td>
          <td>{{ rank.rating.toFixed(0) }}</td>
          <td>{{ rank.vitorias }}-{{ rank.derrotas }}-{{ rank.empates }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
```

---

### 💾 Endpoints API Necessários para Homepage

```python
# GET /api/v1/me - Usuário logado
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@example.com",
  "role": "jogador",
  "avatar_url": "...",
  "data_criacao": "2024-01-15"
}

# GET /api/v1/grupos/meus-grupos
[
  {
    "id": 1,
    "nome": "Sudeste",
    "total_jogadores": 45,
    "total_eventos": 8,
    "role_no_grupo": "jogador",  # ou organizador
    "meu_ranking": {"posicao": 12, "rating": 1650}
  },
  ...
]

# GET /api/v1/eventos/proximos?grupo_id=1
[
  {
    "id": 101,
    "nome": "Copa Sudeste 2025",
    "grupo_id": 1,
    "data_inicio": "2025-11-20",
    "status": "inscricoes",
    "total_inscritos": 28,
    "vagas": 50,
    "tipo_torneio": "fase_grupos_eliminatório",
    "estou_inscrito": true,
    "minha_posicao": 12
  },
  ...
]

# GET /api/v1/ranking/meus-rankings
[
  {
    "grupo_id": 1,
    "grupo_nome": "Sudeste",
    "posicao": 12,
    "rating": 1650,
    "vitorias": 42,
    "derrotas": 18,
    "empates": 2
  },
  ...
]
```

---

## 🎯 Resumo Executivo

### Status das Features

| Feature | Status | Prioridade | Complexidade | Risco |
|---------|--------|-----------|--------------|-------|
| **1: Grupos/Eventos** | ⚠️ Incompleto | 🔴 Alta | 🔴 Alta | 🟠 Médio |
| **2: Usuários/RBAC** | ⚠️ Vago | 🔴 Alta | 🟡 Médio | 🔴 Alto |
| **3: Homepage** | 📋 Proposta | 🟡 Média | 🟢 Baixa | 🟢 Baixo |

### Recomendações Prioritárias

#### 🔴 CRÍTICO (semana 1)
1. Definir ciclo de vida completo de membership (entrada/saída/status)
2. Especificar fórmula de cálculo de ranking e frequência de atualização
3. Implementar RBAC com matriz de permissões explícita

#### 🟠 IMPORTANTE (semana 2)
1. Adicionar tabelas de auditoria (AuditLog)
2. Implementar autenticação JWT com refresh tokens
3. Criar documentação OpenAPI para novos endpoints

#### 🟡 NICE-TO-HAVE (semana 3+)
1. SubGrupos para suportar ligas regionais
2. Versionamento de rankings com histórico completo
3. Dashboard de administrador para monitoramento global

---

## 📚 Apêndices

### A. Diferenças com Sistema Anterior

| Aspecto | Anterior | Novo |
|---------|----------|------|
| Hierarquia | Apenas Evento | Grupo → Evento |
| Jogador em múltiplos eventos | Sim | Sim, mas isolados por grupo |
| Rankings | Global | Por grupo |
| Usuários | Sem roles explícitas | RBAC com 3+ roles |
| Memberships | Implícita | Explícita com histórico |

### B. Casos de Teste Críticos

**Feature 1: Ranking Isolado**
```
DADO: Jogador A está em Grupo 1 e Grupo 2
QUANDO: Jogador A vence partida no Grupo 1
THEN: Rating do Grupo 1 aumenta
AND:  Rating do Grupo 2 não é afetado
```

**Feature 2: Permissões**
```
DADO: Usuário B é organizador do Grupo 2
WHEN: Usuário B tenta criar evento no Grupo 1
THEN: Erro 403 Forbidden (sem permissão)
```

**Feature 3: Homepage**
```
DADO: Usuário C tem 3 grupos
WHEN: Seleciona Grupo 1
THEN: Mostra apenas eventos do Grupo 1
AND:  Rankings mostram posição no Grupo 1
```

---

**Documento preparado para revisão e refinamento**
