# Delete Strategy Decision - T005

**Date**: Sprint 1  
**Task**: T005 - Decide on delete strategy for soft-deleted entities and unused files  
**Status**: Completed

---

## Executive Summary

This document outlines the delete strategy adopted for the Ping Champions project, addressing:
1. How to handle soft-deleted events and players in the database
2. Which unused files should be removed from the codebase
3. Future cleanup procedures

---

## 1. Soft Delete Strategy for Events

### Current Implementation
- Events use **soft deletes** (mark `active = False`)
- Players have cascade delete configured
- SQL queries filter by `active == True`

### Decision: **KEEP Soft Deletes**

**Rationale**:
- **Audit Trail**: Historical data preserved for reporting
- **Data Integrity**: Prevents accidental data loss
- **GDPR Compliance**: Easier to implement right-to-be-forgotten with soft deletes
- **Undo Capability**: Can reactivate events if needed
- **Analytics**: Historical analysis still possible

### Implementation Details
```python
# Current approach (correct)
@router.post("/delete/{event_id}")
def delete_event(event_id: int, db: Session):
    event = db.query(Event).filter(Event.id == event_id).first()
    event.active = False  # Soft delete
    db.commit()

# Query filter (correct)
db.query(Event).filter(Event.active == True).all()
```

### Cleanup Schedule
- **Monthly**: Archive soft-deleted events > 1 year old to separate table
- **Quarterly**: Review and purge archived events > 3 years per data retention policy
- **Documentation**: Update docs/DELETE_STRATEGY_DECISION.md when policy changes

---

## 2. Unused Files Strategy

### Decision: **DELETE and DOCUMENT**

#### A. Files to Delete (Completed in T002)
- ✅ `frontend/src/services/jogadores.js` - Empty, no functionality
  - Alternative: `players.js` covers all player operations
  - Removed: PR #2
  
#### B. Files to Document and Deprecate
- `frontend/src/services/jogos.js` - Stub for future matches service
  - Status: Keep with clear TODO
  - Timeline: Implement in Sprint 2+
  - Reason: Placeholder for upcoming feature

### Future Unused File Detection
- **Quarterly Review**: Check imports and dependencies quarterly
- **Tool**: Use ESLint/Pylint unused variable detection
- **CI/CD**: Add linting rules to detect dead imports

---

## 3. Database Cleanup Procedures

### Event Cleanup (Soft Deleted)
```sql
-- Find soft-deleted events
SELECT * FROM events WHERE active = 0 AND date < DATE_SUB(NOW(), INTERVAL 1 YEAR);

-- Archive (before permanent delete)
INSERT INTO events_archive SELECT * FROM events WHERE active = 0 AND date < DATE_SUB(NOW(), INTERVAL 1 YEAR);

-- Permanent delete (only after archive)
DELETE FROM events WHERE active = 0 AND date < DATE_SUB(NOW(), INTERVAL 1 YEAR);
```

### Cascade Behavior
- Events cascade delete Players ✅ (Fixed in T003)
- Matches cascade delete outcomes (future implementation)
- **Verification**: Run cascade test quarterly

---

## 4. Code Cleanup Strategy

### Trunk-Based Development Approach
1. **Small Deletions**: Include in feature branches (<5 files)
2. **Large Deletions**: Create dedicated cleanup task in planning
3. **Deprecation**: Always mark deprecated files with TODO before deleting
4. **Git History**: Deletion preserved in git, can be recovered

### Branch Strategy
```bash
# For small cleanup
git checkout -b chore/cleanup-unused-services

# For large cleanup
git checkout -b chore/T0XX-major-cleanup-phase
```

---

## 5. Implementation Timeline

| Phase | Task | Timeline | Owner |
|-------|------|----------|-------|
| **Sprint 1** | T002: Delete jogadores.js | ✅ Done | DevOps |
| **Sprint 1** | T003: Fix cascade | ✅ Done | Backend |
| **Sprint 2** | Implement jogos.js | Week 5-6 | Backend |
| **Sprint 3+** | Dead code analysis tool | Backlog | DevOps |
| **Quarterly** | Archive old soft-deletes | Recurring | DBA |

---

## 6. Monitoring and Alerts

### Metrics to Track
- Soft-deleted event count (monitor growth)
- Unused service imports (catch before commit)
- Database size growth (alert if > 20% monthly)

### CI/CD Integration
```yaml
# Potential future GitHub Actions check
- name: Check for unused imports
  run: pylint --disable=all --enable=unused-import backend/
  
- name: Check unused exports
  run: npx eslint --no-eslintrc --rule 'import/no-unused-modules: [2, {unusedExports: true}]' frontend/
```

---

## 7. Decision Authority

**Team Agreement**:
- ✅ Keep soft deletes for events (audit trail)
- ✅ Delete unused services immediately (clarity)
- ✅ Document stubs with clear timeline (T002 jogos.js)
- ✅ Quarterly review process (scheduled task)

**Approval**:
- Decision Owner: Architecture Review (T000)
- Affected Teams: Backend, Frontend, DevOps
- Review Frequency: Quarterly or on major schema changes

---

## 8. References

- [T001](docs/TASKS.md#T001): Fix EventsView.vue SFC Error
- [T002](docs/TASKS.md#T002): Remove obsolete services  
- [T003](docs/TASKS.md#T003): Fix ORM cascade
- [ARCHITECTURE_REVIEW.md](docs/ARCHITECTURE_REVIEW.md): Project complexity analysis
- [Soft Delete Pattern](https://en.wikipedia.org/wiki/Soft_delete)
- [GDPR Data Deletion](https://gdpr-info.eu/issues/right-to-be-forgotten/)

---

## 9. Appendix: Related Configuration

### Database
```python
# models/event.py
class Event(Base):
    __tablename__ = "events"
    active = Column(Boolean, default=True)  # Soft delete marker
    players = relationship("Player", cascade="all, delete-orphan")
```

### ORM Query Pattern
```python
# All queries must filter active events
def list_active_events(db: Session):
    return db.query(Event).filter(Event.active == True).all()

# To access archived events explicitly
def list_all_events_including_deleted(db: Session):
    return db.query(Event).all()
```

### Frontend
```javascript
// jogos.js - Future implementation stub
// TODO: Implement when matches backend is ready (Sprint 2+)
// This will handle match/game operations including create, list, update, delete
// Endpoint: /matches
```

---

**Sprint 1 Completed**: March 2024  
**Next Review**: June 2024 (Q2)
