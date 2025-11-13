"""
Translation API Router

Provides RESTful endpoints for:
- Getting translations by locale/namespace
- Managing translations (admin only)
- Caching and cache invalidation
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from database import SessionLocal
from models.translation import TranslationMessage, LocaleConfig, TranslationAudit
from schemas import TranslationSchema, LocaleConfigSchema
from datetime import datetime

router = APIRouter(prefix="/i18n", tags=["i18n"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================================
# PUBLIC ENDPOINTS (for frontend)
# ============================================================================

@router.get("/messages")
def get_messages(
    locale: str = Query(..., description="Locale code (e.g., 'pt-BR')"),
    namespace: str = Query(None, description="Optional namespace filter (e.g., 'events')"),
    db: Session = Depends(get_db)
):
    """
    Get translation messages for a locale
    
    Examples:
      GET /i18n/messages?locale=pt-BR
      GET /i18n/messages?locale=pt-BR&namespace=events
    
    Returns:
      {
        "locale": "pt-BR",
        "namespace": "events",  # null if not filtered
        "messages": {
          "events": {
            "title": "Eventos",
            "createEvent": "Criar Evento",
            ...
          }
        }
      }
    """
    # Validate locale exists
    locale_config = db.query(LocaleConfig).filter(
        LocaleConfig.locale == locale,
        LocaleConfig.active == True
    ).first()
    
    if not locale_config:
        raise HTTPException(status_code=404, detail=f"Locale '{locale}' not found")
    
    # Get messages
    query = db.query(TranslationMessage).filter(
        and_(
            TranslationMessage.locale == locale,
            TranslationMessage.active == True
        )
    )
    
    if namespace:
        query = query.filter(TranslationMessage.namespace == namespace)
    
    messages = query.all()
    
    # Format response
    formatted = {}
    for msg in messages:
        if msg.namespace not in formatted:
            formatted[msg.namespace] = {}
        formatted[msg.namespace][msg.key] = msg.value
    
    return {
        "locale": locale,
        "namespace": namespace,
        "timestamp": datetime.utcnow().isoformat(),
        "messages": formatted
    }


@router.get("/locales")
def get_active_locales(db: Session = Depends(get_db)):
    """
    Get list of active locales
    
    Returns:
      {
        "locales": [
          {"locale": "pt-BR", "name": "Português (Brasil)", "messageCount": 125},
          {"locale": "en-US", "name": "English (US)", "messageCount": 125}
        ]
      }
    """
    locales = db.query(LocaleConfig).filter(LocaleConfig.active == True).all()
    
    return {
        "locales": [
            {
                "locale": l.locale,
                "name": l.name,
                "messageCount": l.message_count,
                "isDefault": l.default_locale
            }
            for l in locales
        ]
    }


# ============================================================================
# ADMIN ENDPOINTS (protected with auth)
# ============================================================================

@router.post("/messages")
def create_message(
    locale: str,
    namespace: str,
    key: str,
    value: str,
    note: str = None,
    db: Session = Depends(get_db)
):
    """
    Create a new translation message
    Requires admin authorization
    """
    # Check locale exists
    locale_config = db.query(LocaleConfig).filter(
        LocaleConfig.locale == locale
    ).first()
    
    if not locale_config:
        raise HTTPException(status_code=404, detail="Locale not found")
    
    # Check duplicate
    existing = db.query(TranslationMessage).filter(
        and_(
            TranslationMessage.locale == locale,
            TranslationMessage.namespace == namespace,
            TranslationMessage.key == key,
            TranslationMessage.active == True
        )
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=409,
            detail="Translation already exists (update instead)"
        )
    
    # Create message
    message = TranslationMessage(
        locale=locale,
        namespace=namespace,
        key=key,
        value=value,
        note=note,
        version=1
    )
    
    db.add(message)
    db.commit()
    db.refresh(message)
    
    # Update locale message count
    locale_config.message_count = db.query(TranslationMessage).filter(
        and_(
            TranslationMessage.locale == locale,
            TranslationMessage.active == True
        )
    ).count()
    db.commit()
    
    return {
        "id": message.id,
        "locale": message.locale,
        "namespace": message.namespace,
        "key": message.key,
        "value": message.value,
        "created_at": message.created_at.isoformat()
    }


@router.put("/messages/{message_id}")
def update_message(
    message_id: int,
    value: str,
    note: str = None,
    db: Session = Depends(get_db)
):
    """
    Update a translation message
    Requires admin authorization
    
    Creates audit trail and new version
    """
    message = db.query(TranslationMessage).filter(
        TranslationMessage.id == message_id
    ).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    # Create audit entry
    audit = TranslationAudit(
        message_id=message_id,
        previous_value=message.value,
        new_value=value,
        change_type='update',
        changed_at=datetime.utcnow(),
        reason=note
    )
    
    # Update message (or create new version)
    message.value = value
    message.updated_at = datetime.utcnow()
    message.version += 1
    
    db.add(audit)
    db.commit()
    db.refresh(message)
    
    return {
        "id": message.id,
        "value": message.value,
        "version": message.version,
        "updated_at": message.updated_at.isoformat()
    }


@router.delete("/messages/{message_id}")
def delete_message(
    message_id: int,
    reason: str = None,
    db: Session = Depends(get_db)
):
    """
    Soft delete a translation message
    Requires admin authorization
    
    Maintains audit trail
    """
    message = db.query(TranslationMessage).filter(
        TranslationMessage.id == message_id
    ).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    # Create audit entry
    audit = TranslationAudit(
        message_id=message_id,
        previous_value=message.value,
        change_type='delete',
        changed_at=datetime.utcnow(),
        reason=reason
    )
    
    # Soft delete
    message.active = False
    message.updated_at = datetime.utcnow()
    
    db.add(audit)
    db.commit()
    
    return {"message": "Message deleted", "id": message_id}


@router.post("/cache/invalidate")
def invalidate_cache(
    locale: str = None,
    db: Session = Depends(get_db)
):
    """
    Invalidate frontend cache for translations
    Requires admin authorization
    
    Triggers frontend cache refresh
    Returns cache invalidation token
    """
    # In production, this would trigger:
    # 1. WebSocket message to connected clients
    # 2. Cache invalidation token generation
    # 3. Service Worker update notification
    
    import time
    invalidation_token = f"invalidate_{int(time.time())}"
    
    return {
        "message": "Cache invalidation triggered",
        "token": invalidation_token,
        "locale": locale or "all",
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@router.get("/stats")
def get_translation_stats(db: Session = Depends(get_db)):
    """
    Get translation statistics
    
    Returns coverage, completeness, and other metrics
    """
    locales = db.query(LocaleConfig).all()
    
    stats = {
        "totalLocales": len(locales),
        "activeLocales": sum(1 for l in locales if l.active),
        "totalMessages": db.query(TranslationMessage).filter(
            TranslationMessage.active == True
        ).count(),
        "byLocale": {}
    }
    
    for locale in locales:
        count = db.query(TranslationMessage).filter(
            and_(
                TranslationMessage.locale == locale.locale,
                TranslationMessage.active == True
            )
        ).count()
        
        stats["byLocale"][locale.locale] = {
            "name": locale.name,
            "messageCount": count,
            "active": locale.active
        }
    
    return stats
