/**
 * API helper utilities for E2E tests
 * Handles direct API calls for test setup and verification
 */

const API_URL = 'http://127.0.0.1:8000';

/**
 * Create a test event
 */
export async function createTestEvent(name = 'Test Tournament', date = getTodayDate(), time = '14:00') {
  const response = await fetch(`${API_URL}/events`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, date, time }),
  });
  if (!response.ok) throw new Error(`Failed to create event: ${response.statusText}`);
  return response.json();
}

/**
 * Get all events
 */
export async function getAllEvents() {
  const response = await fetch(`${API_URL}/events`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });
  if (!response.ok) throw new Error(`Failed to get events: ${response.statusText}`);
  return response.json();
}

/**
 * Delete an event (soft delete via API)
 */
export async function deleteTestEvent(eventId) {
  const response = await fetch(`${API_URL}/events/${eventId}`, {
    method: 'DELETE',
  });
  if (!response.ok) throw new Error(`Failed to delete event: ${response.statusText}`);
  return response.json();
}

/**
 * Register a player for an event
 */
export async function registerPlayer(eventId, name = 'Test Player') {
  const response = await fetch(`${API_URL}/players`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ event_id: eventId, name }),
  });
  if (!response.ok) throw new Error(`Failed to register player: ${response.statusText}`);
  return response.json();
}

/**
 * Record a match result
 */
export async function recordMatch(eventId, player1Id, player2Id, winnerId) {
  const response = await fetch(`${API_URL}/matches`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      event_id: eventId,
      player1_id: player1Id,
      player2_id: player2Id,
      winner_id: winnerId,
      best_of: 5,
    }),
  });
  if (!response.ok) throw new Error(`Failed to record match: ${response.statusText}`);
  return response.json();
}

/**
 * Get event ranking
 */
export async function getEventRanking(eventId) {
  const response = await fetch(`${API_URL}/ranking/event/${eventId}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });
  if (!response.ok) throw new Error(`Failed to get ranking: ${response.statusText}`);
  return response.json();
}

/**
 * Get today's date in YYYY-MM-DD format
 */
export function getTodayDate() {
  const now = new Date();
  return now.toISOString().split('T')[0];
}

/**
 * Wait for element with text
 */
export async function waitForText(page, text, timeout = 5000) {
  await page.waitForSelector(`text=${text}`, { timeout });
}

/**
 * Click element with text
 */
export async function clickText(page, text) {
  await page.click(`text=${text}`);
}

/**
 * Fill form field by label
 */
export async function fillFieldByLabel(page, label, value) {
  const input = page.locator(`label:has-text("${label}") ~ input, label:has-text("${label}") ~ textarea`).first();
  await input.fill(value);
}

/**
 * Clear database by deleting all events
 */
export async function clearTestDatabase() {
  try {
    const events = await getAllEvents();
    for (const event of events) {
      await deleteTestEvent(event.id);
    }
  } catch (err) {
    console.warn('Failed to clear database:', err.message);
  }
}
