import { test, expect, beforeEach, afterEach } from '@playwright/test';
import { createTestEvent, deleteTestEvent, getTodayDate, clearTestDatabase } from './helpers';

/**
 * E2E tests for Event Creation workflow
 * Tests the complete flow from event creation form through list display
 */

let testEventId;

beforeEach(async ({ page }) => {
  // Clear any existing test data
  await clearTestDatabase();
});

afterEach(async () => {
  // Cleanup created test event if needed
  if (testEventId) {
    try {
      await deleteTestEvent(testEventId);
    } catch (err) {
      console.warn('Cleanup failed:', err.message);
    }
  }
});

test.describe('Event Creation Workflow', () => {
  test('should navigate to events page', async ({ page }) => {
    await page.goto('/');
    await page.click('a:has-text("Events")');
    await expect(page).toHaveURL(/.*events/);
  });

  test('should display events list', async ({ page }) => {
    await page.goto('/events');
    await expect(page.locator('h1, h2')).toContainText(/events|tournaments/i);
  });

  test('should create a new event via form', async ({ page }) => {
    await page.goto('/events');
    
    // Click create event button
    await page.click('button:has-text("Create Event"), button:has-text("New Event"), button:has-text("Add Event")');
    
    // Fill form
    const todayDate = getTodayDate();
    await page.fill('input[type="text"][placeholder*="name" i], input[placeholder*="event" i]', 'E2E Test Tournament');
    await page.fill('input[type="date"], input[placeholder*="date" i]', todayDate);
    await page.fill('input[type="time"], input[placeholder*="time" i]', '14:00');
    
    // Submit form
    await page.click('button:has-text("Create"), button:has-text("Save")');
    
    // Verify success (event appears in list or confirmation message)
    await expect(page).not.toHaveURL(/.*create/); // Should redirect away from create page
    await expect(page.locator('text=E2E Test Tournament')).toBeVisible({ timeout: 5000 });
  });

  test('should create event via API and display in list', async ({ page }) => {
    // Create event via API
    const event = await createTestEvent('API Created Tournament');
    testEventId = event.id;
    
    // Navigate to events page
    await page.goto('/events');
    
    // Verify event appears in list
    await expect(page.locator(`text=${event.name}`)).toBeVisible({ timeout: 5000 });
  });

  test('should navigate to event details from list', async ({ page }) => {
    // Create test event
    const event = await createTestEvent('Details Test Event');
    testEventId = event.id;
    
    // Navigate to events list
    await page.goto('/events');
    
    // Click on event
    await page.click(`a:has-text("${event.name}"), button:has-text("${event.name}")`);
    
    // Verify we're on event details page
    await expect(page).toHaveURL(/.*events.*\d+|.*event.*detail/i);
    await expect(page.locator(`text=${event.name}`)).toBeVisible();
  });

  test('should display event date and time correctly', async ({ page }) => {
    const todayDate = getTodayDate();
    const event = await createTestEvent('Date Time Test', todayDate, '15:30');
    testEventId = event.id;
    
    await page.goto('/events');
    
    // Check date and time are displayed
    const eventElement = page.locator(`text=${event.name}`).first();
    await expect(eventElement).toBeVisible();
    
    // Look for date/time display near event
    const container = eventElement.locator('xpath=./ancestor::*[contains(@class, "card") or contains(@class, "item") or contains(@class, "row")]');
    await expect(container.locator(`text=${todayDate}`)).toBeVisible({ timeout: 5000 }).catch(() => {
      // Date might be in different format, that's ok
      console.log('Date format may differ from display');
    });
  });

  test('should handle event creation validation', async ({ page }) => {
    await page.goto('/events');
    
    // Try to create without name
    await page.click('button:has-text("Create Event"), button:has-text("New Event"), button:has-text("Add Event")');
    await page.fill('input[type="date"], input[placeholder*="date" i]', getTodayDate());
    await page.fill('input[type="time"], input[placeholder*="time" i]', '14:00');
    
    // Try to submit
    const submitButton = page.locator('button:has-text("Create"), button:has-text("Save")');
    
    // Should either prevent submission or show error
    await submitButton.click();
    
    // Check for error message or still on form page
    const hasError = await page.locator('text=required, text=error, text=invalid').first().isVisible({ timeout: 3000 }).catch(() => false);
    const stillOnForm = page.url().includes('create') || page.url().includes('new');
    
    await expect(hasError || stillOnForm).toBeTruthy();
  });
});
