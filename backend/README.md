# Backend FastAPI - Ping Champions

Este diretório contém o backend do sistema de gerenciamento de eventos, ranking e pontuação de jogadores de tênis de mesa.

## Como rodar localmente

1. Crie um ambiente virtual:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
2. Instale as dependências:
   ```powershell
   pip install fastapi uvicorn[standard] sqlalchemy
   ```
3. Não é necessário configurar variáveis de ambiente para SQLite.
4. Inicie o servidor:
   ```powershell
   uvicorn main:app --reload
   ```

## Estrutura inicial sugerida
- `main.py`: ponto de entrada FastAPI
- `models/`: modelos SQLAlchemy
- `routers/`: rotas da API
- `database.py`: conexão com SQLite

## Integração com o Frontend
O frontend Vue.js se comunica com este backend via requisições HTTP (ex: axios/fetch) para os endpoints definidos nas rotas.

Certifique-se de que o backend esteja rodando antes de iniciar o frontend.


## Endpoints principais

### Listar eventos
- **GET** `/eventos`
- Retorna todos os eventos ativos (`ativo = true`).

### Criar evento
- **POST** `/eventos`
- Body (JSON):
   ```json
   {
      "nome": "Nome do evento",
      "data": "2025-09-25",
      "horario": "19:00"
   }
   ```
- Retorna o evento criado.

### Apagar evento (soft delete)
- **POST** `/eventos/apagar/{evento_id}`
- Marca o evento como inativo (`ativo = false`).
- Não remove do banco, apenas oculta do frontend.

### Observações
- O campo `ativo` controla a visualização dos eventos.
- Para ver todos os endpoints e schemas, acesse `/docs` (Swagger UI).

---

## Status do Projeto

### Funcionalidades já implementadas
- Estrutura de modelos, rotas e conexão com SQLite
- Endpoints para eventos (criação, listagem, remoção com soft delete)
- Endpoints para jogadores (cadastro, listagem por evento)
- Integração básica com frontend

### Próximas tarefas
- Endpoints para jogos (criação, controle, visualização)
- Endpoints para ranking
- Permitir remoção/edição de jogadores
- Implementar sistema de pareamento automático
- Autenticação de administrador
- Histórico de eventos e estatísticas

