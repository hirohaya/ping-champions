# Exemplo Prático de Implementação - Caso de Uso Completo

**Objetivo:** Demonstrar como as 3 features funcionam integradas em um cenário real

---

## 📖 Caso de Uso: "Copa Sudeste 2025"

### 🎯 Contexto

- **Grupo:** "Ping Pong Brasil - Sudeste"
- **Organizador:** João Silva (admin_grupo)
- **Tipo:** Fase de Grupos + Eliminatório
- **Participantes:** 12 jogadores inscritos
- **Data:** 20-28 de novembro de 2025

---

## ⏱️ Timeline de Eventos

### Semana 1: Preparação

#### 🗓️ 15 de novembro (T-5 dias)

**João (Organizador) cria evento:**

```python
# Backend: POST /api/v1/grupos/1/eventos
{
    "nome": "Copa Sudeste 2025",
    "data_inicio": "2025-11-20",
    "data_fim": "2025-11-28",
    "tipo_torneio": "fase_grupos_eliminatório",
    "configuracao": {
        "fase_grupos": {
            "tamanho_grupo": 4,        # 4 jogadores por grupo
            "qualificam": 2,           # top 2 avançam
            "rodadas": 3               # 3 rodadas na fase
        },
        "eliminatorio": {
            "tipo": "semifinal_final"  # semifinal + final
        }
    }
}

# Response:
HTTP 201 Created
{
    "id": 101,
    "nome": "Copa Sudeste 2025",
    "grupo_id": 1,
    "status": "planejamento",
    "criado_em": "2025-11-15T10:00:00Z",
    "evento_url": "/api/v1/eventos/101"
}
```

**Sistema cria automaticamente:**
```
✅ Ranking inicial para evento (vazio)
✅ Notificação para membros do grupo: "Novo evento criado!"
✅ Audit log: "João criou evento Copa Sudeste"
```

---

#### 🗓️ 16-19 de novembro (Inscrições)

**Jogadores se inscrevem:**

```python
# Frontend: Usuário clica [Inscrever] no evento

# Backend: POST /api/v1/eventos/101/inscrever
# Autenticado como: jogador_id=5 (Maria)

Response 200 OK:
{
    "mensagem": "Inscrita com sucesso!",
    "evento": {
        "id": 101,
        "inscritos": 12,
        "vagas": 50,
        "estou_inscrito": true,
        "minha_posicao": "TBD (será definida nos grupos)"
    }
}

# Audit log: "Maria se inscreveu em Copa Sudeste"
```

**Homepage da Maria (antes do evento começar):**

```
┌─────────────────────────────────────────────┐
│      PING CHAMPIONS - Meu Dashboard         │
├─────────────────────────────────────────────┤

[Sudeste] [Online] [Casual]     ◄─ Group Selector
         ↑ selecionado

┌─────────────────────────────────────────────┐
│        📅 PRÓXIMOS EVENTOS (Sudeste)        │
├─────────────────────────────────────────────┤
│ Copa Sudeste 2025                           │
│ 📅 20-28 nov | Status: ⏳ Inscrições       │
│ 👥 12/50 inscritos | [Inscrita ✓]           │
│ 🎯 Fase de Grupos + Eliminatório            │
│ [Ver Detalhes]                              │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│     📊 MEU RANKING (Sudeste)                │
├─────────────────────────────────────────────┤
│ Posição: #3                                 │
│ Rating: 1620  |  W: 28  L: 12  D: 1        │
│ [Ver Ranking Completo]                      │
└─────────────────────────────────────────────┘
```

---

### Semana 2: Início

#### 🗓️ 20 de novembro (Evento Inicia)

**Sistema auomaticamente:**

```python
# Trigger: data_hoje >= evento.data_inicio

# 1. Valida inscrições
total_inscritos = 12
eh_valido = total_inscritos >= configuracao.minimo_jogadores (2)
# ✅ Válido

# 2. Cria grupos automaticamente (balanceado por seed)
# Ordena jogadores por rating (maior primeiro)

jogadores_ordenados = [
    (1620, Maria),      # #3 ranking geral
    (1580, João P),     # #5
    (1550, Pedro),      # #8
    (1540, Ana),        # #10
    (1530, Carlos),     # #12
    (1520, Lucas),      # #14
    (1510, Beatriz),    # #16
    (1500, Felipe),     # #18
    (1480, Gisele),     # #22
    (1470, Hermes),     # #24
    (1450, Iris),       # #28
    (1430, Julio)       # #32
]

# Aloca alternando:
grupos = {
    "Grupo A": [Maria(1620), Ana(1540), Lucas(1520), Gisele(1480)],
    "Grupo B": [João P(1580), Carlos(1530), Beatriz(1510), Hermes(1470)],
    "Grupo C": [Pedro(1550), Felipe(1500), Iris(1450), Julio(1430)]
}

# 3. Cria tabela de jogos (round-robin cada grupo)
# Cada jogador joga contra cada um 1 vez (3 rodadas por grupo)

Grupo A - Rodada 1:
├─ Maria vs Ana
├─ Lucas vs Gisele

Grupo A - Rodada 2:
├─ Maria vs Lucas
├─ Ana vs Gisele

Grupo A - Rodada 3:
├─ Maria vs Gisele
└─ Ana vs Lucas

# 4. Notifica jogadores
Email para todos: "Sua chave na Copa Sudeste!"
```

**Homepage da Maria (durante evento - Rodada 1):**

```
┌──────────────────────────────────────────────┐
│        COPA SUDESTE 2025 - Meus Detalhes    │
├──────────────────────────────────────────────┤
│                                              │
│ Status: ⚽ EM ANDAMENTO                      │
│ Fase: Grupos (Rodada 1/3)                   │
│                                              │
│ Meu Grupo: A                                │
│ ┌──────────────────────────────────────┐   │
│ │ Maria        │ W: 0 L: 0 D: 0 (Você) │   │
│ │ Ana          │ W: 0 L: 0 D: 0       │   │
│ │ Lucas        │ W: 0 L: 0 D: 0       │   │
│ │ Gisele       │ W: 0 L: 0 D: 0       │   │
│ └──────────────────────────────────────┘   │
│                                              │
│ Próxima Partida:                           │
│ 🔴 HOJE: Maria vs Ana (seu jogo!)          │
│ [Registrar Resultado]                       │
│                                              │
└──────────────────────────────────────────────┘
```

---

#### 🗓️ 20-25 de novembro (Fase de Grupos)

**Partida 1: Maria vs Ana (20 nov)**

```python
# João (organizador) registra resultado
# POST /api/v1/eventos/101/partidas

{
    "jogador_1_id": 5,      # Maria
    "jogador_2_id": 4,      # Ana
    "vencedor_id": 5,       # Maria venceu
    "data_partida": "2025-11-20",
    "evento_id": 101
}

Response 200 OK:
{
    "partida_id": 501,
    "resultado": "Maria venceu Ana",
    "ranking_evento": {
        "Maria": {"posicao": 1, "rating": 1640, "vitorias": 1, "derrotas": 0},
        "Ana": {"posicao": 4, "rating": 1510, "vitorias": 0, "derrotas": 1}
    }
}

# Sistema calcula automático:
# Maria: 1620 + 32 × (1 - 0.55) = 1620 + 14.4 = 1634.4 ≈ 1634
# Ana:   1540 + 32 × (0 - 0.45) = 1540 - 14.4 = 1525.6 ≈ 1526

# Audit log:
{
    "acao": "registrar_partida",
    "usuario_id": 1,  # João
    "evento_id": 101,
    "partida_id": 501,
    "dados": {
        "jogador_1": "Maria (1620 → 1634)",
        "jogador_2": "Ana (1540 → 1526)",
        "resultado": "1-0"
    }
}
```

**Homepage após Partida (Maria):**

```
┌──────────────────────────────────────────────┐
│ COPA SUDESTE 2025 - Status Atualizado       │
├──────────────────────────────────────────────┤
│                                              │
│ Status: ⚽ EM ANDAMENTO                      │
│ Fase: Grupos (Rodada 1/3)                   │
│                                              │
│ Meu Grupo: A                                │
│ ┌──────────────────────────────────────┐   │
│ │ Maria    │ W: 1 L: 0 D: 0 (Você) ⬆️  │   │
│ │ Lucas    │ W: 0 L: 0 D: 0           │   │
│ │ Gisele   │ W: 0 L: 0 D: 0           │   │
│ │ Ana      │ W: 0 L: 1 D: 0           │   │
│ └──────────────────────────────────────┘   │
│                                              │
│ ✅ Partida registrada: Maria 1-0 Ana       │
│ Rating: 1620 → 1634 (+14)                   │
│                                              │
│ Próxima Partida:                           │
│ 📅 21 nov: Maria vs Lucas                   │
│ [Ver Ordem de Jogos]                        │
│                                              │
└──────────────────────────────────────────────┘
```

**[Após todas 3 rodadas de Grupos - 25 nov]**

```
Resultado final Grupo A:
┌────────────────────────────────────────┐
│ 1. Maria    │ 2-1 (Rating: 1664)       │ ✅ Qualificada
│ 2. Lucas    │ 2-1 (Rating: 1545)       │ ✅ Qualificada
│ 3. Ana      │ 1-2 (Rating: 1510)       │ ❌ Eliminada
│ 4. Gisele   │ 0-3 (Rating: 1430)       │ ❌ Eliminada
└────────────────────────────────────────┘

Qualificados de todos grupos:
└─ Semifinal: Maria (A), Lucas (A), João P (B), Beatriz (B)
```

---

### Semana 3: Fase Eliminatória

#### 🗓️ 26-27 de novembro (Semifinal)

```
Semifinal:
├─ Maria vs João P
└─ Lucas vs Beatriz

27 nov - Resultados:
├─ Maria vence João P
└─ Lucas perde para Beatriz

Finais: Maria vs Beatriz
```

---

#### 🗓️ 28 de novembro (Final)

```
Final:
└─ Maria 1-0 Beatriz

🏆 VENCEDOR: Maria!
```

**Evento Finalizado:**

```python
# Sistema auomaticamente:

# 1. Calcula ranking FINAL
rankings_finais = {
    "evento": {
        "1º lugar": ("Maria", 1690),
        "2º lugar": ("Beatriz", 1560),
        "3º lugar": ("Lucas", 1540),
        "4º lugar": ("João P", 1495),
    }
}

# 2. Atualiza RANKING_GRUPO (agregado)
# Recalcula ranking geral do Grupo "Sudeste"
# com base em TODOS eventos do grupo

ranking_sudeste_atualizado = {
    "Maria": {
        "posicao": 2,          # subiu de #3 para #2 globalmente
        "rating": 1664,         # média de eventos
        "eventos_jogados": 5,
        "vitorias": 32,
        "derrotas": 13
    },
    "Lucas": {
        "posicao": 8,
        "rating": 1545,
        # ...
    }
}

# 3. Notifica todos
Email: "Copa Sudeste 2025 finalizada! Maria é a campeã!"

# 4. Cria certificado (opcional)
# PDF com resultado final

# 5. Registra no histórico
# event_history: evento finalizado em 28 nov
# rankings preserved forever
```

**Homepage Final (Maria):**

```
┌──────────────────────────────────────────────┐
│         🏆 PARABÉNS, MARIA! 🏆              │
├──────────────────────────────────────────────┤
│                                              │
│ Você é CAMPEÃ da Copa Sudeste 2025!         │
│                                              │
│ Seu desempenho:                             │
│ ┌──────────────────────────────────────┐   │
│ │ Grupo A: 2-1 (1º lugar)              │   │
│ │ Semifinal: Venceu João P (1-0)       │   │
│ │ Final: Venceu Beatriz (1-0)          │   │
│ │                                       │   │
│ │ Rating global: 1620 → 1664 (+44)     │   │
│ │ Ranking grupo: #3 → #2               │   │
│ └──────────────────────────────────────┘   │
│                                              │
│ [Baixar Certificado] [Compartilhar]         │
│                                              │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│     📊 SEU NOVO RANKING (Sudeste)           │
├──────────────────────────────────────────────┤
│ Posição: #2 (↑ 1 posição)                   │
│ Rating: 1664 | W: 32 L: 13 D: 1             │
│ [Ver Ranking Completo]                      │
└──────────────────────────────────────────────┘
```

---

## 👥 Perspectiva de Outras Roles

### 📱 Vista do Jogador (Ana - Eliminada em Grupos)

```
Após derrota na fase de grupos:

┌─────────────────────────────────────┐
│  Copa Sudeste 2025 - Seu Resultado  │
├─────────────────────────────────────┤
│                                     │
│ Fase: Grupos ❌ Eliminada           │
│ Sua posição: 4º lugar no Grupo A    │
│ Record: 1-2 (derrota para Maria)    │
│ Rating: 1540 → 1510 (-30)           │
│                                     │
│ [Próximos eventos]                  │
│ [Análise de desempenho]             │
│                                     │
└─────────────────────────────────────┘

Permissões Ana:
✅ Ver ranking (evento finalizado)
✅ Ver seu desempenho
✅ Se inscrever em próximos eventos
❌ Editar resultado (apenas organizador)
❌ Ver partidas não finalizadas
```

### 👨‍💼 Vista do Organizador (João)

```
Dashboard Organizador:

┌──────────────────────────────────────────┐
│ Copa Sudeste 2025 - Painel do Organizador│
├──────────────────────────────────────────┤
│                                          │
│ Status: FINALIZADO ✅                    │
│ Data: 20-28 nov | Jogadores: 12         │
│                                          │
│ [Estatísticas]                          │
│ ├─ Total partidas: 16                   │
│ ├─ Partidas registradas: 16/16 ✅       │
│ ├─ Rating médio: 1550                   │
│ └─ Vitórias/Derrotas mais altas         │
│                                          │
│ [Ações]                                 │
│ ├─ [Editar Rankings] (admin pode)       │
│ ├─ [Exportar Resultados] (PDF)          │
│ ├─ [Auditoria]                          │
│ └─ [Deletar Evento] ❌ (já finalizado)  │
│                                          │
│ [Criar Próximo Evento]                  │
│ └─ [Nova Copa Sudeste 2026?]            │
│                                          │
└──────────────────────────────────────────┘

Auditoria do Evento:
log_id | usuario | acao | recurso | data
-------|---------|------|---------|------
1      | João    | criar_evento | 101 | 15-nov
2      | Maria   | inscrever | 101 | 16-nov
... (150+ linhas) ...
250    | Sistema | finalizou | 101 | 28-nov
```

---

## 🔄 Ciclo de Memberships (Histórico)

**Exemplo: Pedro em "Sudeste"**

```
┌─────────────────────────────────────────────────────┐
│ Historia de Pedro no Grupo "Sudeste"               │
├─────────────────────────────────────────────────────┤

data_entrada: 2024-01-15
data_saida:   NULL (ainda ativo)
status:       ativo

EVENTOS PARTICIPADOS:
├─ Copa Sudeste 2024 (jan) ✅ (ranking: #8)
├─ Torneio Spring 2024 (abr) ✅ (ranking: #6)
├─ Copa Sudeste 2025 (nov) ✅ (ranking: #8) ← agora
│
RANKINGS NO GRUPO:
├─ Global: #8 (média de todos eventos)
├─ 2024: #7
└─ 2025: #8

SE Pedro sair em dez 2025:
├─ data_saida = 2025-12-01
├─ status = inativo
└─ rankings históricos = preservados
```

---

## 📊 Relatório de Auditoria

```
EVENTO: Copa Sudeste 2025 (ID: 101)
PERÍODO: 15 nov - 28 nov 2025
AÇÕES REGISTRADAS: 247

┌─────────────────────────────────────────────┐
│        Atividades por Usuário               │
├─────────────────────────────────────────────┤
│ João (organizador): 18 ações                │
│ ├─ 1 criar_evento                          │
│ ├─ 12 registrar_partida                    │
│ ├─ 3 editar_resultado                      │
│ ├─ 2 notificar_jogadores                   │
│ └─ 0 remover_jogador (nenhuma)             │
│                                             │
│ Maria (jogadora): 12 ações                  │
│ ├─ 1 inscrever                             │
│ ├─ 11 ver_ranking (consultou 11x)          │
│ └─ 0 ações ilegais                         │
│                                             │
│ [outros 10 jogadores]: lançaram 217 ações  │
│                                             │
│ SISTEMA (automático): 82 ações             │
│ ├─ criar_grupos                            │
│ ├─ calcular_ranking                        │
│ ├─ enviar_notificacoes                     │
│ └─ finalizar_evento                        │
│                                             │
└─────────────────────────────────────────────┘

✅ CONFORMIDADE: 100%
- Nenhuma ação não autorizada
- Nenhuma manipulação de rankings
- Todos registros íntegros
```

---

## 💡 Lições Aprendidas

1. **Isolamento por Grupo Funciona**: Maria mantém #3 em Sudeste, poderia ter #15 em Online
2. **Timeline é Crítica**: Jogador que saiu em março vs participou em janeiro = rankings preservados
3. **Auditoria Essencial**: Rastrear quem registrou cada partida é vital
4. **Notificações Importantes**: Manter jogadores informados do status
5. **RBAC Evita Abuso**: Organização não pode ser feita por jogador casual

---

**Este exemplo serve como blueprint para testes e documentação do usuário.**
