"""
i18n Database Models - Translation Storage

This model stores translations in a database for dynamic updates
without rebuilding the application.

Features:
- Support for multiple locales
- Namespaced message organization
- Versioning for rollback
- Soft delete for audit trail
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, UniqueConstraint
from database import Base


class TranslationMessage(Base):
    """
    Translation message storage
    
    Allows managing translations at runtime
    Supports hot updates without application restart
    """
    __tablename__ = "translation_messages"
    
    id = Column(Integer, primary_key=True)
    locale = Column(String(10), nullable=False, index=True)  # e.g., 'pt-BR', 'en-US'
    namespace = Column(String(50), nullable=False, index=True)  # e.g., 'events', 'players'
    key = Column(String(100), nullable=False, index=True)  # e.g., 'title', 'createSuccess'
    value = Column(Text, nullable=False)  # The actual translation
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = Column(Integer, default=1)  # For tracking changes
    active = Column(Boolean, default=True)  # Soft delete / deactivate
    
    # Context metadata
    note = Column(Text, nullable=True)  # Translator notes
    context = Column(String(255), nullable=True)  # Context for translation
    
    # Unique constraint: only one active version per message
    __table_args__ = (
        UniqueConstraint('locale', 'namespace', 'key', 'version', name='unique_translation_version'),
    )
    
    def __repr__(self):
        return f'<TranslationMessage {self.locale}/{self.namespace}/{self.key}>'


class TranslationAudit(Base):
    """
    Audit trail for translation changes
    
    Tracks all modifications for compliance and rollback
    """
    __tablename__ = "translation_audits"
    
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, nullable=False)  # Reference to TranslationMessage
    
    # Change tracking
    previous_value = Column(Text, nullable=True)  # What changed from
    new_value = Column(Text, nullable=True)  # What changed to
    change_type = Column(String(20), nullable=False)  # 'create', 'update', 'delete'
    
    # Metadata
    changed_by = Column(String(100), nullable=True)  # User who made change
    changed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    reason = Column(String(255), nullable=True)  # Why was it changed
    
    def __repr__(self):
        return f'<TranslationAudit {self.change_type} on {self.changed_at}>'


class LocaleConfig(Base):
    """
    Configuration per locale
    
    Stores locale-specific settings and metadata
    """
    __tablename__ = "locale_configs"
    
    id = Column(Integer, primary_key=True)
    locale = Column(String(10), unique=True, nullable=False)  # e.g., 'pt-BR'
    name = Column(String(50), nullable=False)  # e.g., 'Português (Brasil)'
    
    # Settings
    active = Column(Boolean, default=True)  # Enable/disable locale
    default_locale = Column(Boolean, default=False)  # Fallback locale
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    message_count = Column(Integer, default=0)  # Cache for optimization
    
    def __repr__(self):
        return f'<LocaleConfig {self.locale}>'


# Add these imports to models/__init__.py:
# from models.translation import TranslationMessage, TranslationAudit, LocaleConfig
