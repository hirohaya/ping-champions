"""
Users Router - Autenticação e gerenciamento de usuários

Endpoints:
  - POST /users/register: Registrar novo usuário
  - POST /users/login: Login de usuário
  - GET /users/{user_id}: Obter detalhes do usuário
  - PUT /users/{user_id}: Atualizar usuário
  - GET /users: Listar usuários (admin only)
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import jwt
import bcrypt
from pydantic import BaseModel, EmailStr

from database import SessionLocal
from models import User, UserRole

router = APIRouter(prefix="/users", tags=["users"])

# Configuração de JWT
SECRET_KEY = "sua-chave-secreta-aqui-mude-em-producao"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Schemas Pydantic
class UserRegister(BaseModel):
    """Schema para registrar novo usuário"""
    email: EmailStr
    password: str
    name: str
    role: UserRole = UserRole.PLAYER


class UserLogin(BaseModel):
    """Schema para login"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema para resposta de usuário"""
    id: int
    email: str
    name: str
    role: UserRole
    active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema para resposta de token"""
    access_token: str
    token_type: str
    user: UserResponse


# Funções auxiliares
def hash_password(password: str) -> str:
    """Hash de senha usando bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """Verificar se senha corresponde ao hash"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))


def create_access_token(user_id: int, user_email: str, expires_delta: Optional[timedelta] = None):
    """Criar token JWT"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "sub": str(user_id),
        "email": user_email,
        "exp": expire
    }
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Endpoints
@router.post("/register", response_model=TokenResponse, status_code=201)
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Registrar novo usuário na plataforma
    
    Tipos de usuário:
    - player: Jogador (padrão)
    - organizer: Organizador de eventos
    - admin: Administrador (requer autorização especial)
    
    Retorna token JWT para login automático
    """
    # Validar se email já existe
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já registrado")
    
    # Validar role (apenas admin pode criar outros admins)
    if user_data.role == UserRole.ADMIN:
        # TODO: Implementar validação de permissão de admin
        # Por enquanto, apenas permitir player e organizer
        raise HTTPException(
            status_code=403,
            detail="Apenas administradores podem criar outras contas de admin. Contate suporte."
        )
    
    # Criar novo usuário
    user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        name=user_data.name,
        role=user_data.role,
        active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Criar token JWT
    access_token = create_access_token(user.id, user.email)
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.from_orm(user)
    )


@router.post("/login", response_model=TokenResponse)
def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login de usuário com email e senha
    
    Retorna token JWT para autenticação em próximas requisições
    """
    # Encontrar usuário
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")
    
    # Verificar senha
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")
    
    # Verificar se usuário está ativo
    if not user.active:
        raise HTTPException(status_code=403, detail="Usuário desativado")
    
    # Criar token JWT
    access_token = create_access_token(user.id, user.email)
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.from_orm(user)
    )


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Obter detalhes de um usuário"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


@router.get("", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Listar todos os usuários (paginado)
    
    TODO: Adicionar validação de permissão (apenas admin)
    """
    return db.query(User).offset(skip).limit(limit).all()


@router.get("/role/{role}", response_model=list[UserResponse])
def list_users_by_role(
    role: UserRole,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Listar usuários por tipo de role
    
    Tipos: admin, organizer, player
    """
    return db.query(User).filter(User.role == role).offset(skip).limit(limit).all()
