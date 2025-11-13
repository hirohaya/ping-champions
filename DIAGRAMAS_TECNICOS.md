# Diagramas Técnicos - Refatoração Ping Champions

---

## 1. Diagrama Entidade-Relacionamento (DER)

```
┌─────────────────────────────────────────────────────────────────┐
│                       MODELO DE DADOS                           │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│    USUARIO       │
├──────────────────┤
│ id (PK)          │──┐
│ email            │  │
│ nome             │  │
│ senha_hash       │  │
│ role_global      │  │
│ avatar_url       │  │
│ bio              │  │
│ ativo            │  │
│ data_criacao     │  │
└──────────────────┘  │
         │            │
         │            │
    ┌────┴────────────┴──────┐
    │                         │
┌───▼──────────────────┐   ┌─▼──────────────────┐
│  GRUPO_MEMBERSHIP    │   │ USUARIO_GRUPO_ROLE│
├──────────────────────┤   ├──────────────────┤
│ id (PK)              │   │ id (PK)           │
│ jogador_id (FK)      │   │ usuario_id (FK)   │
│ grupo_id (FK)        │   │ grupo_id (FK)     │
│ data_entrada         │   │ role              │
│ data_saida (NULL)    │   └───────────────────┘
│ role                 │
│ status               │
└──────┬───────────────┘
       │
       │
   ┌───▼──────────────────────┐
   │      GRUPO               │
   ├──────────────────────────┤
   │ id (PK)                  │
   │ nome                     │
   │ descricao                │
   │ criador_id (FK) → USUARIO│
   │ data_criacao             │
   │ ativo                    │
   │ formula_ranking (elo)    │
   │ k_factor (32)            │
   │ atualiza_automatico      │
   └──────┬────────────────────┘
          │
          │
      ┌───▼──────────────────────┐
      │      EVENTO              │
      ├──────────────────────────┤
      │ id (PK)                  │
      │ grupo_id (FK)            │
      │ nome                     │
      │ data_inicio              │
      │ data_fim                 │
      │ tipo_torneio             │
      │ status                   │
      │ configuracao (JSON)      │
      └──────┬────────────────────┘
             │
             │ 1:N
      ┌──────▼────────────────────┐
      │     PARTIDA              │
      ├──────────────────────────┤
      │ id (PK)                  │
      │ evento_id (FK)           │
      │ jogador_1_id (FK)        │
      │ jogador_2_id (FK)        │
      │ vencedor_id (FK)         │
      │ data_partida             │
      │ resultado (1/0/-1)       │
      └──────────────────────────┘

   ┌──────────────────────────────┐
   │  RANKING_EVENTO              │
   ├──────────────────────────────┤
   │ id (PK)                      │
   │ evento_id (FK)               │
   │ grupo_id (FK) [desnorm]      │
   │ jogador_id (FK)              │
   │ posicao                      │
   │ rating                       │
   │ vitorias / derrotas / empates│
   │ data_atualizacao             │
   │ UNIQUE(evento_id, jogador_id)│
   └──────────────────────────────┘

   ┌──────────────────────────────┐
   │  RANKING_GRUPO               │
   ├──────────────────────────────┤
   │ id (PK)                      │
   │ grupo_id (FK)                │
   │ jogador_id (FK)              │
   │ posicao                      │
   │ rating_medio                 │
   │ vitorias_total               │
   │ derrotas_total               │
   │ data_atualizacao             │
   │ UNIQUE(grupo_id, jogador_id) │
   └──────────────────────────────┘

   ┌──────────────────────────────┐
   │  AUDIT_LOG                   │
   ├──────────────────────────────┤
   │ id (PK)                      │
   │ usuario_id (FK)              │
   │ acao (criar_evento)          │
   │ recurso_tipo (evento)        │
   │ recurso_id                   │
   │ dados_antes (JSON)           │
   │ dados_depois (JSON)          │
   │ data_hora                    │
   │ ip_address                   │
   └──────────────────────────────┘
```

---

## 2. Fluxo de Memberships (Timeline)

```
USUARIO ENTRA EM GRUPO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    Convite           Aceita          Ativo           Saída
    ┌────────────────────┐            ┌──────────────────┐
    │ status: convite    │           │ status: ativo    │
    │ data_entrada: null │    ──→    │ data_entrada: X  │    ──→    status: inativo
    │ data_saida: null   │           │ data_saida: null │           data_saida: Y
    └────────────────────┘            └──────────────────┘


QUERIES IMPORTANTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Membros ATIVOS de um grupo AGORA
   SELECT * FROM grupo_membership 
   WHERE grupo_id = ? 
     AND status = 'ativo'
     AND data_entrada <= CURDATE()
     AND (data_saida IS NULL OR data_saida > CURDATE())

2. Membros que ERAM do grupo em DATA X
   SELECT * FROM grupo_membership 
   WHERE grupo_id = ?
     AND data_entrada <= DATE(?)
     AND (data_saida IS NULL OR data_saida >= DATE(?))

3. Jogadores elegíveis para EVENTO (baseado em timeline)
   SELECT DISTINCT u.* 
   FROM usuarios u
   JOIN grupo_membership gm ON u.id = gm.jogador_id
   JOIN evento e ON e.grupo_id = gm.grupo_id
   WHERE e.id = ?
     AND gm.data_entrada <= e.data_inicio
     AND (gm.data_saida IS NULL OR gm.data_saida >= e.data_inicio)
```

---

## 3. Hierarquia de Permissões

```
┌─────────────────────────────────────────────────────────┐
│                    ROLE HIERARCHY                       │
└─────────────────────────────────────────────────────────┘

                        SUPERADMIN
                          │ │ │
                          │ │ └──── Manage Users (globally)
                          │ └────── Manage Groups
                          └──────── Manage Disputes

                            │
                            ▼
                    ADMIN_GRUPO (por grupo)
                          │ │ │
                          │ │ └──── Edit Rankings
                          │ └────── Suspend Members
                          └──────── View Group Stats

                            │
                            ▼
                      ORGANIZADOR (por grupo)
                          │ │ │
                          │ │ └──── Register Matches
                          │ └────── Create Events
                          └──────── Manage Event Players

                            │
                            ▼
                        JOGADOR
                          │ │ │
                          │ │ └──── View Ranking
                          │ └────── Self-Register Event
                          └──────── Play Matches


MATRIZ DE PERMISSÕES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ação                      │ Jogador │ Organizador │ Admin Grupo │ SuperAdmin
─────────────────────────┼─────────┼─────────────┼─────────────┼───────────
Criar Grupo              │    ❌   │      ❌      │      ❌      │     ✅
Editar Grupo             │    ❌   │      ❌      │      ✅      │     ✅
Criar Evento (seu grupo) │    ❌   │      ✅      │      ✅      │     ✅
Editar Evento (seu)      │    ❌   │      ✅      │      ✅      │     ✅
Deletar Evento           │    ❌   │      ❌      │      ✅      │     ✅
Registrar Partida        │    ❌   │      ✅      │      ✅      │     ✅
Editar Ranking           │    ❌   │      ❌      │      ✅      │     ✅
Ver Rankings             │    ✅   │      ✅      │      ✅      │     ✅
Se Inscrever Evento      │    ✅   │      ✅      │      ✅      │     ✅
Sair do Evento           │    ✅   │      ✅      │      ✅      │     ✅
Remover Jogador Event    │    ❌   │      ✅      │      ✅      │     ✅
Suspender Membro Grupo   │    ❌   │      ❌      │      ✅      │     ✅
Editar Membros Grupo     │    ❌   │      ❌      │      ✅      │     ✅
```

---

## 4. Fluxo de Cálculo de Ranking

```
EVENTO INICIADO
│
├─► PARTIDA 1 REGISTRADA
│   ├─► Jogador A vence Jogador B
│   ├─► Calcula novo rating (ELO)
│   │   Rating_novo = Rating_antigo + K × (1 - Esperado)
│   ├─► Atualiza RANKING_EVENTO (para este evento)
│   └─► Atualiza RANKING_GRUPO (agregado de todos)
│
├─► PARTIDA 2 REGISTRADA
│   └─► Mesmo fluxo...
│
└─► EVENTO FINALIZADO
    │
    ├─► Trigger: RECALCULAR_RANKING_GRUPO
    │   └─► Para todos jogadores que participaram
    │       ├─► Calcula média de ratings de TODOS eventos
    │       ├─► Calcula total de vitórias/derrotas
    │       └─► Ordena por rating (posição)
    │
    └─► LOG: Ranking atualizado em [data/hora]


ESTRATÉGIA DE ATUALIZAÇÃO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Opção 1: REAL-TIME (após cada partida)
  Vantagem: Rankings sempre atualizados
  Desvantagem: CPU/DB stress com muitas partidas
  Usar se: < 5000 partidas/dia

Opção 2: BATCH (diariamente à noite)
  Vantagem: Operações em lote, mais eficiente
  Desvantagem: Rankings atrasados
  Usar se: Quer consistência sem impacto real-time

Opção 3: HYBRID (real-time evento, batch grupo)
  Vantagem: Equilíbrio entre performance e atualização
  Desvantagem: Mais complexo de implementar
  Usar se: Quer o melhor dos dois mundos

Recomendação: HYBRID com Redis cache
```

---

## 5. Fluxo de Autenticação (JWT)

```
CLIENT                          SERVER
   │                              │
   ├──────── POST /login ────────►│
   │         {email, senha}        │
   │                              │
   │◄─── 200 OK ────────────────┤
   │  {                           │
   │    access_token: "eyJ...",   │  Válido por 15 min
   │    refresh_token: "eyJ...",  │  Válido por 7 dias
   │    usuario: {...}            │
   │  }                           │
   │                              │
   ├─ Armazena em localStorage    │
   │                              │
   │                              │
   ├──── GET /api/eventos ───────►│
   │  Headers:                    │
   │  Authorization:              │
   │  Bearer eyJ...               │
   │                              │
   │  Servidor verifica token     │
   │  Decodifica e valida         │
   │                              │
   │◄──── 200 OK [dados] ────────┤
   │                              │
   │                              │
   │ [15 min depois, token expira]│
   │                              │
   │                              │
   ├──── GET /api/eventos ───────►│
   │                              │
   │ Token expirado!              │
   │                              │
   │◄──── 401 UNAUTHORIZED ──────┤
   │                              │
   │                              │
   ├─ POST /refresh ────────────►│
   │  {refresh_token: "eyJ..."}   │
   │                              │
   │◄─── 200 OK ────────────────┤
   │  {access_token: "novo..."}   │
   │                              │
   ├──── GET /api/eventos ───────►│
   │  Authorization: Bearer novo..│
   │                              │
   │◄──── 200 OK [dados] ────────┤


TOKEN STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Header: {alg: "HS256", typ: "JWT"}

Payload:
{
  "sub": "1",                    # usuario id
  "email": "user@example.com",
  "nome": "João Silva",
  "role": "jogador",
  "grupos": [1, 2, 5],          # grupos que participa
  "iat": 1605000000,            # issued at
  "exp": 1605000900             # expiration (15 min = 900 seg)
}

Signature: HMACSHA256(header.payload, SECRET)

Refresh Token (7 dias):
{
  "sub": "1",
  "type": "refresh",
  "iat": 1605000000,
  "exp": 1605604800             # 7 dias depois
}
```

---

## 6. Estados de Evento (State Machine)

```
┌─────────────┐
│ PLANEJAMENTO│  ◄─── Criado
└──────┬──────┘
       │ Definir datas/players
       ▼
┌─────────────────────┐
│ INSCRICOES_ABERTAS  │
└──────┬──────────────┘
       │ Data começa
       │ Jogadores inscritos
       ▼
┌───────────────┐
│  EM_ANDAMENTO │
└──────┬────────┘
       │ Registrar partidas
       │ Próximas rodadas
       ▼
┌──────────────┐
│  FINALIZADO  │  ◄─── Rankings finais calculados
└──────────────┘


TRANSIÇÕES E REGRAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PLANEJAMENTO → INSCRICOES_ABERTAS
  Condições: data_inicio > hoje
  Ações: Notificar grupo

INSCRICOES_ABERTAS → EM_ANDAMENTO
  Condições: hoje >= data_inicio
  Ações: Gerar chaves/grupos automáticos (se tipo != simples)
  Ações: Notificar jogadores inscritos

EM_ANDAMENTO → FINALIZADO
  Condições: hoje >= data_fim OU todas partidas jogadas
  Ações: Calcular ranking final
  Ações: Atualizar rating dos jogadores
  Ações: Notificar vencedores

PERMITIDO DELETAR?
  PLANEJAMENTO: ✅ Sim (sem dados)
  INSCRICOES_ABERTAS: ⚠️ Com cuidado (jogadores inscritos)
  EM_ANDAMENTO: ❌ Não (dados de partidas)
  FINALIZADO: ❌ Nunca (dados históricos)
```

---

## 7. Tipos de Torneio - Configurações

```
SIMPLES (1v1)
┌──────────────────────────────────────┐
│ Jogador A ─┐                         │
│            ├─► Partida 1             │
│ Jogador B ─┘                         │
│                                      │
│ Configuração:                        │
│ - minimo_jogadores: 2                │
│ - maximo_rodadas: N                  │
│ - pode_repetir_oponente: true        │
└──────────────────────────────────────┘


ELIMINATORIO (8/16/32 jogadores)
┌──────────────────────────────────────┐
│ Oitavas:   Quartas:   Semis:  Final: │
│ A ──┐                           │    │
│ B ──┤──┐                    │    │    │
│      ├──X ──┐              │    │    │
│ C ──┐│      │──┐       │    │    │    │
│ D ──┤┘      │  X ──┐   │    │    │    │
│      ├──────┘      │───X    │    │    │
│ E ──┐│              │        ├───X    │
│ F ──┤├──Y ──┐       │        │        │
│      ┘      │───Y ──X        │        │
│ G ──┐       │               │        │
│ H ──┤───────┘               │        │
│      └──────────────────────┘        │
│                                      │
│ Configuração:                        │
│ - tamanho_chave: 8/16/32/64          │
│ - terceiro_lugar: true/false         │
│ - roteio: "sorteado" ou "seed_based" │
└──────────────────────────────────────┘


FASE DE GRUPOS + ELIMINATORIO
┌──────────────────────────────────────┐
│ GRUPOS (Round Robin)                 │
│                                      │
│ Grupo A:           Grupo B:          │
│ J1 vs J2 vs J3    J5 vs J6 vs J7    │
│                                      │
│ Top 2 de cada:     [J1, J2, J5, J6]  │
│                                      │
│ ┌─ ELIMINTÓRIO (Semifinal) ────┐    │
│ │                               │    │
│ │  J1 ──┐       ┌─ FINAL ─┐    │    │
│ │       ├─────►J?          │    │    │
│ │  J5 ──┘            ├──► Campeão   │
│ │                    │               │
│ │  J2 ──┐       ┌─┘ │               │
│ │       ├─────►J?     │               │
│ │  J6 ──┘            │               │
│ └───────────────────────┘            │
│                                      │
│ Configuração:                        │
│ - tamanho_grupo: 3/4/5               │
│ - qualificam_per_grupo: 2            │
│ - rodadas_grupo: rodadas/datas       │
└──────────────────────────────────────┘


RODADA SUICA (Pareamento Dinâmico)
┌──────────────────────────────────────┐
│ Rodada 1:                            │
│ J1(0p) vs J2(0p)  → J1 vence        │
│ J3(0p) vs J4(0p)  → J3 vence        │
│ J5(0p) vs J6(0p)  → J5 vence        │
│                                      │
│ Placar: J1(1p), J3(1p), J5(1p), ...│
│                                      │
│ Rodada 2: Parear por SCORE          │
│ J1(1p) vs J3(1p)  → J1 vence        │
│ J5(1p) vs J2(0p)  → J5 vence        │
│ ...                                  │
│                                      │
│ Configuração:                        │
│ - total_rodadas: 5                   │
│ - algoritmo: "dutch_system"          │
│ - emparelhador: "Swiss pairing"      │
│ - calculo_ranking: "buchholz"        │
└──────────────────────────────────────┘
```

---

## 8. Fluxo de Navegação - Homepage (Novo)

```
LOGIN
│
└─► DASHBOARD PRINCIPAL
    │
    ├─ [Seletor de Grupo] ◄─────────┐
    │  ┌─────────────────────────┐   │
    │  │ Grupo 1 │ Grupo 2 │ ...│   │
    │  └─────────────────────────┘   │
    │           │                    │
    │           ▼                    │
    │  ┌──────────────────────────┐  │
    │  │  PRÓXIMOS EVENTOS (G1)   │  │
    │  │ - Copa Sudeste 2025      │  │
    │  │   [Detalhes] [Inscrever] │  │
    │  └──────────────────────────┘  │
    │           │                    │
    │           ▼                    │
    │  ┌──────────────────────────┐  │
    │  │ MEU RANKING (G1)         │  │
    │  │ #12 - Rating: 1650       │  │
    │  │ W: 42 L: 18 D: 2         │  │
    │  │ [Ver Ranking Completo]   │  │
    │  └──────────────────────────┘  │
    │           │                    │
    │           ▼                    │
    │  ┌──────────────────────────┐  │
    │  │ AÇÕES (se Organizador)   │  │
    │  │ [Criar Evento] [Gerenciar] │
    │  └──────────────────────────┘  │
    │                                │
    └────────────────────────────────┘
      (mudar grupo = refrescar conteúdo)


COMPONENTES VUE NECESSÁRIOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. GroupSelector.vue
   ├─ Listar meus grupos
   ├─ Selecionar ativo
   └─ Link para procurar grupos

2. EventosProximos.vue
   ├─ Filtrar por grupo ativo
   ├─ Mostrar status
   ├─ CTA "Inscrever" ou "Ver"
   └─ Paginação

3. RankingResumido.vue
   ├─ Tabela: Posição | Rating | W-L-D
   ├─ Filtro por grupo
   └─ Link para ranking completo

4. ActualizarOrganizador.vue (conditional)
   ├─ Criar evento
   ├─ Gerenciar membros
   └─ Ver estatísticas

5. Layout.vue (principal)
   ├─ Header com user info
   ├─ Sidebar com navegação
   └─ Footer
```

---

## 9. Checklist de Implementação

```
FASE 1: Database Schema (2 dias)
  ☐ Criar tabelas Grupo, GrupoMembership
  ☐ Criar tabelas Evento (com tipo_torneio)
  ☐ Modificar tabela Ranking
  ☐ Criar tabelas AuditLog, UsuarioGrupoRole
  ☐ Indexes e constraints

FASE 2: Backend API (1 semana)
  ☐ CRUD Grupos
  ☐ CRUD Eventos
  ☐ Endpoints RBAC
  ☐ JWT authentication
  ☐ Endpoints ranking
  ☐ Testes unitários

FASE 3: Frontend (1 semana)
  ☐ GroupSelector.vue
  ☐ EventosProximos.vue
  ☐ RankingResumido.vue
  ☐ Nova HomePage
  ☐ Integração com API
  ☐ Testes E2E

FASE 4: Tipos de Torneio (2 semanas)
  ☐ Algoritmo Eliminatório
  ☐ Algoritmo Fase de Grupos
  ☐ Testes lógica
  ☐ UI para registrar partidas

FASE 5: Polish & Deploy (1 semana)
  ☐ Performance testing
  ☐ Security audit
  ☐ Documentação
  ☐ Deploy staging
  ☐ Deploy production
```

---

Este arquivo serve como referência visual para os arquitetos e desenvolvedores.
