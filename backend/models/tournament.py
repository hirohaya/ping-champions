"""
Tournament Model - Sprint 3

Representa um torneio com diferentes formatos:
- SINGLE_ELIMINATION: Eliminação simples (best-of-1 ou best-of-3)
- SWISS: Pairing automático com suíço sistema
- GROUP_KNOCKOUT: Fase de grupos + fase eliminatória
- ROUND_ROBIN: Todos jogam contra todos

Integrado com Membership para validar participantes ATIVO.
"""

from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum as SQLEnum, ForeignKey, Boolean, JSON, DateTime
from sqlalchemy.orm import relationship
from database import Base


class TournamentType(str, Enum):
    """Tipos de torneio disponíveis"""
    SINGLE_ELIMINATION = "SINGLE_ELIMINATION"
    SWISS = "SWISS"
    GROUP_KNOCKOUT = "GROUP_KNOCKOUT"
    ROUND_ROBIN = "ROUND_ROBIN"


class TournamentStatus(str, Enum):
    """Estados de um torneio"""
    CREATED = "CREATED"           # Criado, aguardando início
    STARTING = "STARTING"         # Em processo de inicialização
    IN_PROGRESS = "IN_PROGRESS"   # Rodadas em andamento
    FINISHED = "FINISHED"         # Concluído
    CANCELLED = "CANCELLED"       # Cancelado


class Tournament(Base):
    """
    Modelo de Torneio
    
    Atributos:
        id: ID único
        event_id: Referência ao Event
        name: Nome do torneio (ex: "Copa Novembro 2025")
        tournament_type: Tipo (SINGLE_ELIMINATION, SWISS, GROUP_KNOCKOUT, ROUND_ROBIN)
        status: Estado atual (CREATED, IN_PROGRESS, FINISHED, CANCELLED)
        
        # Configurações gerais
        created_at: Data de criação
        started_at: Data de início
        finished_at: Data de conclusão
        max_participants: Número máximo de participantes (None = ilimitado)
        
        # Configurações específicas por tipo
        best_of: 1, 3, 5 para SINGLE_ELIMINATION (rodadas)
        num_groups: Para GROUP_KNOCKOUT (ex: 2 grupos)
        swiss_rounds: Para SWISS (número de rodadas)
        allow_draws: Se empates são permitidos (ROUND_ROBIN)
        
        # Estado do torneio
        current_round: Rodada atual
        bracket: JSON com estrutura do bracket (atualizado conforme avança)
        participants_ids: Lista de IDs de jogadores participando
        
        # Relacionamentos
        event: Relacionamento com Event
        matches: Todos os matches do torneio
    """
    
    __tablename__ = "tournaments"
    
    # Chave primária
    id = Column(Integer, primary_key=True, index=True)
    
    # Relacionamento com Event
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    event = relationship("Event", back_populates="tournaments")
    
    # Informações básicas
    name = Column(String(255), nullable=False)
    tournament_type = Column(SQLEnum(TournamentType), nullable=False)
    status = Column(SQLEnum(TournamentStatus), default=TournamentStatus.CREATED, nullable=False)
    
    # Datas
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    
    # Limites
    max_participants = Column(Integer, nullable=True)  # None = ilimitado
    
    # Configurações por tipo
    best_of = Column(Integer, default=1, nullable=False)  # SINGLE_ELIMINATION: 1, 3, 5
    num_groups = Column(Integer, default=2, nullable=False)  # GROUP_KNOCKOUT: 2, 4, etc
    swiss_rounds = Column(Integer, default=3, nullable=False)  # SWISS: número de rodadas
    allow_draws = Column(Boolean, default=False, nullable=False)  # ROUND_ROBIN
    
    # Estado do torneio
    current_round = Column(Integer, default=0, nullable=False)
    bracket = Column(JSON, nullable=True)  # Estrutura do bracket atualizada
    participants_ids = Column(JSON, default=[], nullable=False)  # Lista de player_ids
    
    def __repr__(self):
        return (f"<Tournament(id={self.id}, name='{self.name}', "
                f"type={self.tournament_type}, status={self.status})>")
    
    # ====== PROPRIEDADES ======
    
    @property
    def is_active(self) -> bool:
        """Retorna True se o torneio está em andamento"""
        return self.status == TournamentStatus.IN_PROGRESS
    
    @property
    def participant_count(self) -> int:
        """Retorna número atual de participantes"""
        return len(self.participants_ids) if self.participants_ids else 0
    
    @property
    def is_full(self) -> bool:
        """Retorna True se atingiu limite de participantes"""
        if self.max_participants is None:
            return False
        return self.participant_count >= self.max_participants
    
    @property
    def can_start(self) -> bool:
        """Retorna True se pode começar (precisa de participantes)"""
        if self.status != TournamentStatus.CREATED:
            return False
        # Mínimo de participantes depende do tipo
        min_participants = {
            TournamentType.SINGLE_ELIMINATION: 2,
            TournamentType.SWISS: 3,
            TournamentType.GROUP_KNOCKOUT: 4,
            TournamentType.ROUND_ROBIN: 2,
        }
        return self.participant_count >= min_participants.get(self.tournament_type, 2)
    
    # ====== MÉTODOS DE PARTICIPANTE ======
    
    def add_participant(self, player_id: int) -> bool:
        """Adiciona um jogador ao torneio. Retorna True se sucesso."""
        if self.is_full:
            return False
        if player_id in self.participants_ids:
            return False  # Já está participando
        
        self.participants_ids.append(player_id)
        return True
    
    def remove_participant(self, player_id: int) -> bool:
        """Remove um jogador do torneio. Retorna True se sucesso."""
        if player_id not in self.participants_ids:
            return False
        
        self.participants_ids.remove(player_id)
        return True
    
    def has_participant(self, player_id: int) -> bool:
        """Retorna True se o jogador está participando"""
        return player_id in self.participants_ids
    
    # ====== MÉTODOS DE ESTADO ======
    
    def start(self) -> bool:
        """Inicia o torneio. Retorna True se sucesso."""
        if not self.can_start:
            return False
        
        self.status = TournamentStatus.STARTING
        self.started_at = datetime.utcnow()
        self.current_round = 1
        
        return True
    
    def advance_round(self) -> bool:
        """Avança para a próxima rodada. Retorna True se sucesso."""
        if self.status != TournamentStatus.IN_PROGRESS:
            return False
        
        # Validar se todas as partidas da rodada atual foram jogadas
        # (será implementado quando integrar com Match)
        
        self.current_round += 1
        return True
    
    def finish(self) -> bool:
        """Finaliza o torneio. Retorna True se sucesso."""
        if self.status not in [TournamentStatus.IN_PROGRESS, TournamentStatus.STARTING]:
            return False
        
        self.status = TournamentStatus.FINISHED
        self.finished_at = datetime.utcnow()
        
        return True
    
    def cancel(self) -> bool:
        """Cancela o torneio. Retorna True se sucesso."""
        if self.status == TournamentStatus.FINISHED:
            return False  # Não pode cancelar torneio já finalizado
        
        self.status = TournamentStatus.CANCELLED
        return True
