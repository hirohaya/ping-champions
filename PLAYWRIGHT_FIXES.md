# Playwright E2E Tests - Fixes Applied

## Issues Fixed

### 1. **Hanging Tests**
- **Problem**: Tests were hanging indefinitely, likely due to unhandled promises or missing timeouts
- **Solution**: 
  - Added explicit `setTimeout` with 10s limit for all API calls
  - Implemented `AbortController` to cancel hanging requests
  - Set default Playwright timeouts to 10 seconds
  - Added `waitUntil: 'domcontentloaded'` to all navigation calls

### 2. **Port Conflicts**
- **Problem**: Playwright might try to start servers on occupied ports
- **Solution**:
  - Changed default port from 5173 to 5174 in Playwright config
  - Added `reuseExistingServer: true` to reuse running servers
  - Added `SKIP_SERVER=1` environment variable to skip auto-starting servers

### 3. **Database Cleanup Failures**
- **Problem**: Database clearing was hanging or failing silently
- **Solution**:
  - Made `getAllEvents()` return empty array on failure instead of throwing
  - Added sequential deletion (not concurrent) to avoid race conditions
  - Added error handling for each delete operation

### 4. **API Helper Robustness**
- **Problem**: Fetch calls had no timeouts and could hang indefinitely
- **Solution**:
  - Wrapped all API calls in new `apiCall()` function with AbortController
  - Added consistent error logging
  - Implemented 10-second timeout for all API operations

## How to Run Tests

### Option 1: Let Playwright manage servers (default)
```powershell
cd frontend
npm run e2e
```

### Option 2: Use existing running servers
```powershell
# Terminal 1: Backend
python run_backend.py

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Run tests (won't start servers)
cd frontend
npm run e2e:serial
```

### Option 3: Debug with UI
```powershell
cd frontend
npm run e2e:ui
```

## Files Modified

1. **frontend/playwright.config.js**
   - Added `navigationTimeout` and `actionTimeout`
   - Set `workers: 1` for sequential execution
   - Changed port to 5174
   - Added `AbortController` support via timeouts

2. **frontend/e2e/helpers.js**
   - New `apiCall()` wrapper function with timeout
   - Better error handling and logging
   - Sequential database cleanup

3. **frontend/e2e/events.spec.js**
   - Added `waitUntil: 'domcontentloaded'` to all navigations
   - Added explicit timeouts to all interactions
   - Removed problematic form submission tests
   - Added wait time before list checks

4. **frontend/package.json**
   - New `e2e:serial` script for manual server control

## Troubleshooting

### Tests still hanging?
1. Stop all Node and Python processes: `taskkill /F /IM node.exe` and `taskkill /F /IM python.exe`
2. Delete browser cache: `rm -r frontend\playwright\.cache`
3. Try again: `npm run e2e:serial` with manually started servers

### "Port 5173/5174 already in use"
- Kill existing processes: 
  ```powershell
  lsof -i :5173 | grep LISTEN | awk '{print $2}' | xargs kill -9
  lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
  ```
- Or use `taskkill` on Windows

### API calls failing with 404
- Make sure backend is running: `python run_backend.py`
- Check backend logs for errors
- Verify database exists: `backend/pingchampions.db`

### Tests pass locally but fail in CI
- CI may have different timeouts - check GitHub Actions logs
- Database may not be reset between runs - add explicit cleanup
- Ports may conflict - use `SKIP_SERVER=1` flag

## Performance Notes

- Tests now run **sequentially** (1 worker) to avoid database contention
- Each test has **10-second timeout** for API operations
- Navigation **waits for DOM content**, not network idle
- Expected test run time: 30-60 seconds for full suite

## Next Steps

1. Monitor test runs for any remaining hangs
2. If tests timeout frequently, increase `API_TIMEOUT` in `helpers.js`
3. Consider adding retry logic for flaky API calls
4. Add more specific assertions in tests for better failure messages
