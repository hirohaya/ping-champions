# 🌐 E2E TESTS

Testes end-to-end que validam fluxos completos do sistema.

## Arquivos

- **test_e2e.py** - Testes E2E gerais
- **test_elo_e2e.py** - Testes E2E do sistema ELO
- **test_membership_e2e.py** - Testes E2E do Membership (HTTP-based)
- **test_membership_direct.py** - Testes E2E do Membership (direct DB)

## Características

### test_membership_direct.py
- 15 cenários de teste
- Acesso direto ao banco de dados (sem HTTP)
- Valida ciclo de vida completo do Membership
- Status: ✅ 15/15 testes passando

### test_membership_e2e.py
- Testes via HTTP
- Valida API REST de Membership
- Estado: Alternativa ao test_membership_direct.py

### test_elo_e2e.py
- Testes do sistema ELO completo
- Validação de cálculos de rating
- Histórico de partidas

## Como Rodar

```bash
# Rodar todos os testes E2E
pytest tests/e2e/

# Rodar teste específico
pytest tests/e2e/test_membership_direct.py

# Rodar com verbose
pytest tests/e2e/ -v
```

## Requisitos

- Backend em funcionamento (para testes HTTP-based)
- Banco de dados configurado (para testes direct DB)

