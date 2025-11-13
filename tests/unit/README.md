# 🧪 UNIT TESTS

Testes unitários de componentes individuais.

## Arquivos

- **test_elo.py** - Testes do sistema ELO
- **test_elo_unit.py** - Testes unitários adicionais do ELO
- **test_membership_unit.py** - Testes do modelo Membership (15 cenários)
- **test_events.py** - Testes de eventos
- **test_players.py** - Testes de jogadores
- **test_matches.py** - Testes de partidas
- **test_ranking.py** - Testes de ranking
- **test_collate.py** - Testes de collate/encoding
- **conftest.py** - Configuração pytest
- **__init__.py** - Inicialização do pacote

## Como Rodar

```bash
# Rodar todos os testes unitários
pytest tests/unit/

# Rodar teste específico
pytest tests/unit/test_elo.py

# Rodar com coverage
pytest tests/unit/ --cov=backend --cov-report=html
```

## Coverage

Os testes unitários cobrem:
- Cálculos de ELO
- Modelo de Membership com 5 estados
- CRUD de eventos, jogadores, partidas
- Validações de ranking

