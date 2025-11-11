"""
Internationalization (i18n) module for FastAPI backend.
Supports Portuguese (BR) and English (US) messages.
"""

from enum import Enum
from typing import Dict, Optional

class Locale(str, Enum):
    """Supported locales"""
    PT_BR = "pt-BR"
    EN_US = "en-US"

class Messages:
    """Localized message translations"""
    
    _messages: Dict[Locale, Dict[str, str]] = {
        Locale.PT_BR: {
            # Common
            "success": "Sucesso",
            "error": "Erro",
            "not_found": "Não encontrado",
            "validation_error": "Erro de validação",
            
            # Events
            "event_created": "Evento criado com sucesso!",
            "event_updated": "Evento atualizado com sucesso!",
            "event_deleted": "Evento deletado com sucesso!",
            "event_not_found": "Evento não encontrado",
            "invalid_date": "Data inválida. Use formato YYYY-MM-DD",
            "invalid_time": "Hora inválida. Use formato HH:MM",
            "event_name_required": "Nome do evento é obrigatório",
            
            # Players
            "player_registered": "Jogador registrado com sucesso!",
            "player_updated": "Jogador atualizado com sucesso!",
            "player_deleted": "Jogador deletado com sucesso!",
            "player_not_found": "Jogador não encontrado",
            "player_name_required": "Nome do jogador é obrigatório",
            "player_already_in_event": "Jogador já está registrado neste evento",
            
            # Matches
            "match_created": "Partida criada com sucesso!",
            "match_updated": "Partida atualizada com sucesso!",
            "match_deleted": "Partida deletada com sucesso!",
            "match_not_found": "Partida não encontrada",
            "match_not_finished": "Partida ainda não foi finalizada",
            "same_player_error": "Selecione jogadores diferentes",
            "invalid_best_of": "Best Of deve ser um número ímpar (1, 3, 5, etc)",
            "invalid_winner": "Vencedor inválido",
            "set_counts_required": "Número de sets ganhos é obrigatório",
            
            # Ranking
            "ranking_calculated": "Ranking calculado com sucesso!",
            "ranking_not_available": "Ranking não disponível para este evento",
        },
        Locale.EN_US: {
            # Common
            "success": "Success",
            "error": "Error",
            "not_found": "Not found",
            "validation_error": "Validation error",
            
            # Events
            "event_created": "Event created successfully!",
            "event_updated": "Event updated successfully!",
            "event_deleted": "Event deleted successfully!",
            "event_not_found": "Event not found",
            "invalid_date": "Invalid date. Use YYYY-MM-DD format",
            "invalid_time": "Invalid time. Use HH:MM format",
            "event_name_required": "Event name is required",
            
            # Players
            "player_registered": "Player registered successfully!",
            "player_updated": "Player updated successfully!",
            "player_deleted": "Player deleted successfully!",
            "player_not_found": "Player not found",
            "player_name_required": "Player name is required",
            "player_already_in_event": "Player is already registered in this event",
            
            # Matches
            "match_created": "Match created successfully!",
            "match_updated": "Match updated successfully!",
            "match_deleted": "Match deleted successfully!",
            "match_not_found": "Match not found",
            "match_not_finished": "Match is not yet finished",
            "same_player_error": "Select different players",
            "invalid_best_of": "Best Of must be an odd number (1, 3, 5, etc)",
            "invalid_winner": "Invalid winner",
            "set_counts_required": "Number of sets won is required",
            
            # Ranking
            "ranking_calculated": "Ranking calculated successfully!",
            "ranking_not_available": "Ranking not available for this event",
        }
    }
    
    @classmethod
    def get(cls, key: str, locale: Locale = Locale.EN_US) -> str:
        """Get translated message for given key and locale"""
        return cls._messages.get(locale, {}).get(key, key)
    
    @classmethod
    def get_all(cls, locale: Locale = Locale.EN_US) -> Dict[str, str]:
        """Get all messages for a locale"""
        return cls._messages.get(locale, {})

def get_locale_from_header(accept_language: Optional[str] = None) -> Locale:
    """Extract locale from Accept-Language header"""
    if not accept_language:
        return Locale.EN_US
    
    # Parse Accept-Language header
    # Format: "pt-BR,pt;q=0.9,en;q=0.8"
    languages = accept_language.lower().split(',')
    for lang in languages:
        lang = lang.split(';')[0].strip()
        if lang.startswith('pt'):
            return Locale.PT_BR
        if lang.startswith('en'):
            return Locale.EN_US
    
    return Locale.EN_US
