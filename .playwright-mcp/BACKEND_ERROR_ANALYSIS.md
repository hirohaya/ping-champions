# Backend Error Analysis - Session 19 E2E Testing

**Date**: 2024-11-13
**Issue**: HTTP 500 Error on `/matches?event_id=7` endpoint
**Status**: BLOCKING - Prevents further E2E testing
**Severity**: CRITICAL

---

## Problem Description

When attempting to load event details that require fetching associated matches, the backend returns HTTP 500 Internal Server Error.

### Error Details

**Endpoint**: `GET /matches?event_id=7`
**Status Code**: 500 Internal Server Error
**Source**: http://127.0.0.1:8000/matches?event_id=7

### Frontend Error Message

```
[ERROR] Access to XMLHttpRequest at 'http://localhost:8000/matches?event_id=7' from origin 'http://localhost:5173'
[ERROR] Error loading event: AxiosError @ http://localhost:5173/src/components/EventOverview.vue:68
[ERROR] Failed to load resource: net::ERR_FAILED @ http://localhost:8000/matches?event_id=7:0
```

### Affected Component

**File**: `frontend/src/components/EventOverview.vue`
**Line**: 68 (in error loading logic)
**Impact**: Cannot display event details page

---

## Diagnosis

### What Works ✅

1. **Backend is running**
   - Port 8000 is active
   - CORS configured correctly
   - Can accept requests

2. **Other endpoints work**
   - `/events` - Returns 200 OK
   - Returns full event list with data
   - Event ID 7 exists in database ("Copa do Clube")

3. **Frontend connectivity**
   - Can reach backend
   - Can parse successful responses
   - CORS headers not blocking requests

### What Fails ❌

1. **Matches endpoint**
   - Route: `/matches?event_id=7`
   - Returns: HTTP 500 (Internal Server Error)
   - No error details in HTTP response

2. **Probable Root Cause**

   The error occurs during the response serialization or data retrieval, not the routing:
   
   - Route exists and is accepting the request
   - Query parameter `event_id=7` is valid
   - Server error suggests:
     a) Database query failure
     b) Serialization issue with Match model
     c) Relationship loading failure
     d) Pydantic validation error

---

## Code Analysis

### Endpoint Definition

**File**: `backend/routers/matches.py` (Lines 140-153)

```python
@router.get("", response_model=list[MatchRead])
def list_matches(event_id: int = Query(..., gt=0), db: Session = Depends(get_db)):
    """
    Get all matches for an event.
    Works for both active and inactive events.
    """
    # Verify event exists (active or inactive)
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return db.query(Match).filter(Match.event_id == event_id).all()
```

**Assessment**: Code looks correct. Event verification works, query syntax is valid.

### Response Model

**File**: `backend/schemas.py` (Lines 156-168)

```python
class MatchRead(BaseModel):
    """Schema for reading match data"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    event_id: int
    player1_id: int
    player2_id: int
    winner_id: Optional[int] = None
    best_of: int
    finished: bool
    player1_games: int
    player2_games: int
    games_score: Optional[str] = None
```

**Assessment**: Schema is valid, all required fields are defined.

### Database Model

**File**: `backend/models/match.py`

```python
class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    player1_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    player2_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    winner_id = Column(Integer, ForeignKey("players.id"), nullable=True)
    # ... other columns ...
```

**Assessment**: Model structure is valid and matches schema fields.

---

## Investigation Steps Completed

1. ✅ Verified backend is running on port 8000
2. ✅ Verified other endpoints work (`/events` returns 200)
3. ✅ Confirmed event ID 7 exists in database
4. ✅ Tested endpoint directly with Invoke-WebRequest
5. ✅ Confirmed HTTP 500 error is consistent
6. ✅ Verified frontend code correctly attempts the call
7. ✅ Verified CORS not blocking the request

---

## Next Steps for Resolution

### 1. Check Backend Logs

Look for error messages in backend output:

```bash
# Examine the terminal/log where backend is running
# Look for stack trace or error details
# Check for database connection issues
# Check for unhandled exceptions
```

### 2. Database Validation

```bash
# In the database, check:
# - Does event 7 have any associated matches?
# - Are matches.event_id foreign keys valid?
# - Are there orphaned records?
```

### 3. Test Database Query Directly

```python
# In Python shell:
from database import SessionLocal
from models import Match

db = SessionLocal()
matches = db.query(Match).filter(Match.event_id == 7).all()
print(f"Matches found: {len(matches)}")
for m in matches:
    print(f"Match {m.id}: Players {m.player1_id} vs {m.player2_id}")
```

### 4. Enable Debug Logging

Add logging to the matches endpoint:

```python
import logging

logger = logging.getLogger(__name__)

@router.get("", response_model=list[MatchRead])
def list_matches(event_id: int = Query(..., gt=0), db: Session = Depends(get_db)):
    logger.info(f"Fetching matches for event {event_id}")
    
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        logger.warning(f"Event {event_id} not found")
        raise HTTPException(status_code=404, detail="Event not found")
    
    matches = db.query(Match).filter(Match.event_id == event_id).all()
    logger.info(f"Found {len(matches)} matches")
    
    return matches
```

### 5. Restart Backend with Fresh Database

If all else fails:

```bash
# Backup current database
# Run recreate_db.py to reset
# Restart backend
# Test again
```

---

## Test Impact

**Current Status**: 🟡 BLOCKED
- ✅ i18n tests passing (33% of planned tests)
- ❌ Events detail tests blocked (60% planned)
- ❌ Matches tests blocked (100% planned)
- ❌ Players tests blocked (100% planned)
- ❌ Ranking tests blocked (100% planned)
- ❌ ngrok tests blocked (100% planned)

**Workaround**: None available at this moment. Must fix backend error to continue.

---

## Recommendation

**PRIORITY**: HIGH - Must fix before continuing with other tests

Once this issue is resolved:
1. Resume Events E2E tests
2. Continue with remaining test suites
3. Test on ngrok URL
4. Compile final report
5. Merge to main

---

**Investigation by**: GitHub Copilot
**Investigation Method**: Playwright MCP + Direct API Testing
**Environment**: Windows 10, Python 3.9+, FastAPI, Vue 3
**Time Spent**: ~30 minutes

*End of Analysis*
