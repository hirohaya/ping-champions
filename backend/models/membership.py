"""
Membership Model - Ciclo de Vida de Membros em Eventos

Estados possíveis:
  - CONVIDADO: Convite enviado, pendente de aceitar
  - ATIVO: Membro ativo, pode jogar
  - INATIVO: Saiu do evento (voluntário)
  - SUSPENSO: Suspenso temporariamente (violação, inatividade)
  - DELETADO: Conta deletada (soft delete, dados preservados)

Timeline:
  - data_entrada: Quando entrou no evento (aceitou convite)
  - data_saida: Quando saiu voluntariamente
  - data_suspensao: Quando foi suspenso
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from database import Base


class MembershipStatus(str, enum.Enum):
    """Estados possíveis de membership"""
    CONVIDADO = "convidado"
    ATIVO = "ativo"
    INATIVO = "inativo"
    SUSPENSO = "suspenso"
    DELETADO = "deletado"


class Membership(Base):
    """
    Representa a relação entre Player e Event (membership)
    
    Atributos:
      - id: ID único
      - event_id: FK para Event
      - player_id: FK para Player
      - status: Estado do membro (CONVIDADO/ATIVO/INATIVO/SUSPENSO/DELETADO)
      - data_entrada: Data de entrada (aceitação do convite)
      - data_saida: Data de saída voluntária
      - data_suspensao: Data de suspensão
      - motivo_suspensao: Razão da suspensão
      - created_at: Data de criação do registro
      - updated_at: Data da última atualização
    """
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Status e timeline
    status = Column(Enum(MembershipStatus), default=MembershipStatus.CONVIDADO, index=True)
    data_entrada = Column(DateTime, nullable=True)  # NULL até aceitar convite
    data_saida = Column(DateTime, nullable=True)    # Preenchido ao sair voluntariamente
    data_suspensao = Column(DateTime, nullable=True)  # Preenchido ao ser suspenso
    motivo_suspensao = Column(String(255), nullable=True)  # Razão da suspensão
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    event = relationship("Event", back_populates="memberships")
    player = relationship("Player", back_populates="memberships")

    def __repr__(self):
        return f"<Membership(event_id={self.event_id}, player_id={self.player_id}, status={self.status})>"

    def accept_invite(self):
        """Transição: CONVIDADO -> ATIVO"""
        if self.status != MembershipStatus.CONVIDADO:
            raise ValueError(f"Não pode aceitar convite com status {self.status}")
        self.status = MembershipStatus.ATIVO
        self.data_entrada = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def leave_group(self):
        """Transição: ATIVO -> INATIVO"""
        if self.status != MembershipStatus.ATIVO:
            raise ValueError(f"Apenas membros ATIVO podem sair (status atual: {self.status})")
        self.status = MembershipStatus.INATIVO
        self.data_saida = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def suspend_member(self, motivo: str = ""):
        """Transição: ATIVO -> SUSPENSO"""
        if self.status == MembershipStatus.DELETADO:
            raise ValueError("Não pode suspender membro deletado")
        self.status = MembershipStatus.SUSPENSO
        self.data_suspensao = datetime.utcnow()
        self.motivo_suspensao = motivo
        self.updated_at = datetime.utcnow()

    def reactivate(self):
        """Transição: SUSPENSO -> ATIVO"""
        if self.status != MembershipStatus.SUSPENSO:
            raise ValueError(f"Apenas membros SUSPENSO podem ser reativados (status: {self.status})")
        self.status = MembershipStatus.ATIVO
        self.data_suspensao = None
        self.motivo_suspensao = None
        self.updated_at = datetime.utcnow()

    def soft_delete(self):
        """Transição: qualquer -> DELETADO (soft delete)"""
        self.status = MembershipStatus.DELETADO
        self.updated_at = datetime.utcnow()

    @property
    def is_active(self) -> bool:
        """Retorna True se membro está ATIVO"""
        return self.status == MembershipStatus.ATIVO

    @property
    def can_play(self) -> bool:
        """Retorna True se membro pode jogar (deve estar ATIVO)"""
        return self.is_active
