"""
Configuração centralizada do aplicativo Ping Champions
"""

# Limites de requisição
MAX_REQUEST_BODY_SIZE = 100 * 1024 * 1024  # 100MB (padrão é ~2.5MB)
MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100MB para uploads

# Configuração do banco de dados
DATABASE_URL = "sqlite:///pingchampions.db"

# Configuração de CORS
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]

# Configuração de servidor
HOST = "127.0.0.1"
PORT = 8000
RELOAD = True

# Outras configurações
DEBUG = True
