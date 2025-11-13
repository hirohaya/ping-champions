"""
Membership Router - Endpoints para gerenciar membership (convites, aceitar, sair, suspender)

Endpoints:
  GET /members/{event_id} - Listar membros de um evento
  POST /members - Convidar jogador para evento (criar membership)
  GET /members/{id} - Get detalhes de um membership
  PUT /members/{id}/accept - Aceitar convite
  PUT /members/{id}/leave - Sair voluntariamente
  PUT /members/{id}/suspend - Suspender membro
  PUT /members/{id}/reactivate - Reativar membro suspenso
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Membership, Event, Player, MembershipStatus
from schemas import (
    MembershipCreate,
    MembershipRead,
    MembershipAcceptInvite,
    MembershipLeave,
    MembershipSuspend,
    MembershipReactivate,
)

router = APIRouter(prefix="/members", tags=["members"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{event_id}", response_model=list[MembershipRead])
def list_memberships(
    event_id: int,
    status: str = Query(None, description="Filter by status (convidado, ativo, inativo, suspenso, deletado)"),
    db: Session = Depends(get_db),
):
    """
    Listar membros de um evento, com opção de filtrar por status.
    
    Args:
        event_id: ID do evento
        status: Status opcional para filtrar (ex: 'ativo', 'convidado')
    """
    # Validar se evento existe
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Evento não encontrado")

    # Query base
    query = db.query(Membership).filter(Membership.event_id == event_id)

    # Filtrar por status se fornecido
    if status:
        try:
            status_enum = MembershipStatus(status.lower())
            query = query.filter(Membership.status == status_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Status inválido: {status}")

    memberships = query.all()
    return memberships


@router.post("", response_model=MembershipRead)
def create_membership(
    membership: MembershipCreate,
    db: Session = Depends(get_db),
):
    """
    Criar membership (convidar jogador para evento).
    
    Status inicial: CONVIDADO (pendente de aceitar)
    
    Args:
        membership: MembershipCreate com event_id e player_id
    """
    # Validar evento
    event = db.query(Event).filter(Event.id == membership.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Evento não encontrado")

    # Validar jogador (deve estar no mesmo evento)
    player = db.query(Player).filter(
        Player.id == membership.player_id,
        Player.event_id == membership.event_id
    ).first()
    if not player:
        raise HTTPException(status_code=404, detail="Jogador não encontrado neste evento")

    # Verificar se já existe membership
    existing = db.query(Membership).filter(
        Membership.event_id == membership.event_id,
        Membership.player_id == membership.player_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Jogador já possui membership com status: {existing.status.value}"
        )

    # Criar novo membership
    new_membership = Membership(
        event_id=membership.event_id,
        player_id=membership.player_id,
        status=MembershipStatus.CONVIDADO,
    )
    db.add(new_membership)
    db.commit()
    db.refresh(new_membership)
    return new_membership


@router.get("/{id}", response_model=MembershipRead)
def get_membership(
    id: int,
    db: Session = Depends(get_db),
):
    """Get detalhes de um membership específico"""
    membership = db.query(Membership).filter(Membership.id == id).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Membership não encontrado")
    return membership


@router.put("/{id}/accept", response_model=MembershipRead)
def accept_invite(
    id: int,
    db: Session = Depends(get_db),
):
    """
    Aceitar convite para evento.
    
    Transição: CONVIDADO -> ATIVO
    
    Args:
        id: ID do membership
    """
    membership = db.query(Membership).filter(Membership.id == id).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Membership não encontrado")

    if membership.status != MembershipStatus.CONVIDADO:
        raise HTTPException(
            status_code=400,
            detail=f"Não pode aceitar convite. Status atual: {membership.status.value}"
        )

    # Transição
    membership.accept_invite()
    db.commit()
    db.refresh(membership)
    return membership


@router.put("/{id}/leave", response_model=MembershipRead)
def leave_group(
    id: int,
    db: Session = Depends(get_db),
):
    """
    Sair voluntariamente do evento.
    
    Transição: ATIVO -> INATIVO
    
    Args:
        id: ID do membership
    """
    membership = db.query(Membership).filter(Membership.id == id).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Membership não encontrado")

    if membership.status != MembershipStatus.ATIVO:
        raise HTTPException(
            status_code=400,
            detail=f"Apenas membros ATIVO podem sair. Status atual: {membership.status.value}"
        )

    # Transição
    membership.leave_group()
    db.commit()
    db.refresh(membership)
    return membership


@router.put("/{id}/suspend", response_model=MembershipRead)
def suspend_member(
    id: int,
    suspend_data: MembershipSuspend,
    db: Session = Depends(get_db),
):
    """
    Suspender membro (administrador).
    
    Transição: ATIVO/CONVIDADO -> SUSPENSO
    
    Args:
        id: ID do membership
        suspend_data: Razão da suspensão
    """
    membership = db.query(Membership).filter(Membership.id == id).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Membership não encontrado")

    if membership.status == MembershipStatus.DELETADO:
        raise HTTPException(
            status_code=400,
            detail="Não pode suspender membro deletado"
        )

    # Transição
    membership.suspend_member(suspend_data.motivo_suspensao or "Sem motivo especificado")
    db.commit()
    db.refresh(membership)
    return membership


@router.put("/{id}/reactivate", response_model=MembershipRead)
def reactivate_member(
    id: int,
    db: Session = Depends(get_db),
):
    """
    Reativar membro suspenso.
    
    Transição: SUSPENSO -> ATIVO
    
    Args:
        id: ID do membership
    """
    membership = db.query(Membership).filter(Membership.id == id).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Membership não encontrado")

    if membership.status != MembershipStatus.SUSPENSO:
        raise HTTPException(
            status_code=400,
            detail=f"Apenas membros SUSPENSO podem ser reativados. Status: {membership.status.value}"
        )

    # Transição
    membership.reactivate()
    db.commit()
    db.refresh(membership)
    return membership
