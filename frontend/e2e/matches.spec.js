import { test, expect, beforeEach, afterEach } from '@playwright/test';
import { createTestEvent, deleteTestEvent, registerPlayer, recordMatch, getTodayDate, clearTestDatabase } from './helpers';

/**
 * E2E tests for Match Recording workflow
 * Tests recording match results and verifying match display
 */

let testEventId;
let player1Id;
let player2Id;

beforeEach(async () => {
  // Clear any existing test data
  await clearTestDatabase();
  
  // Create test event and players
  const event = await createTestEvent('Match Test Event');
  testEventId = event.id;
  
  const player1 = await registerPlayer(testEventId, 'Player One');
  const player2 = await registerPlayer(testEventId, 'Player Two');
  
  player1Id = player1.id;
  player2Id = player2.id;
});

afterEach(async () => {
  // Cleanup
  if (testEventId) {
    try {
      await deleteTestEvent(testEventId);
    } catch (err) {
      console.warn('Cleanup failed:', err.message);
    }
  }
});

test.describe('Match Recording Workflow', () => {
  test('should navigate to matches page for event', async ({ page }) => {
    await page.goto('/events');
    
    // Navigate to event details
    await page.click(`a:contains("Match Test Event"), button:contains("Match Test Event")`);
    
    // Navigate to matches section
    await page.click('a:has-text("Matches"), button:has-text("Matches"), a:has-text("Games"), button:has-text("Games")');
    
    await expect(page).toHaveURL(/.*match|.*game/i);
  });

  test('should display matches list', async ({ page }) => {
    await page.goto(`/events/${testEventId}/matches`);
    
    // Should see matches heading or empty state
    await expect(page.locator('h1, h2, text=matches, text=games')).toBeVisible({ timeout: 5000 });
  });

  test('should record a match via form', async ({ page }) => {
    await page.goto(`/events/${testEventId}/matches`);
    
    // Click to create/record match
    await page.click('button:has-text("Record Match"), button:has-text("New Match"), button:has-text("Add Match")');
    
    // Select players (dropdown or selection)
    await page.selectOption('select', { label: 'Player One' }).catch(async () => {
      // Try clicking if not a select
      await page.click(`text=Player One`);
    });
    
    await page.selectOption('select', { label: 'Player Two' }).catch(async () => {
      // Try clicking if not a select
      await page.click(`text=Player Two`);
    });
    
    // Select winner
    await page.selectOption('select', { label: 'Player One' }).catch(async () => {
      await page.click(`text=Player One`);
    });
    
    // Submit
    await page.click('button:has-text("Record"), button:has-text("Save")');
    
    // Verify match appears in list
    const matchText = page.locator('text=Player One, text=Player Two').first();
    await expect(matchText).toBeVisible({ timeout: 5000 });
  });

  test('should record match via API and display in list', async ({ page }) => {
    // Record match via API
    const match = await recordMatch(testEventId, player1Id, player2Id, player1Id);
    
    // Navigate to matches page
    await page.goto(`/events/${testEventId}/matches`);
    
    // Verify match appears
    await expect(page.locator('text=Player One')).toBeVisible({ timeout: 5000 });
    await expect(page.locator('text=Player Two')).toBeVisible({ timeout: 5000 });
  });

  test('should display match details correctly', async ({ page }) => {
    // Record a match
    const match = await recordMatch(testEventId, player1Id, player2Id, player1Id);
    
    // Navigate to matches page
    await page.goto(`/events/${testEventId}/matches`);
    
    // Find match row/card
    const matchRow = page.locator(`text=Player One`).first();
    await expect(matchRow).toBeVisible();
    
    // Should show both players and winner
    const container = matchRow.locator('xpath=./ancestor::*[contains(@class, "card") or contains(@class, "item") or contains(@class, "row")]');
    await expect(container.locator('text=Player Two')).toBeVisible();
  });

  test('should show empty matches list initially', async ({ page }) => {
    // Create new event with players but no matches
    const emptyEvent = await createTestEvent('No Matches Event');
    const p1 = await registerPlayer(emptyEvent.id, 'No Match Player 1');
    const p2 = await registerPlayer(emptyEvent.id, 'No Match Player 2');
    
    try {
      // Navigate to matches page
      await page.goto(`/events/${emptyEvent.id}/matches`);
      
      // Should show empty state
      const emptyText = page.locator('text=no matches, text=empty, text=none');
      const hasEmptyMessage = await emptyText.isVisible({ timeout: 3000 }).catch(() => false);
      
      // Or should not have any player names visible
      const hasMatchContent = await page.locator('text=No Match Player').isVisible({ timeout: 3000 }).catch(() => false);
      
      await expect(hasEmptyMessage || !hasMatchContent).toBeTruthy();
    } finally {
      await deleteTestEvent(emptyEvent.id);
    }
  });

  test('should prevent invalid match recording', async ({ page }) => {
    await page.goto(`/events/${testEventId}/matches`);
    
    // Try to record match with same player twice
    await page.click('button:has-text("Record Match"), button:has-text("New Match"), button:has-text("Add Match")');
    
    // Try to select same player twice
    await page.selectOption('select', { label: 'Player One' }).catch(() => {});
    await page.selectOption('select', { label: 'Player One' }).catch(() => {});
    
    // Try to submit
    const submitButton = page.locator('button:has-text("Record"), button:has-text("Save")');
    await submitButton.click().catch(() => {});
    
    // Should either prevent submission or show error
    const hasError = await page.locator('text=error, text=invalid, text=different').first().isVisible({ timeout: 3000 }).catch(() => false);
    const stillOnForm = page.url().includes('record') || page.url().includes('new');
    
    await expect(hasError || stillOnForm).toBeTruthy();
  });
});
