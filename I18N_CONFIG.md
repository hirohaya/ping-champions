# Internationalization (i18n) Configuration

## Overview

Ping Champions now supports multiple languages:
- **Portuguese (BR)** - Português Brasileiro
- **English (US)** - English (United States)

## Frontend (Vue 3 + vue-i18n)

### Setup

The frontend uses `vue-i18n` for client-side translations.

```bash
npm install vue-i18n
```

### File Structure

```
frontend/src/
├── i18n.js              # i18n configuration
├── locales/
│   ├── pt-BR.json       # Portuguese (BR) translations
│   └── en-US.json       # English (US) translations
├── components/
│   └── LanguageSwitcher.vue  # Language selector component
```

### Usage in Components

Use the `$t()` function to translate strings:

```vue
<template>
  <h1>{{ $t('events.title') }}</h1>
  <button>{{ $t('common.save') }}</button>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const message = t('events.eventCreatedSuccess')
</script>
```

### Language Selection

1. The app automatically detects the browser's language preference
2. User can manually select language via `LanguageSwitcher` component
3. Preference is saved to `localStorage` as `locale`

### Adding New Translations

1. Add keys to both `frontend/src/locales/pt-BR.json` and `frontend/src/locales/en-US.json`
2. Use the same key structure in both files
3. Follow the existing key hierarchy (e.g., `events.title`)

### Key Hierarchy Structure

```json
{
  "common": { ... },
  "navigation": { ... },
  "events": { ... },
  "players": { ... },
  "matches": { ... },
  "ranking": { ... },
  "validation": { ... },
  "messages": { ... },
  "settings": { ... }
}
```

## Backend (FastAPI)

### Modules

- `backend/i18n.py` - Localization utilities and message definitions
- `backend/routers/i18n.py` - API endpoints for i18n

### API Endpoints

#### Get Localized Messages

```http
GET /api/i18n/messages
Accept-Language: pt-BR,pt;q=0.9,en;q=0.8
```

Returns all messages for the user's preferred language (based on `Accept-Language` header).

Response:
```json
{
  "locale": "pt-BR",
  "messages": {
    "event_created": "Evento criado com sucesso!",
    ...
  }
}
```

#### Get Available Locales

```http
GET /api/i18n/locales
```

Returns list of supported languages.

Response:
```json
{
  "locales": [
    {"code": "pt-BR", "name": "Português (BR)"},
    {"code": "en-US", "name": "English (US)"}
  ]
}
```

#### Set Locale

```http
POST /api/i18n/set-locale
Content-Type: application/json

{"locale": "pt-BR"}
```

### Using Backend Messages

In your router/endpoint code:

```python
from i18n import Messages, Locale

# Get a message
message = Messages.get("event_created", Locale.PT_BR)

# Or automatically detect from header
from fastapi import Header
from i18n import get_locale_from_header

@router.get("/events")
async def get_events(accept_language: str = Header(None)):
    locale = get_locale_from_header(accept_language)
    success_message = Messages.get("event_created", locale)
    # Use message...
```

### Adding Backend Messages

1. Add new key-value pairs to both locales in `backend/i18n.py` > `Messages._messages`
2. Use consistent naming (e.g., `entity_action` like `event_created`, `player_updated`)
3. Maintain both PT_BR and EN_US entries

Example:
```python
Locale.PT_BR: {
    "new_key": "Mensagem em Português",
    ...
},
Locale.EN_US: {
    "new_key": "Message in English",
    ...
}
```

## Frontend Integration with Backend

### Getting Messages from API

You can optionally fetch messages from the backend API:

```javascript
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

const fetchBackendMessages = async () => {
  const response = await fetch('/api/i18n/messages', {
    headers: {
      'Accept-Language': locale.value
    }
  })
  const data = await response.json()
  return data.messages
}
```

## Best Practices

### Frontend
1. Always define translations in both languages simultaneously
2. Use descriptive key names that indicate context
3. Keep translations in JSON files, not hardcoded in components
4. Test both languages in all UI components

### Backend
1. Use the Messages class for all user-facing text
2. Support Accept-Language header to auto-detect client preference
3. Provide consistent message keys across API responses
4. Document all message keys in this file

### Shared Conventions
- Use lowercase keys with underscores: `event_created`, `player_not_found`
- Group related translations under parent keys: `events.title`, `events.createEvent`
- Keep messages concise and user-friendly
- Avoid HTML/special characters in messages
- Test both languages thoroughly before committing

## Future Enhancements

- [ ] Support additional languages (Spanish, French, etc.)
- [ ] Server-side locale persistence (user preferences in database)
- [ ] Pluralization support for messages
- [ ] Date/time locale formatting
- [ ] Currency formatting if needed
- [ ] Automatic missing translation detection
- [ ] Translation management UI

## Troubleshooting

**Q: Language doesn't change**
- Clear browser cache and localStorage
- Verify `LanguageSwitcher` component is loaded
- Check browser console for errors

**Q: Some strings still in original language**
- Search codebase for hardcoded strings (not using `$t()`)
- Add missing keys to locale JSON files
- Verify key names match exactly

**Q: Backend returns wrong language**
- Check Accept-Language header is being sent
- Verify `get_locale_from_header()` logic
- Check browser language settings

## Files Modified

- `frontend/src/main.js` - Added i18n initialization
- `frontend/src/App.vue` - Added LanguageSwitcher component
- `frontend/src/i18n.js` - NEW - i18n configuration
- `frontend/src/components/LanguageSwitcher.vue` - NEW - Language selector
- `frontend/src/locales/pt-BR.json` - NEW - Portuguese translations
- `frontend/src/locales/en-US.json` - NEW - English translations
- `backend/i18n.py` - NEW - Backend i18n utilities
- `backend/routers/i18n.py` - NEW - i18n API endpoints
- `backend/main.py` - Added i18n router registration

---

**Last Updated**: November 10, 2025
**Status**: Implementation Complete - Ready for Testing
