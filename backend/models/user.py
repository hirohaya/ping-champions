"""
User Model - Sistema de Usuários com RBAC

Tipos de usuários (Role):
  - admin: Administrador do sistema (acesso total)
  - organizer: Organizador de eventos (pode criar eventos e gerenciar jogadores)
  - player: Jogador (pode participar de eventos e torneios)

Notas:
  - Organizadores são também jogadores (têm acesso aos recursos de jogador)
  - Cada usuário tem uma conta de login única
  - Senhas são hasheadas com bcrypt
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
import enum

from database import Base


class UserRole(str, enum.Enum):
    """Papéis/tipos de usuários no sistema"""
    ADMIN = "admin"
    ORGANIZER = "organizer"
    PLAYER = "player"


class User(Base):
    """
    Representa um usuário no sistema
    
    Atributos:
      - id: ID único
      - email: Email único para login
      - password_hash: Senha hasheada com bcrypt
      - name: Nome completo
      - role: Tipo de usuário (admin/organizer/player)
      - active: Indica se usuário está ativo
      - created_at: Data de criação da conta
      - updated_at: Data da última atualização
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.PLAYER, nullable=False, index=True)
    active = Column(Boolean, default=True, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"

    @property
    def is_admin(self) -> bool:
        """Retorna True se usuário é admin"""
        return self.role == UserRole.ADMIN

    @property
    def is_organizer(self) -> bool:
        """Retorna True se usuário é organizador"""
        return self.role == UserRole.ORGANIZER

    @property
    def is_player(self) -> bool:
        """Retorna True se usuário é jogador"""
        return self.role == UserRole.PLAYER

    @property
    def is_admin_or_organizer(self) -> bool:
        """Retorna True se é admin ou organizador"""
        return self.role in [UserRole.ADMIN, UserRole.ORGANIZER]
