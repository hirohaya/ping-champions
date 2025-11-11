"""Router for internationalization endpoints"""

from fastapi import APIRouter, Header, Optional
from i18n import Messages, Locale, get_locale_from_header

router = APIRouter(prefix="/api/i18n", tags=["i18n"])

@router.get("/messages")
async def get_localized_messages(
    accept_language: Optional[str] = Header(None)
) -> dict:
    """
    Get all localized messages for the client's preferred language.
    
    The language preference is determined by:
    1. Accept-Language header (if provided)
    2. Default to English (US)
    """
    locale = get_locale_from_header(accept_language)
    messages = Messages.get_all(locale)
    
    return {
        "locale": locale.value,
        "messages": messages
    }

@router.get("/locales")
async def get_available_locales() -> dict:
    """Get list of available locales"""
    return {
        "locales": [
            {"code": "pt-BR", "name": "Português (BR)"},
            {"code": "en-US", "name": "English (US)"}
        ]
    }

@router.post("/set-locale")
async def set_locale(body: dict) -> dict:
    """Set preferred locale for the session"""
    locale = body.get("locale", "en-US")
    
    # Validate locale
    try:
        Locale(locale)
    except ValueError:
        return {
            "success": False,
            "error": f"Invalid locale: {locale}"
        }
    
    return {
        "success": True,
        "locale": locale
    }
