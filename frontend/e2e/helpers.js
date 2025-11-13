/**
 * API helper utilities for E2E tests
 * Handles direct API calls for test setup and verification
 */

const API_URL = 'http://127.0.0.1:8000';
const API_TIMEOUT = 10000; // 10 second timeout

/**
 * Helper to make API calls with timeout
 */
async function apiCall(endpoint, options = {}) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT);
  
  try {
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      signal: controller.signal,
      headers: { 'Content-Type': 'application/json', ...options.headers },
    });
    
    if (!response.ok) {
      throw new Error(`API Error [${response.status}]: ${response.statusText}`);
    }
    
    return await response.json();
  } finally {
    clearTimeout(timeoutId);
  }
}

/**
 * Create a test event
 */
export async function createTestEvent(name = 'Test Tournament', date = getTodayDate(), time = '14:00') {
  try {
    return await apiCall('/events', {
      method: 'POST',
      body: JSON.stringify({ name, date, time }),
    });
  } catch (err) {
    console.error('createTestEvent failed:', err.message);
    throw err;
  }
}

/**
 * Get all events
 */
export async function getAllEvents() {
  try {
    return await apiCall('/events', { method: 'GET' });
  } catch (err) {
    console.error('getAllEvents failed:', err.message);
    return [];
  }
}

/**
 * Delete an event (soft delete via API)
 */
export async function deleteTestEvent(eventId) {
  try {
    return await apiCall(`/events/${eventId}`, { method: 'DELETE' });
  } catch (err) {
    console.error(`deleteTestEvent(${eventId}) failed:`, err.message);
    throw err;
  }
}

/**
 * Register a player for an event
 */
export async function registerPlayer(eventId, name = 'Test Player') {
  try {
    return await apiCall('/players', {
      method: 'POST',
      body: JSON.stringify({ event_id: eventId, name }),
    });
  } catch (err) {
    console.error('registerPlayer failed:', err.message);
    throw err;
  }
}

/**
 * Record a match result
 */
export async function recordMatch(eventId, player1Id, player2Id, winnerId) {
  try {
    return await apiCall('/matches', {
      method: 'POST',
      body: JSON.stringify({
        event_id: eventId,
        player1_id: player1Id,
        player2_id: player2Id,
        winner_id: winnerId,
        best_of: 5,
      }),
    });
  } catch (err) {
    console.error('recordMatch failed:', err.message);
    throw err;
  }
}

/**
 * Get event ranking
 */
export async function getEventRanking(eventId) {
  try {
    return await apiCall(`/ranking/event/${eventId}`, { method: 'GET' });
  } catch (err) {
    console.error('getEventRanking failed:', err.message);
    throw err;
  }
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
 * Create a tournament
 */
export async function createTournament(eventId, name = 'Test Tournament', tournamentType = 'SINGLE_ELIMINATION') {
  try {
    return await apiCall('/tournaments', {
      method: 'POST',
      body: JSON.stringify({
        event_id: eventId,
        name,
        tournament_type: tournamentType,
        best_of: 1,
        num_groups: 2,
        swiss_rounds: 3,
        allow_draws: false,
      }),
    });
  } catch (err) {
    console.error('createTournament failed:', err.message);
    throw err;
  }
}

/**
 * Delete a tournament
 */
export async function deleteTournament(tournamentId) {
  try {
    return await apiCall(`/tournaments/${tournamentId}`, { method: 'DELETE' });
  } catch (err) {
    console.error(`deleteTournament(${tournamentId}) failed:`, err.message);
    throw err;
  }
}

/**
 * Add participant to tournament
 */
export async function addParticipantToTournament(tournamentId, playerId) {
  try {
    return await apiCall(`/tournaments/${tournamentId}/participants`, {
      method: 'POST',
      body: JSON.stringify({ player_id: playerId }),
    });
  } catch (err) {
    console.error('addParticipantToTournament failed:', err.message);
    throw err;
  }
}

/**
 * Start tournament
 */
export async function startTournament(tournamentId) {
  try {
    return await apiCall(`/tournaments/${tournamentId}/start`, {
      method: 'POST',
      body: JSON.stringify({}),
    });
  } catch (err) {
    console.error('startTournament failed:', err.message);
    throw err;
  }
}

/**
 * Get tournament
 */
export async function getTournament(tournamentId) {
  try {
    return await apiCall(`/tournaments/${tournamentId}`, { method: 'GET' });
  } catch (err) {
    console.error('getTournament failed:', err.message);
    throw err;
  }
}

/**
 * Get tournament bracket
 */
export async function getTournamentBracket(tournamentId) {
  try {
    return await apiCall(`/tournaments/${tournamentId}/bracket`, { method: 'GET' });
  } catch (err) {
    console.error('getTournamentBracket failed:', err.message);
    throw err;
  }
}

/**
 * Clear database by deleting all events
 */
export async function clearTestDatabase() {
  try {
    const events = await getAllEvents();
    if (!Array.isArray(events) || events.length === 0) {
      return;
    }
    
    // Delete events sequentially to avoid race conditions
    for (const event of events) {
      try {
        await deleteTestEvent(event.id);
      } catch (err) {
        console.warn(`Failed to delete event ${event.id}:`, err.message);
      }
    }
  } catch (err) {
    console.warn('Failed to clear database:', err.message);
  }
}
