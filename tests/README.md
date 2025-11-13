# 🧪 TESTES - Ping Champions

Testes automatizados organizados por tipo e escopo.

## 📁 Estrutura

```
tests/
├── unit/           - Testes unitários (10 arquivos)
│   ├── test_elo.py
│   ├── test_membership_unit.py
│   ├── test_events.py
│   ├── test_players.py
│   ├── test_matches.py
│   ├── test_ranking.py
│   └── ...
│
├── e2e/            - Testes end-to-end (4 arquivos)
│   ├── test_membership_direct.py   ✅ 15/15 passando
│   ├── test_membership_e2e.py
│   ├── test_elo_e2e.py
│   └── test_e2e.py
│
└── integration/    - Testes de integração (2 arquivos)
    ├── test_complete.py
    └── test_server_startup.py
```

## 🚀 Quick Start

### Rodar Todos os Testes
```bash
pytest tests/
```

### Rodar por Tipo
```bash
# Unit tests apenas
pytest tests/unit/

# E2E tests apenas
pytest tests/e2e/

# Integration tests apenas
pytest tests/integration/
```

### Com Coverage
```bash
pytest tests/ --cov=backend --cov-report=html
```

## 📊 Status Atual

| Tipo | Arquivos | Status |
|------|----------|--------|
| Unit | 10 | ✅ |
| E2E | 4 | ✅ (15/15 no Membership) |
| Integration | 2 | ✅ |
| **Total** | **16** | **✅** |

## 📖 Documentação Detalhada

Veja README.md em cada subpasta:
- [Unit Tests](unit/README.md)
- [E2E Tests](e2e/README.md)
- [Integration Tests](integration/README.md)

## 🔑 Principais Testes

**ELO System:**
- `test_elo.py` - Cálculos e ajustes de rating
- `test_elo_e2e.py` - Fluxo completo ELO

**Membership Lifecycle:**
- `test_membership_unit.py` - 15 testes unitários (todas transições)
- `test_membership_direct.py` - 15 cenários E2E completos ✅
- `test_membership_e2e.py` - Testes via HTTP

**Sistema Completo:**
- `test_complete.py` - Integração total
- `test_events.py`, `test_players.py`, `test_matches.py` - CRUD

## 💡 Boas Práticas

1. **Antes de commitar**: Rodar `pytest tests/`
2. **Antes de merge**: Validar coverage com `--cov`
3. **Novo código**: Escrever testes primeiro (TDD)
4. **Testes lentos**: Marcar com `@pytest.mark.slow`

## 🐛 Troubleshooting

Se os testes falharem:
1. Verifique se o banco de dados está limpo
2. Valide imports em `conftest.py`
3. Confirme backend está parado (para unit/integration)
4. Limpe cache: `rm -r .pytest_cache/`

