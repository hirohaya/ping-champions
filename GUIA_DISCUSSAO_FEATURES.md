# Guia de Discussão - Refinement das Features

**Objetivo:** Validar features propostas com o time antes de desenvolvimento  
**Formato:** Perguntas orientadas para consenso
**Duração recomendada:** 2-3 reuniões de 1 hora cada

---

## 🎯 Sessão 1: Feature 1 - Organização de Partidas

### Bloco 1: Hierarquia e Escopo

**Pergunta 1.1:** A hierarquia Grupo → Evento é definitiva?
- Grupo: Contém múltiplos eventos, agrupa jogadores
- Evento: Torneio específico dentro de grupo
- Decisão: ☐ SIM ☐ NÃO ☐ TALVEZ (precisa subgrupos)

**Pergunta 1.2:** Um evento pode conter múltiplos tipos de torneio?
- Exemplo: Mesmo evento com "Fase de Grupos" E "Eliminatório"?
- Decisão: ☐ SIM ☐ NÃO ☐ DEPOIS (v2)

**Pergunta 1.3:** Jogadores fora do grupo podem participar de seus eventos?
- Cenário: Jogador de SP participa evento do grupo RJ?
- Decisão: ☐ SIM ☐ NÃO ☐ COM APROVAÇÃO

---

### Bloco 2: Cálculo de Ranking

**Pergunta 2.1:** Qual fórmula de ranking usar?
```
☐ ELO (tradicional, usado em xadrez/LoL)
  ├─ Vantagem: Conhecido, justo
  ├─ Desvantagem: Complexo
  └─ K-factor sugerido: 32

☐ Win Rate (%, simples)
  ├─ Vantagem: Fácil entender
  ├─ Desvantagem: Não considera força do oponente
  └─ Exemplo: 10 vitórias, 5 derrotas = 66.67%

☐ Pontos Acumulativos (vitória=3, derrota=0)
  ├─ Vantagem: Muito simples
  ├─ Desvantagem: Pode ficar monótono
  └─ Exemplo: 10 vitórias = 30 pontos

☐ Outro: ________________
```

**Pergunta 2.2:** Com que frequência recalcular rankings?
```
☐ Real-time (após cada partida)
  └─ Custo: Alto, precisa cache + background jobs

☐ Diário (uma vez por dia à noite)
  └─ Custo: Baixo, mas dados atrasados

☐ Sob demanda (quando usuário acessa)
  └─ Custo: Médio, pode ter delay

☐ Híbrido: Real-time (evento), Diário (grupo)
  └─ Recomendação: Esta é a melhor prática
```

**Pergunta 2.3:** Qual é o rating inicial de um jogador?
```
☐ 1600 (padrão ELO)
☐ 1200 (mais acessível)
☐ Baseado em eventos anteriores
☐ Outra: ________________
```

---

### Bloco 3: Tipos de Torneio

**Pergunta 3.1:** Qual tipo implementar PRIMEIRO?
```
1º: ☐ Simples (1v1) - base para outros
2º: ☐ Eliminatório
3º: ☐ Fase de Grupos + Eliminatório
4º: ☐ Rodada Suíça (deixar para v2)
```

**Pergunta 3.2:** Para Eliminatório, qual tamanho suportar?
```
☐ 8 jogadores
☐ 8, 16, 32 (adaptável)
☐ 8, 16, 32, 64 (completo)
☐ Qualquer número (BYE automático)
```

**Pergunta 3.3:** Para Fase de Grupos, como definir grupos?
```
Opção A: Manual (admin defini manualmente)
☐ Vantagem: Controle total
☐ Desvantagem: Trabalhoso

Opção B: Automático (aleatório)
☐ Vantagem: Rápido
☐ Desvantagem: Pode ficar desbalanceado

Opção C: Balanceado (seed por rating)
☐ Vantagem: Justo e rápido
☐ Desvantagem: Mais complexo
Recomendação: Escolha esta

Decisão: ☐ A ☐ B ☐ C
```

---

### Bloco 4: Memberships e Timeline

**Pergunta 4.1:** O que acontece com ranking se jogador SAIR do grupo?
```
Cenário: Jogador A sai do Grupo 1 em março,
mas tem eventos em janeiro.

☐ Ranking dele conta (dados históricos)
☐ Ranking dele NÃO conta (remove do histórico)
☐ Ranking conta, mas marcado como "inativo"

Recomendação: Opção 1 (dados históricos preservados)
Decisão: ☐
```

**Pergunta 4.2:** Qual é o ciclo de vida de membership?
```
Convite → Aceita → Ativo → Saída?

OU

Direto → Ativo → Saída?

OU

Admin adiciona → Ativo → Saída?

Decisão: ☐
```

**Pergunta 4.3:** Jogador pode reentrar em grupo após sair?
```
☐ SIM, sempre
☐ NÃO, uma vez que sai é para sempre
☐ COM APROVAÇÃO do admin
☐ SIM, mas com penalidade/reset de ranking

Decisão: ☐
```

---

## 🔐 Sessão 2: Feature 2 - Usuários e RBAC

### Bloco 1: Hierarquia de Roles

**Pergunta 1.1:** Confirmar roles propostos:
```
✅ SUPERADMIN (controla tudo)
✅ ADMIN_GRUPO (admin de 1 grupo)
✅ ORGANIZADOR (cria eventos)
✅ JOGADOR (participa)

Adicionar:
☐ MODERADOR (resolve disputas)
☐ ARBITRO (registra partidas)
☐ Outro: ________________
```

**Pergunta 1.2:** Um organizador pode ser admin de múltiplos grupos?
```
Cenário: João é organizador em RJ E SP?

☐ NÃO, uma role por grupo
☐ SIM, pode ter múltiplas roles
☐ SIM, mas com aprovação

Recomendação: SIM (permite flexibilidade)
Decisão: ☐
```

**Pergunta 1.3:** Um admin de grupo é jogador ou não?
```
☐ SIM, admin é também jogador (pode participar eventos)
☐ NÃO, admin é administrativo puro
☐ Depende (pode ser configurado)

Recomendação: SIM (permite jogar em seus próprios eventos)
Decisão: ☐
```

---

### Bloco 2: Permissões Granulares

**Pergunta 2.1:** Um jogador pode se REMOVER de um evento iniciado?
```
Cenário: Evento começou, jogador pede para sair.

☐ SIM, sempre (perda para seu ranking)
☐ NÃO, nunca (prejudica o torneio)
☐ SIM, mas com penalidade
☐ Depende do tipo de torneio

Recomendação: Opção 2 (impede abandono)
Decisão: ☐
```

**Pergunta 2.2:** Quem pode REGISTRAR uma partida?
```
☐ Qualquer jogador (confiança)
☐ Organizador do evento (controle)
☐ Árbitro designado (formal)
☐ Ambos jogadores (consenso)

Recomendação: Opção 2 ou 3
Decisão: ☐
```

**Pergunta 2.3:** Quem pode EDITAR um ranking já calculado?
```
☐ Ninguém (imutável)
☐ Admin grupo (com log de auditoria)
☐ Superadmin (com log de auditoria)
☐ Moderador (para resolver disputas)

Recomendação: Opção 2 + 4 (com auditoria)
Decisão: ☐
```

---

### Bloco 3: Autenticação e Sessão

**Pergunta 3.1:** Como usuários se autenticam?
```
☐ Usuário/Senha (JWT recomendado)
☐ Google OAuth
☐ GitHub OAuth
☐ Múltiplas opções (Usuário/Senha + Google)

Recomendação: Usuário/Senha com JWT
Decisão: ☐
```

**Pergunta 3.2:** Quanto tempo tokens duram?
```
Access Token (curta duração):
☐ 15 minutos ← Recomendado
☐ 30 minutos
☐ 1 hora

Refresh Token (longa duração):
☐ 7 dias ← Recomendado
☐ 30 dias
☐ 365 dias

Decisão: ☐ access/refresh proposto
```

**Pergunta 3.3:** Implementar "Remember me"?
```
☐ SIM (sessão mais longa)
☐ NÃO (sempre relogin)

Decisão: ☐
```

---

### Bloco 4: Entrada em Grupos

**Pergunta 4.1:** Como um jogador ENTRA em um grupo?
```
Opção A: Auto-register (cria conta, entra em grupo público)
☐ Vantagem: Rápido onboarding
☐ Desvantagem: Pode gerar spam

Opção B: Convite (admin convida)
☐ Vantagem: Controle
☐ Desvantagem: Lento

Opção C: Ambos (grupos públicos + convites)
☐ Vantagem: Flexível
☐ Desvantagem: Mais complexo

Recomendação: Opção C
Decisão: ☐
```

**Pergunta 4.2:** Grupos visíveis na listagem global?
```
Cenário: Jogador novo procura grupos para entrar.

Opção A: Todos os grupos públicos listados
Opção B: Apenas grupos que está convidado
Opção C: Ambos (com filtro)

Decisão: ☐
```

---

## 🎨 Sessão 3: Feature 3 - Homepage e UX

### Bloco 1: Layout e Informações

**Pergunta 1.1:** Homepage deve mostrar quais informações?
```
☐ Meus grupos (com quick stats)
☐ Próximos eventos (todos os grupos ou selecionado?)
☐ Meu ranking (por grupo)
☐ Notificações (convites, partidas para jogar)
☐ Ações rápidas (criar evento, inscrever)
☐ Feed de atividades recentes
☐ Sugestões de novos grupos

Todas necessárias? Ou priorizar?
Recomendação: Tudo exceto feed/sugestões (v1.1)
Decisão: ☐
```

**Pergunta 1.2:** Quando usuário seleciona grupo, o que muda?
```
☐ Próximos eventos (filtrados)
☐ Ranking (do grupo selecionado)
☐ Ações (criar evento in este grupo)
☐ Tudo acima

Decisão: ☐ Tudo
```

**Pergunta 1.3:** Mostrar apenas MEUS grupos ou TODOS os grupos?
```
☐ Apenas meus grupos (default)
☐ Meus grupos + botão "procurar"
☐ Todos os grupos (listagem global)

Decisão: ☐
```

---

### Bloco 2: Componentes e Interações

**Pergunta 2.1:** GroupSelector deve ser:
```
☐ Dropdown (seletor)
☐ Cards horizontais (clicáveis)
☐ Sidebar (sempre visível)
☐ Tabs

Recomendação: Cards horizontais (mais visual)
Decisão: ☐
```

**Pergunta 2.2:** Ranking deve mostrar:
```
☐ Posição
☐ Rating (número)
☐ Vitórias/Derrotas/Empates
☐ Próximo adversário
☐ Tendência (seta para cima/baixo)

Decisão: ☐
```

**Pergunta 2.3:** Próximos eventos deve ser:
```
☐ Lista (vertical)
☐ Grid (cards)
☐ Mapa/timeline (por data)

Recomendação: Cards em grid
Decisão: ☐
```

---

### Bloco 3: Mobile e Performance

**Pergunta 3.1:** Homepage deve ser mobile-first?
```
☐ SIM, design para mobile depois desktop
☐ NÃO, desktop first depois adaptar
☐ SIM, responsive design

Recomendação: Responsivo desde o início
Decisão: ☐
```

**Pergunta 3.2:** Dados devem carregar:
```
☐ Tudo junto (aguarda tudo)
☐ Progressivo (cada seção carrega)
☐ Lazy loading (ao scroll)

Recomendação: Progressivo
Decisão: ☐
```

---

## 📋 Resumo de Decisões

Use esta tabela para registrar as decisões do time:

| Pergunta | Opção A | Opção B | Opção C | Decisão | Observações |
|----------|---------|---------|---------|---------|-------------|
| 1.1 Hierarquia | SIM | NÃO | TALVEZ | ☐ | |
| 2.1 Fórmula Ranking | ELO | Win% | Pontos | ☐ | |
| 2.2 Frequência | Real-time | Diário | Híbrido | ☐ | |
| 3.1 Tipo Prioridade | Simples | Elim | Grupos | ☐ | |
| 4.1 Jogador Sai | Conta | N/Conta | Marcado | ☐ | |
| 1.1 (F2) Roles | Atual | +Mod | +Árbitro | ☐ | |
| 3.1 Autenticação | Pwd | OAuth | Múltiplo | ☐ | |
| 4.1 Entrada | Auto | Convite | Ambos | ☐ | |
| 1.1 (F3) Infos | Todas | Principais | Customizável | ☐ | |
| 3.1 (F3) Mobile | Mobile-first | Desktop | Responsivo | ☐ | |

---

## 🎬 Próximos Passos Após Decisões

1. **Documentar decisões** (arquivo DECISIONS.md)
2. **Criar user stories** com base nas decisões
3. **Estimar pontos** de complexidade
4. **Planejar sprints** (com base em prioridades)
5. **Validar com stakeholders** (PO, usuarios finais)

---

## 💬 Notas de Discussão

### Sessão 1 (Data: ___/___/___):
```
Presentes: ________________

Consensos alcançados:
☐ 
☐ 
☐ 

Discordâncias/Pontos abertos:
☐ 
☐ 

Ações:
☐ 
☐ 
```

### Sessão 2 (Data: ___/___/___):
```
Presentes: ________________

Consensos alcançados:
☐ 
☐ 

Discordâncias/Pontos abertos:
☐ 

Ações:
☐ 
```

### Sessão 3 (Data: ___/___/___):
```
Presentes: ________________

Consensos alcançados:
☐ 

Discordâncias/Pontos abertos:
☐ 

Ações:
☐ 
```

---

**Facilitador recomendado:** Tech Lead / Product Owner  
**Tempo total recomendado:** 3-4 horas  
**Documento de saída:** DECISIONS.md com todas as decisões registradas
