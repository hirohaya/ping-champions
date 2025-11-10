# Playwright MCP Testing Workflow - Instructions Added

## Summary

Added comprehensive mandatory testing instructions to `.github/copilot-instructions.md` requiring all implementations to be tested immediately using Playwright MCP.

## What Was Added

### New Section: "Implementation & Testing Workflow"

A complete 8-step mandatory workflow that governs how ALL code changes must be made and tested:

#### 1. **Project State Before Implementation**
- Both backend and frontend must be running
- Backend: `python run_backend.py` on `http://127.0.0.1:8000`
- Frontend: `npm run dev` on `http://localhost:5173`
- Verify both are responding before any code changes

#### 2. **Development Cycle**
1. Make code changes
2. Save files (Vite and uvicorn auto-reload)
3. **Immediately test in browser using Playwright MCP** ✅
4. Verify changes
5. Repeat for next feature

#### 3. **Playwright MCP Testing Protocol**

**When to Test** (mandatory for):
- ✅ After every backend endpoint modification
- ✅ After every frontend component change
- ✅ After database schema changes
- ✅ After service layer updates
- ✅ Before committing code to git

**Testing Approach**:
1. Navigate to page: `mcp_microsoft_pla_browser_navigate(url)`
2. Wait for content: `mcp_microsoft_pla_browser_wait_for(time)`
3. Take snapshot: `mcp_microsoft_pla_browser_snapshot()`
4. Interact with UI: click, type, select, fill forms
5. Verify results: check alerts, inspect state, verify API responses
6. Test edge cases: validation, error states, empty states

**Example Test Flow**:
```
Navigate → Wait → Snapshot (verify page loaded)
→ Click button → Type text → Submit form
→ Check alert message → Verify data in list
→ Refresh page → Verify persistence
```

#### 4. **Key Playwright Commands** (Reference)
- `mcp_microsoft_pla_browser_navigate(url)` - Navigate to page
- `mcp_microsoft_pla_browser_snapshot()` - Get page state
- `mcp_microsoft_pla_browser_click(element, ref)` - Click element
- `mcp_microsoft_pla_browser_type(element, ref, text)` - Type into field
- `mcp_microsoft_pla_browser_select_option(element, ref, values)` - Select dropdown
- `mcp_microsoft_pla_browser_fill_form(fields)` - Fill multiple fields
- `mcp_microsoft_pla_browser_wait_for(time)` - Wait for condition
- `mcp_microsoft_pla_browser_handle_dialog(accept)` - Handle alerts
- `mcp_microsoft_pla_browser_take_screenshot(filename)` - Take screenshot

#### 5. **Test Coverage Requirements**

**Minimum per feature**:
- ✅ Happy path (successful operation)
- ✅ Validation failures (invalid input)
- ✅ API error handling (404, 500, etc.)
- ✅ Data persistence (page refresh)
- ✅ Related features (rankings, calculations, etc.)

**Example for Match Creation**:
- Create match with valid data → verify appears in list
- Create match with invalid data → verify error message
- Create match without required field → verify validation alert
- Refresh page → verify match still exists
- Check rankings updated → verify Elo calculations

#### 6. **Success Criteria**
- All Playwright tests pass without errors
- No browser console errors ([ERROR] messages)
- Form validation works as designed
- Data persists after page refresh
- Related calculations/rankings update correctly
- No breaking changes to existing features

#### 7. **Documentation of Test Results**
After testing, document:
- Test scenarios attempted
- Pass/fail status for each scenario
- Any alerts or error messages displayed
- Final state verification (rankings, data, etc.)
- Screenshots of successful UI if complex feature

#### 8. **Common Testing Mistakes to Avoid** (Critical)
- ❌ Making changes without running backend/frontend
- ❌ Skipping browser testing (only running unit tests)
- ❌ Not waiting for async operations (use `mcp_microsoft_pla_browser_wait_for`)
- ❌ Not checking page state after actions (use `mcp_microsoft_pla_browser_snapshot`)
- ❌ Forgetting to test data persistence (page refresh)
- ❌ Not testing validation and error cases
- ❌ Leaving browser in inconsistent state (always navigate fresh)

#### 9. **Terminal Management**
- Keep servers running: Background process with `isBackground=true`
- Check output: Use `get_terminal_output(id)` to verify no errors
- Close on completion: Kill terminals after final testing
- Monitor logs: Watch for exceptions or warnings

## File Changed

- `.github/copilot-instructions.md` (+102 lines)

## Git Commit

```
docs: Add mandatory Playwright MCP testing workflow to copilot instructions
```

## Impact

This establishes a **mandatory workflow** that all AI coding agents must follow:

1. **Every code change requires immediate browser testing** - No exceptions
2. **Playwright MCP is the standard testing tool** for UI verification
3. **Tests must cover happy path, validation, persistence, and edge cases**
4. **Both servers must be running before making changes**
5. **Documentation of test results is required**

## Why This Matters

The previous implementation of the Match Score Recording feature demonstrated that:
- Code changes made without immediate testing can have subtle issues
- API schema changes need immediate UI verification
- Database changes need persistence verification
- Complex features need comprehensive testing across multiple scenarios

These instructions ensure **every future implementation** follows the same rigorous testing protocol.

## Example: Match Score Recording Implementation

The Match Score Recording feature that was just completed would follow this workflow:

1. **Start both servers** ✅
2. **Make backend model changes** (add 3 columns)
3. **Test immediately** with Playwright:
   - Navigate to `/events/2/matches`
   - Create a test match
   - Verify form appears and data saves
   - Refresh page to verify persistence
4. **Make frontend changes** (redesign MatchesView.vue)
5. **Test immediately** with Playwright:
   - Verify two-step form displays
   - Enter test data
   - Verify submission
   - Check that data persists and displays correctly
6. **Make API schema changes**
7. **Test immediately** with Playwright:
   - Create another test match
   - Verify rankings calculate correctly
8. **Commit changes** only after all tests pass

---

## Next Steps for Copilot

When implementing ANY feature for Ping Champions:
1. Read this entire workflow section
2. Start both backend and frontend servers
3. Make changes incrementally
4. **Test immediately after each change using Playwright MCP**
5. Document test results
6. Commit only when all tests pass

---

**Status**: ✅ Instructions added and committed to repository
**Date**: November 10, 2025
**Commit Hash**: Check `git log` for latest commit

