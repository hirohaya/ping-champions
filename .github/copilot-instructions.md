# Ping Champions - AI Coding Agent Instructions

This document provides essential context for AI coding agents (GitHub Copilot, Claude, etc.) working on the Ping Champions project. Use this to understand architecture, conventions, and workflows.

## Project Overview

**Ping Champions** is a tournament management system for ping-pong events.

- **Status**: Low complexity, MVP phase with 24 prioritized tasks (see `docs/TASKS.md`)
- **Tech Stack**: FastAPI + Vue 3 + SQLite + SQLAlchemy
- **Setup**: Single unified entry point via `setup.py` (handles backend, frontend, environment)
- **Database**: SQLite with 3 core entities (Events, Players, Matches)

## Coding Philosophy

- **Simplicity**: Prioritize clear, maintainable code over complex optimizations
- **Conventions**: Follow established patterns in existing code (see below)
- **Documentation**: Comment non-obvious logic; refer to this file for architecture/context
- **Virtual Environments**: Always works on and use virtual environments for Python dependencies; isolate frontend with npm
- **README Updates**: Keep `README.md` updated with architecture changes and project progress from tasks
- **Testing**: Always run a complete tests, unit and e2e after making any changes. Write tests for new features and bug fixes; use existing test files as reference
- **Branch Cleaning**: Delete feature branches after merging to main to keep repo tidy
- **Terminal**: always close terminal sessions after use to avoid resource leaks

## Implementation & Testing Workflow

**⚠️ CRITICAL REQUIREMENT**: Every implementation must follow this workflow - No exceptions.

### 1. Project State Before Implementation
- Start with **both backend and frontend running**:
  - Backend: `python run_backend.py` (on `http://127.0.0.1:8000`)
  - Frontend: `npm run dev` in `frontend/` directory (on `http://localhost:5173`)
- Verify both are responding before making code changes

### 2. Development Cycle
1. **Make code changes** (backend, frontend, or both)
2. **Save files** - Vite and uvicorn will auto-reload
3. **Immediately test in browser** using Playwright MCP
4. **Verify changes** before moving to next feature
5. **Repeat** for each component/feature

### 3. Playwright MCP Testing Protocol

**Purpose**: Automated browser testing with real UI interaction

**When to Test**:
- ✅ After every backend endpoint modification
- ✅ After every frontend component change
- ✅ After database schema changes
- ✅ After service layer updates
- ✅ Before committing code to git

**Testing Approach**:
1. Navigate to relevant page: `mcp_microsoft_pla_browser_navigate(url)`
2. Wait for content to load: `mcp_microsoft_pla_browser_wait_for(time)`
3. Take snapshot of page state: `mcp_microsoft_pla_browser_snapshot()`
4. Interact with UI: click, type, select, fill forms
5. Verify results: check alerts, inspect page state, API responses
6. Test edge cases: validation, error states, empty states

**Example Test Flow**:
```
Navigate → Wait → Snapshot (verify page loaded)
→ Click button → Type text → Submit form
→ Check alert message → Verify data in list
→ Refresh page → Verify persistence
```

**Key Playwright Commands**:
- `mcp_microsoft_pla_browser_navigate(url)` - Navigate to page
- `mcp_microsoft_pla_browser_snapshot()` - Get page accessibility snapshot
- `mcp_microsoft_pla_browser_click(element, ref)` - Click element
- `mcp_microsoft_pla_browser_type(element, ref, text)` - Type into field
- `mcp_microsoft_pla_browser_select_option(element, ref, values)` - Select dropdown
- `mcp_microsoft_pla_browser_fill_form(fields)` - Fill multiple fields
- `mcp_microsoft_pla_browser_wait_for(time)` - Wait for time or condition
- `mcp_microsoft_pla_browser_handle_dialog(accept)` - Handle alert/confirm dialogs
- `mcp_microsoft_pla_browser_take_screenshot(filename)` - Take visual screenshot

### 4. Test Coverage Requirements

**Minimum Testing Per Feature**:
- ✅ Happy path (successful operation)
- ✅ Validation failures (invalid input)
- ✅ API error handling (404, 500, etc.)
- ✅ Data persistence (page refresh)
- ✅ Related features (rankings, calculations, etc.)

**For Match Creation** (example):
- Create match with valid data → verify appears in list
- Create match with invalid data → verify error message
- Create match without required field → verify validation alert
- Refresh page → verify match still exists
- Check rankings updated → verify Elo calculations

### 5. Success Criteria
- All Playwright tests pass without errors
- No browser console errors ([ERROR] messages)
- Form validation works as designed
- Data persists after page refresh
- Related calculations/rankings update correctly
- No breaking changes to existing features

### 6. Documentation of Test Results
After testing, document:
- Test scenarios attempted
- Pass/fail status for each scenario
- Any alerts or error messages displayed
- Final state verification (rankings, data, etc.)
- Screenshots of successful UI if complex feature

### 7. Common Testing Mistakes to Avoid
- ❌ Making changes without running backend/frontend
- ❌ Skipping browser testing and only running unit tests
- ❌ Not waiting for async operations (use `mcp_microsoft_pla_browser_wait_for`)
- ❌ Not checking page state after actions (use `mcp_microsoft_pla_browser_snapshot`)
- ❌ Forgetting to test data persistence (page refresh)
- ❌ Not testing validation and error cases
- ❌ Leaving browser in inconsistent state (always navigate fresh)

### 8. Terminal Management
- **Keep servers running**: Background process with `isBackground=true`
- **Check output**: Use `get_terminal_output(id)` to verify no errors
- **Close on completion**: Kill terminals after final testing complete
- **Monitor logs**: Watch for exceptions or warnings in output

## Backend Architecture

### Stack & Dependencies
- **Python**: 3.9+
- **Framework**: FastAPI (async web framework)
- **ORM**: SQLAlchemy with SQLite database
- **Database File**: `backend/pingchampions.db` (auto-created on first run)
- **Entry Point**: `backend/main.py` runs on `http://127.0.0.1:8000`

### Key Files Structure
```
backend/
├── main.py              # FastAPI app, CORS setup, router registration
├── database.py          # SQLAlchemy engine, session factory, Base class
├── schemas.py           # Pydantic request/response models (if using)
├── models/
│   ├── __init__.py      # Imports Event, Player, Match (MUST maintain!)
│   ├── event.py         # Event model: name, date (YYYY-MM-DD), time, active flag
│   ├── player.py        # Player model: event_id FK, name, initial_elo
│   └── match.py         # Match model: event_id FK, p1_id, p2_id, winner_id
└── routers/
    ├── events.py        # POST/GET /events/* endpoints
    ├── players.py       # POST/GET /players/* endpoints
    ├── matches.py       # POST/GET /matches/* endpoints
    └── ranking.py       # GET /ranking/* endpoints
```

### Database Patterns
- **Soft Delete**: Events use `active` boolean flag (visible when `active=True`)
- **Relationships**: SQLAlchemy `relationship()` with `back_populates` and `cascade="all, delete-orphan"`
- **Dates**: Stored as strings in `YYYY-MM-DD` format in Event model (not DateTime columns)
- **Times**: Stored as strings in `HH:MM` format

### API Conventions
- **Prefix**: All routers use prefix (e.g., `/events`, `/players`, `/matches`)
- **Dependency Injection**: Use `Depends(get_db)` for session management
- **Error Handling**: Raise `HTTPException(status_code=404, detail="...")` for not found
- **KNOWN ISSUE - Trailing Slashes**: API has inconsistent trailing slash behavior (documented in `docs/TASKS.md` as T004) - be aware when creating new endpoints

### Models Relationship Map
```
Event (1) ---> (N) Player
  |
  +---> (N) Match
  
Player (1) ---> (N) Match (as player_1)
       (1) ---> (N) Match (as player_2)
```

**CRITICAL**: Always import models through `models/__init__.py`:
```python
# CORRECT:
from models import Event, Player, Match

# WRONG (avoid):
from models.event import Event
```

## Frontend Architecture

### Stack & Dependencies
- **Framework**: Vue 3 (Composition API preferred)
- **Build Tool**: Vite
- **Router**: Vue Router with lazy loading
- **HTTP Client**: Axios (baseURL: `http://localhost:8000`)
- **Development Server**: `npm run dev` (runs on `http://localhost:5173`)

### File Structure
```
frontend/src/
├── App.vue              # Root component
├── main.js              # Vue app setup, router registration
├── router/
│   └── index.js         # Route definitions (lazy-loaded views)
├── components/
│   ├── Breadcrumbs.vue  # Reusable breadcrumb component
│   ├── EventCard.vue    # Event display card
│   └── ...              # Other shared components
├── views/
│   ├── HomeView.vue     # Home page
│   ├── EventsView.vue   # Event list (KNOWN ISSUE: SFC error - T001)
│   ├── EventDetailView.vue  # Nested detail page with child routes
│   ├── PlayersView.vue  # Player list/management
│   ├── MatchesView.vue  # Match list/management
│   ├── RankingView.vue  # Tournament ranking display
│   └── StatusView.vue   # Backend/system status page
└── services/
    ├── api.js           # Axios instance (baseURL preconfigured)
    ├── events.js        # Event API calls
    ├── players.js       # Player API calls
    ├── jogos.js         # Match API calls (note: "jogos" = "games" in Portuguese)
    └── ranking.js       # Ranking API calls
```

### Component Patterns
- **Services Pattern**: All API calls go through `services/*.js` files, not inline in components
- **Route Nesting**: EventDetailView contains nested routes for Players and Matches per event
- **Lazy Loading**: Use dynamic imports in router for code splitting:
  ```javascript
  component: () => import('../views/EventDetailView.vue')
  ```

### CORS Configuration
- Backend CORS allows `http://localhost:5173` (frontend dev server)
- Configured in `backend/main.py`

## Development Workflow

### Project Setup (First-Time Only)
```powershell
python setup.py
```
This script:
1. Creates Python virtual environment in `backend/`
2. Installs backend dependencies (requirements.txt + requirements-dev.txt)
3. Installs frontend dependencies (npm install)
4. Creates `.env` and `.env.local` configuration files
5. Shows next steps for development

**Cross-platform**: Automatically detects Windows/Linux and adjusts paths.

### Running Development Servers

**Backend**:
```powershell
python run_backend.py
# Runs: uvicorn main:app --host 127.0.0.1 --port 8000 --reload
# Accessible at: http://127.0.0.1:8000
# Docs at: http://127.0.0.1:8000/docs (Swagger UI)
```

**Frontend**:
```powershell
cd frontend
npm run dev
# Runs: vite
# Accessible at: http://localhost:5173
```

**Database Reset** (caution - deletes all data):
```powershell
python recreate_db.py
# Drops all tables and recreates fresh schema
```

### Script Purpose Reference
- `setup.py` - Initial project setup (backend, frontend, environment files)
- `run_backend.py` - Quick backend startup with auto-reload
- `recreate_db.py` - Database reset utility

## Known Issues & Conventions

### Critical (P0) Issues
- **T001**: Vue EventsView.vue SFC error - component doesn't render properly
- **T003**: ORM relationship issues - some queries failing (partially fixed in v0.2.0)
- **T004**: API trailing slash inconsistency - `/events` vs `/events/` behavior varies

### High Priority (P1) Issues
- Missing Pydantic schemas in multiple routers (T006, T007, T008)
- Validation errors not properly handled
- Database connection pooling not configured
- No linting or type checking setup

### Code Conventions
- **Date Format**: Use `YYYY-MM-DD` strings in Event model (NOT DateTime columns)
- **Relationships**: Always use `relationship()` with `back_populates` for bidirectional links
- **Soft Deletes**: Use `active` boolean flag instead of hard deletes
- **API Response Format**: Return model instances directly (FastAPI auto-serializes)
- **Unicode Output**: Avoid special characters in terminal output (use ASCII-only: [OK], [ERROR], [WARNING])

### File Naming
- Vue components: `PascalCase.vue` (e.g., `EventCard.vue`)
- JavaScript services: `camelCase.js` (e.g., `api.js`, `events.js`)
- Python modules: `snake_case.py` (e.g., `database.py`, `event.py`)

## Testing

### Test Files
- `test_complete.py` - Full integration test suite
- `test_e2e.py` - End-to-end tests
- `backend/pytest.ini` - Pytest configuration

### Running Tests
```powershell
cd backend
pytest
```

## Common Tasks

### Add a New Endpoint
1. Create schema in `backend/routers/{feature}.py`:
   ```python
   from pydantic import BaseModel
   class ItemCreate(BaseModel):
       name: str
   ```
2. Add route handler:
   ```python
   @router.post("/create")
   def create_item(item: ItemCreate, db: Session = Depends(get_db)):
       # implementation
   ```
3. Register router in `backend/main.py` if new file
4. Test via Swagger UI at `http://127.0.0.1:8000/docs`

### Add a New Vue Component
1. Create component file: `frontend/src/components/NewComponent.vue`
2. Use it in views or other components:
   ```vue
   <script setup>
   import NewComponent from '@/components/NewComponent.vue'
   </script>
   <template>
     <NewComponent />
   </template>
   ```

### Query a Model with Relationships
```python
# Bad: Separate queries
event = db.query(Event).filter(Event.id == 1).first()
players = db.query(Player).filter(Player.event_id == 1).all()

# Good: Use relationship (eager loading if needed)
event = db.query(Event).filter(Event.id == 1).first()
players = event.players  # Access via relationship
```

## Environment Variables

### `.env` (Backend)
```
DATABASE_URL=sqlite:///pingchampions.db
BACKEND_PORT=8000
```

### `.env.local` (Frontend)
```
VITE_API_URL=http://localhost:8000
```

Both files created automatically by `setup.py`.

## Architecture Decision Log

### Why Single `setup.py` Instead of Individual Scripts?
- **Unified Experience**: One command to set up entire project
- **Cross-Platform**: Handles Windows/Linux/macOS paths automatically
- **Consistency**: All developers run same setup process
- **Error Handling**: Centralized logging and error reporting
- **Maintainability**: Single source of truth for setup logic

### Why Soft Delete Instead of Hard Delete?
- **Data Preservation**: Audit trail of all events
- **Recovery**: Mistakes are reversible
- **Reporting**: Historical data remains queryable

### Why String Dates in Event Model?
- **Simplicity**: Frontend sends `YYYY-MM-DD` strings, no parsing needed
- **Format Consistency**: All events use same format
- **Note**: This is noted as a potential future refactor (use proper DateTime columns)

## Roadmap References

See `docs/TASKS.md` for 24 prioritized tasks organized by sprint:
- **Sprint 1**: Fix bugs (T001-T005, focus on SFC error and trailing slashes)
- **Sprint 2**: Add validation (T006-T010, Pydantic schemas)
- **Sprint 3**: Setup linting & testing (T011-T015)
- **Sprint 4**: Complete documentation (T016-T024)

## Quick Reference Commands

| Task | Command |
|------|---------|
| Full project setup | `python setup.py` |
| Start backend | `python run_backend.py` |
| Start frontend | `cd frontend; npm run dev` |
| Reset database | `python recreate_db.py` |
| Run tests | `cd backend; pytest` |
| View API docs | Navigate to `http://127.0.0.1:8000/docs` |
| View app | Navigate to `http://localhost:5173` |

## Asking for Clarification

When in doubt about project structure or conventions:
1. Check this file first (answers 90% of setup/workflow questions)
2. Consult `README.md` for high-level architecture
3. Review `docs/TASKS.md` for known issues and priorities
4. Examine existing code in routers/ or views/ for patterns
5. Check `backend/pytest.ini` for test configuration

## Contact & Documentation

- **Project README**: `README.md` (architecture overview, task list reference)
- **Task List**: `docs/TASKS.md` (24 prioritized tasks with descriptions)
- **Architecture Details**: See README sections on Backend/Frontend structure
- **Code Comments**: Inline comments in models and routers explain business logic

---

**Last Updated**: Generated from codebase analysis
**Python Version**: 3.9+
**Node Version**: 16.x+ (verified with `node -v`)
**Database**: SQLite (file-based, auto-created)
