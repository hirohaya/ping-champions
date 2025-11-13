# Feature 2 - Nova Estrutura de Usuários ✅ IMPLEMENTADA

## Visão Geral

Implementação completa do sistema de usuários com 3 tipos de papéis (roles) conforme especificado em Feature 2.

## Arquitetura

### 3 Tipos de Usuários

```
┌─────────────────────────────────────────────┐
│           ADMINISTRADOR (Admin)             │
│  - Acesso total ao sistema                  │
│  - Gerenciar organizadores e jogadores      │
│  - Visualizar relatórios do sistema         │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│         ORGANIZADOR (Organizer)             │
│  - Criar eventos                            │
│  - Gerenciar jogadores nos eventos          │
│  - Visualizar rankings dos seus eventos     │
│  - Também é um JOGADOR (pode participar)    │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│             JOGADOR (Player)                │
│  - Participar de eventos                    │
│  - Ver próprio ranking por grupo            │
│  - Participar de torneios                   │
└─────────────────────────────────────────────┘
```

## Modelos Implementados

### 1. **User Model** (`backend/models/user.py`)

```python
class UserRole(str, enum.Enum):
    ADMIN = "admin"          # Administrador
    ORGANIZER = "organizer"  # Organizador
    PLAYER = "player"        # Jogador

class User(Base):
    id: int                  # ID único
    email: str              # Email único para login
    password_hash: str      # Senha hasheada com bcrypt
    name: str               # Nome completo
    role: UserRole          # Tipo de usuário
    active: bool            # Status (ativo/inativo)
    created_at: datetime    # Data de criação
    updated_at: datetime    # Última atualização
    
    # Properties para fácil acesso
    @property
    def is_admin() -> bool
    @property
    def is_organizer() -> bool
    @property
    def is_player() -> bool
    @property
    def is_admin_or_organizer() -> bool
```

## Endpoints Implementados

### Autenticação (`/users`)

#### 1. **POST /users/register** - Registrar Novo Usuário
```bash
curl -X POST "http://127.0.0.1:8000/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "novo@email.com",
    "password": "senha123",
    "name": "Novo Usuário",
    "role": "player"
  }'
```

**Resposta (201 Created)**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "novo@email.com",
    "name": "Novo Usuário",
    "role": "player",
    "active": true,
    "created_at": "2025-11-13T12:00:00",
    "updated_at": "2025-11-13T12:00:00"
  }
}
```

#### 2. **POST /users/login** - Fazer Login
```bash
curl -X POST "http://127.0.0.1:8000/users/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@pingchampions.com",
    "password": "admin123"
  }'
```

**Resposta (200 OK)**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "admin@pingchampions.com",
    "name": "Administrador",
    "role": "admin",
    "active": true,
    "created_at": "2025-11-13T12:00:00",
    "updated_at": "2025-11-13T12:00:00"
  }
}
```

#### 3. **GET /users/{user_id}** - Obter Usuário
```bash
curl "http://127.0.0.1:8000/users/1"
```

#### 4. **GET /users** - Listar Todos os Usuários (Paginado)
```bash
curl "http://127.0.0.1:8000/users?skip=0&limit=10"
```

#### 5. **GET /users/role/{role}** - Listar por Role
```bash
curl "http://127.0.0.1:8000/users/role/admin"
curl "http://127.0.0.1:8000/users/role/organizer"
curl "http://127.0.0.1:8000/users/role/player"
```

## Segurança Implementada

### 1. **Hash de Senha** (Bcrypt)
- Senhas nunca são armazenadas em texto plano
- Cada usuário tem um salt único
- Impossível recuperar senha original do hash

### 2. **Autenticação JWT**
- Tokens com expiração (30 minutos por padrão)
- Contém ID do usuário e email
- Pode ser usado em próximas requisições

### 3. **Validações**
- Email único obrigatório
- Email com formato válido (Pydantic EmailStr)
- Apenas organizadores e jogadores podem se registrar (admin requer autorização)
- Usuários inativos não podem fazer login

## Credenciais de Teste

Já criadas automaticamente com `create_test_users.py`:

```
🔴 ADMINISTRADOR:
   Email: admin@pingchampions.com
   Senha: admin123

🟠 ORGANIZADOR:
   Email: organizador@pingchampions.com
   Senha: org123

🟢 JOGADORES:
   1. jogador1@pingchampions.com / player1
   2. jogador2@pingchampions.com / player2
   3. jogador3@pingchampions.com / player3
```

## Próximos Passos - Feature 2 (Phase 2)

- [ ] Middleware de autenticação para proteger endpoints
- [ ] Validação de permissões (admin/organizer checks)
- [ ] Endpoint para atualizar usuário
- [ ] Endpoint para deactivar usuário
- [ ] Endpoint para reset de senha
- [ ] Sistema de convites para admin/organizer
- [ ] Histórico de login

## Próximos Passos - Feature 1 (Paralelamente)

- [ ] Modelo de Group
- [ ] Endpoints para Group CRUD
- [ ] Associação de Players a Groups
- [ ] Ranking por Group

## Arquivos Criados/Modificados

### Novos Arquivos:
- ✅ `backend/models/user.py` - Model User com UserRole enum
- ✅ `backend/routers/users.py` - Router com endpoints de auth
- ✅ `backend/create_test_users.py` - Script de dados teste

### Modificados:
- ✅ `backend/models/__init__.py` - Adicionado User e UserRole
- ✅ `backend/main.py` - Registrado router users
- ✅ `backend/requirements.txt` - Adicionadas dependências

### Tabelas Criadas:
- ✅ `users` - Tabela principal de usuários

## Status

✅ **IMPLEMENTAÇÃO COMPLETA**
- Modelo User com 3 roles
- Endpoints de registro e login
- Hash de senha com bcrypt
- Tokens JWT
- Dados de teste criados
- Documentação completa

## Como Testar

1. **Backend rodando**:
   ```bash
   cd backend
   python run_backend.py
   ```

2. **Verificar Swagger Docs**:
   ```
   http://127.0.0.1:8000/docs
   ```

3. **Testar endpoints** (veja exemplos acima)

---

**Status**: ✅ Feature 2 Fase 1 Completa
**Próximo**: Implementar Feature 1 (Groups) ou continuar Feature 2 (Fase 2)
**Branch**: test-fixes-e2e
