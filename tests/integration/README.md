# 🔗 INTEGRATION TESTS

Testes de integração que validam múltiplos componentes juntos.

## Arquivos

- **test_complete.py** - Suite de testes de integração completa
- **test_server_startup.py** - Testes de inicialização do servidor

## Características

### test_complete.py
- Testes de integração entre módulos
- Validação de fluxos multi-etapas
- Integração com banco de dados

### test_server_startup.py
- Valida inicialização correta do FastAPI
- Testa carregamento de routers
- Verifica estado inicial da aplicação

## Como Rodar

```bash
# Rodar todos os testes de integração
pytest tests/integration/

# Rodar teste específico
pytest tests/integration/test_complete.py

# Rodar com output detalhado
pytest tests/integration/ -v -s
```

## Notas

- Podem requer banco de dados em estado limpo
- Algumas situações podem requerer backend em execução

