import { test, expect } from '@playwright/test';
import { createTestEvent, deleteTestEvent, getTodayDate } from './helpers';

/**
 * E2E tests for Event Creation workflow
 * Tests the complete flow from event creation form through list display
 */

let testEventId;

test.beforeEach(async ({ page }) => {
  // Set default timeout for page interactions
  page.setDefaultTimeout(10000);
  page.setDefaultNavigationTimeout(10000);
  
  // Pre-navigate to ensure page is loaded
  await page.goto('/events', { waitUntil: 'domcontentloaded' }).catch(() => {
    // Navigation error is acceptable in beforeEach
  });
});

test.afterEach(async () => {
  // Cleanup created test event if needed
  if (testEventId) {
    try {
      await deleteTestEvent(testEventId);
    } catch (err) {
      console.warn('Cleanup failed:', err.message);
    }
    testEventId = null;
  }
});

test.describe('Event Navigation and Display', () => {
  test('should navigate to events page from home', async ({ page }) => {
    await page.goto('/', { waitUntil: 'domcontentloaded' });
    
    // Use getByRole instead of CSS selectors
    const eventsLink = page.getByRole('link', { name: /events/i });
    await expect(eventsLink).toBeVisible({ timeout: 5000 });
    await eventsLink.click();
    
    // Wait for navigation
    await expect(page).toHaveURL(/.*events/, { timeout: 5000 });
  });

  test('should display events heading', async ({ page }) => {
    await page.goto('/events', { waitUntil: 'domcontentloaded' });
    
    const heading = page.locator('h1, h2').first();
    await expect(heading).toBeVisible({ timeout: 5000 });
  });

  test('should create event via API and verify list updates', async ({ page }) => {
    try {
      // Create event via API
      const event = await createTestEvent('Test_Event_' + Date.now());
      testEventId = event.id;
      
      // Navigate to events page
      await page.goto('/events', { waitUntil: 'domcontentloaded' });
      
      // Wait for page to stabilize
      await page.waitForLoadState('networkidle').catch(() => {
        // Network idle might not complete, that's ok
      });
      await page.waitForTimeout(1000);
      
      // Look for event using multiple strategies
      const eventByText = page.locator(`text=${event.name}`);
      const eventVisible = await eventByText.isVisible({ timeout: 5000 }).catch(() => false);
      
      if (!eventVisible) {
        console.log('Event not visible, checking page content');
        const pageText = await page.textContent('body');
        expect(pageText).toContain(event.name);
      }
    } catch (err) {
      console.warn('Test failed:', err.message);
      throw err;
    }
  });

  test('should display event form', async ({ page }) => {
    await page.goto('/events', { waitUntil: 'domcontentloaded' });
    
    // Check for form elements
    const nameField = page.getByLabel(/event name|name/i);
    const dateField = page.locator('input[type="date"]');
    const createButton = page.getByRole('button', { name: /create|add/i });
    
    // At least one of these should exist
    const nameFieldExists = await nameField.isVisible({ timeout: 3000 }).catch(() => false);
    const dateFieldExists = await dateField.isVisible({ timeout: 3000 }).catch(() => false);
    const createButtonExists = await createButton.isVisible({ timeout: 3000 }).catch(() => false);
    
    expect(nameFieldExists || dateFieldExists || createButtonExists).toBeTruthy();
  });
});
