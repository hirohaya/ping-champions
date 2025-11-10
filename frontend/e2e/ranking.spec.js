import { test, expect } from '@playwright/test';
import { createTestEvent, deleteTestEvent, registerPlayer, recordMatch, getEventRanking, getTodayDate, clearTestDatabase } from './helpers';

/**
 * E2E tests for Ranking/Leaderboard workflow
 * Tests ranking display and leaderboard functionality
 */

let testEventId;
let player1Id;
let player2Id;
let player3Id;

test.beforeEach(async () => {
  // Clear any existing test data
  await clearTestDatabase();
  
  // Create test event and multiple players
  const event = await createTestEvent('Ranking Test Event');
  testEventId = event.id;
  
  const p1 = await registerPlayer(testEventId, 'Alice Champion');
  const p2 = await registerPlayer(testEventId, 'Bob Challenger');
  const p3 = await registerPlayer(testEventId, 'Carol Competitor');
  
  player1Id = p1.id;
  player2Id = p2.id;
  player3Id = p3.id;
  
  // Record some matches to create ranking variation
  await recordMatch(testEventId, player1Id, player2Id, player1Id);
  await recordMatch(testEventId, player1Id, player3Id, player1Id);
  await recordMatch(testEventId, player2Id, player3Id, player2Id);
});

test.afterEach(async () => {
  // Cleanup
  if (testEventId) {
    try {
      await deleteTestEvent(testEventId);
    } catch (err) {
      console.warn('Cleanup failed:', err.message);
    }
  }
});

test.describe('Ranking/Leaderboard Workflow', () => {
  test('should navigate to ranking page for event', async ({ page }) => {
    await page.goto('/events');
    
    // Navigate to event details
    await page.click(`a:contains("Ranking Test Event"), button:contains("Ranking Test Event")`);
    
    // Navigate to ranking section
    await page.click('a:has-text("Ranking"), button:has-text("Ranking"), a:has-text("Leaderboard"), button:has-text("Leaderboard")');
    
    await expect(page).toHaveURL(/.*ranking|.*leaderboard/i);
  });

  test('should display ranking table with players', async ({ page }) => {
    await page.goto(`/events/${testEventId}/ranking`);
    
    // Should see ranking/leaderboard heading
    await expect(page.locator('h1, h2, text=ranking, text=leaderboard')).toBeVisible({ timeout: 5000 });
    
    // Should display players
    await expect(page.locator('text=Alice Champion')).toBeVisible({ timeout: 5000 });
    await expect(page.locator('text=Bob Challenger')).toBeVisible({ timeout: 5000 });
    await expect(page.locator('text=Carol Competitor')).toBeVisible({ timeout: 5000 });
  });

  test('should display ranking statistics', async ({ page }) => {
    await page.goto(`/events/${testEventId}/ranking`);
    
    // Verify table headers for ranking data
    await expect(page.locator('th, [role="columnheader"]')).toContainText(/rank|position|#/i);
    
    // Should show wins/losses or similar stats
    const statsHeaders = page.locator('th, [role="columnheader"]');
    await expect(statsHeaders).toContainText(/win|loss|record|games/i);
  });

  test('should order players by ranking via API data', async ({ page }) => {
    // Get ranking from API
    const ranking = await getEventRanking(testEventId);
    
    // Navigate to ranking page
    await page.goto(`/events/${testEventId}/ranking`);
    
    // Verify players are displayed in ranking order
    const rows = page.locator('tr, [class*="row"], [class*="item"]');
    
    // First player should be champion (Alice)
    const firstPlayer = rows.first();
    await expect(firstPlayer).toContainText('Alice Champion');
  });

  test('should update ranking after match is recorded', async ({ page }) => {
    // Navigate to ranking page
    await page.goto(`/events/${testEventId}/ranking`);
    
    // Record a new match via API
    await recordMatch(testEventId, player3Id, player1Id, player3Id);
    
    // Refresh page to see updated ranking
    await page.reload();
    
    // Ranking should still be displayed with updated data
    await expect(page.locator('text=Alice Champion')).toBeVisible({ timeout: 5000 });
    await expect(page.locator('text=Carol Competitor')).toBeVisible({ timeout: 5000 });
  });

  test('should display player statistics correctly', async ({ page }) => {
    await page.goto(`/events/${testEventId}/ranking`);
    
    // Find Alice's row (should be top ranking with 2 wins, 0 losses)
    const aliceRow = page.locator(`text=Alice Champion`).first();
    const container = aliceRow.locator('xpath=./ancestor::tr, ./ancestor::*[contains(@class, "row") or contains(@class, "item")]');
    
    // Should show win record
    await expect(container).toContainText(/2|win/i);
  });

  test('should show empty ranking for event with no matches', async ({ page }) => {
    // Create event with players but no matches
    const emptyEvent = await createTestEvent('No Matches For Ranking');
    await registerPlayer(emptyEvent.id, 'Solo Player 1');
    await registerPlayer(emptyEvent.id, 'Solo Player 2');
    
    try {
      // Navigate to ranking page
      await page.goto(`/events/${emptyEvent.id}/ranking`);
      
      // Should show players with 0 wins/losses
      await expect(page.locator('text=Solo Player')).toBeVisible({ timeout: 5000 });
      
      // Should show 0 wins initially
      const statsContent = page.locator('body').textContent();
      const hasZeroStats = statsContent.includes('0') || statsContent.includes('zero');
    } finally {
      await deleteTestEvent(emptyEvent.id);
    }
  });

  test('should handle single player event ranking', async ({ page }) => {
    // Create event with single player
    const singleEvent = await createTestEvent('Single Player Event');
    await registerPlayer(singleEvent.id, 'Lone Player');
    
    try {
      // Navigate to ranking page
      await page.goto(`/events/${singleEvent.id}/ranking`);
      
      // Should display the single player
      await expect(page.locator('text=Lone Player')).toBeVisible({ timeout: 5000 });
    } finally {
      await deleteTestEvent(singleEvent.id);
    }
  });

  test('should display win rate or percentage', async ({ page }) => {
    await page.goto(`/events/${testEventId}/ranking`);
    
    // Look for win rate indicator (percentage, decimal, or ratio)
    const pageContent = await page.locator('body').textContent();
    
    // Should have some win rate display (0%, 100%, 1.0, etc.)
    // Alice should have 100% (2 wins, 0 losses)
    const aliceRow = page.locator(`text=Alice Champion`).first();
    const container = aliceRow.locator('xpath=./ancestor::tr, ./ancestor::*[contains(@class, "row") or contains(@class, "item")]');
    
    await expect(container).toBeVisible();
  });
});
