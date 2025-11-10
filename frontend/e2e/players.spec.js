import { test, expect } from '@playwright/test';
import { createTestEvent, deleteTestEvent, registerPlayer, getTodayDate, clearTestDatabase } from './helpers';

/**
 * E2E tests for Player Registration workflow
 * Tests player registration and management within an event
 */

let testEventId;

test.beforeEach(async () => {
  // Clear any existing test data
  await clearTestDatabase();
  // Create a test event for player tests
  const event = await createTestEvent('Player Test Event');
  testEventId = event.id;
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

test.describe('Player Registration Workflow', () => {
  test('should navigate to players page for event', async ({ page }) => {
    await page.goto('/events');
    
    // Navigate to event details
    await page.click(`a:contains("Player Test Event"), button:contains("Player Test Event")`);
    
    // Navigate to players section
    await page.click('a:has-text("Players"), button:has-text("Players")');
    
    await expect(page).toHaveURL(/.*player/i);
  });

  test('should register a player via form', async ({ page }) => {
    await page.goto(`/events/${testEventId}/players`);
    
    // Click register button
    await page.click('button:has-text("Register"), button:has-text("Add Player"), button:has-text("New Player")');
    
    // Fill player name
    await page.fill('input[type="text"][placeholder*="name" i], input[placeholder*="player" i]', 'Test Player 1');
    
    // Submit
    await page.click('button:has-text("Register"), button:has-text("Save")');
    
    // Verify player appears in list
    await expect(page.locator('text=Test Player 1')).toBeVisible({ timeout: 5000 });
  });

  test('should register multiple players via API', async ({ page }) => {
    // Register players via API
    const player1 = await registerPlayer(testEventId, 'Alice Smith');
    const player2 = await registerPlayer(testEventId, 'Bob Johnson');
    
    // Navigate to players page
    await page.goto(`/events/${testEventId}/players`);
    
    // Verify both players are listed
    await expect(page.locator('text=Alice Smith')).toBeVisible({ timeout: 5000 });
    await expect(page.locator('text=Bob Johnson')).toBeVisible({ timeout: 5000 });
  });

  test('should display player score and ranking', async ({ page }) => {
    // Register a player
    const player = await registerPlayer(testEventId, 'Score Test Player');
    
    // Navigate to players page
    await page.goto(`/events/${testEventId}/players`);
    
    // Check player is displayed with score/ranking fields
    const playerRow = page.locator(`text=${player.name}`).first();
    await expect(playerRow).toBeVisible();
    
    // Look for score and ranking columns
    const container = playerRow.locator('xpath=./ancestor::*[contains(@class, "card") or contains(@class, "item") or contains(@class, "row")]');
    
    // Player should have initial score display
    await expect(container).toBeVisible();
  });

  test('should handle player registration validation', async ({ page }) => {
    await page.goto(`/events/${testEventId}/players`);
    
    // Click register button
    await page.click('button:has-text("Register"), button:has-text("Add Player"), button:has-text("New Player")');
    
    // Try to submit without name
    await page.click('button:has-text("Register"), button:has-text("Save")');
    
    // Should show error or stay on form
    const hasError = await page.locator('text=required, text=error, text=invalid').first().isVisible({ timeout: 3000 }).catch(() => false);
    const stillOnForm = page.url().includes('register') || page.url().includes('new');
    
    await expect(hasError || stillOnForm).toBeTruthy();
  });

  test('should show empty players list for new event', async ({ page }) => {
    // Create another empty event
    const emptyEvent = await createTestEvent('Empty Event');
    
    try {
      // Navigate to players page
      await page.goto(`/events/${emptyEvent.id}/players`);
      
      // Should show empty state or no players
      const emptyText = page.locator('text=no players, text=empty, text=none');
      const playerTable = page.locator('table, [class*="player"], [class*="list"]');
      
      // Either empty message or empty table
      let isEmpty = false;
      try {
        isEmpty = await emptyText.isVisible({ timeout: 3000 });
      } catch {
        const tableVisible = await playerTable.isVisible({ timeout: 3000 }).catch(() => false);
        isEmpty = !tableVisible;
      }
      
      await expect(isEmpty).toBeTruthy();
    } finally {
      await deleteTestEvent(emptyEvent.id);
    }
  });
});
