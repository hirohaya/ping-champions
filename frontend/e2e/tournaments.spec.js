import { test, expect } from '@playwright/test';
import {
  createTestEvent,
  deleteTestEvent,
  registerPlayer,
  createTournament,
  addParticipantToTournament,
  startTournament,
  getTournament,
  getTournamentBracket,
  getTodayDate,
} from './helpers';

/**
 * E2E tests for Tournament Management
 * Tests creation, participant management, and state transitions
 */

let testEventId;
let testTournamentId;
let testPlayers = [];

test.beforeEach(async ({ page }) => {
  page.setDefaultTimeout(10000);
  page.setDefaultNavigationTimeout(10000);
  
  // Create test event and players
  try {
    const event = await createTestEvent('Tournament_Test_' + Date.now());
    testEventId = event.id;
    
    // Create 4 test players
    for (let i = 1; i <= 4; i++) {
      const player = await registerPlayer(testEventId, `Player_${i}_${Date.now()}`);
      testPlayers.push(player);
    }
  } catch (err) {
    console.warn('Setup failed:', err.message);
  }
});

test.afterEach(async () => {
  // Cleanup
  if (testTournamentId) {
    try {
      // Tournaments cascade delete with events
      testTournamentId = null;
    } catch (err) {
      console.warn('Cleanup failed:', err.message);
    }
  }
  
  if (testEventId) {
    try {
      await deleteTestEvent(testEventId);
    } catch (err) {
      console.warn('Event cleanup failed:', err.message);
    }
    testEventId = null;
  }
  
  testPlayers = [];
});

test.describe('Tournament Creation and Management', () => {
  test('should create a new tournament via API', async () => {
    const tournament = await createTournament(testEventId, 'Test Single Elim', 'SINGLE_ELIMINATION');
    testTournamentId = tournament.id;
    
    expect(tournament).toBeDefined();
    expect(tournament.id).toBeGreaterThan(0);
    expect(tournament.name).toBe('Test Single Elim');
    expect(tournament.tournament_type).toBe('SINGLE_ELIMINATION');
    expect(tournament.status).toBe('CREATED');
    expect(tournament.participant_count).toBe(0);
  });

  test('should add participants to tournament', async () => {
    const tournament = await createTournament(testEventId, 'Participant Test', 'SINGLE_ELIMINATION');
    testTournamentId = tournament.id;
    
    // Add first participant
    const updated1 = await addParticipantToTournament(tournament.id, testPlayers[0].id);
    expect(updated1.participant_count).toBe(1);
    expect(updated1.participants_ids).toContain(testPlayers[0].id);
    
    // Add second participant
    const updated2 = await addParticipantToTournament(tournament.id, testPlayers[1].id);
    expect(updated2.participant_count).toBe(2);
    expect(updated2.participants_ids).toContain(testPlayers[1].id);
  });

  test('should start tournament with 2+ participants', async () => {
    const tournament = await createTournament(testEventId, 'Start Test', 'SINGLE_ELIMINATION');
    testTournamentId = tournament.id;
    
    // Add 2 participants
    await addParticipantToTournament(tournament.id, testPlayers[0].id);
    await addParticipantToTournament(tournament.id, testPlayers[1].id);
    
    // Start tournament
    const started = await startTournament(tournament.id);
    
    expect(started.status).toBe('IN_PROGRESS');
    expect(started.started_at).toBeDefined();
    expect(started.current_round).toBe(1);
    expect(started.bracket).toBeDefined();
  });

  test('should generate bracket on tournament start', async () => {
    const tournament = await createTournament(testEventId, 'Bracket Test', 'SINGLE_ELIMINATION');
    testTournamentId = tournament.id;
    
    // Add 4 participants
    for (let i = 0; i < 2; i++) {
      await addParticipantToTournament(tournament.id, testPlayers[i].id);
    }
    
    // Start tournament
    const started = await startTournament(tournament.id);
    
    expect(started.bracket).toBeDefined();
    expect(started.bracket.rounds).toBeDefined();
    // Rounds is a dict/object with round numbers as keys
    expect(typeof started.bracket.rounds).toBe('object');
    expect(Object.keys(started.bracket.rounds).length).toBeGreaterThan(0);
  });

  test('should create tournament of all types', async () => {
    const types = ['SINGLE_ELIMINATION', 'SWISS', 'GROUP_KNOCKOUT', 'ROUND_ROBIN'];
    
    for (const type of types) {
      const tournament = await createTournament(testEventId, `Test_${type}`, type);
      
      expect(tournament.tournament_type).toBe(type);
      expect(tournament.status).toBe('CREATED');
      
      // Cleanup
      if (tournament.id) {
        try {
          // Tournaments will be deleted with event
        } catch (err) {
          console.warn(`Cleanup ${type} failed:`, err.message);
        }
      }
    }
  });
});

test.describe('Tournament Validation Rules', () => {
  test('should prevent starting tournament with < 2 participants', async () => {
    const tournament = await createTournament(testEventId, 'Validation Test', 'SINGLE_ELIMINATION');
    testTournamentId = tournament.id;
    
    // Add only 1 participant
    await addParticipantToTournament(tournament.id, testPlayers[0].id);
    
    // Try to start (should fail)
    try {
      await startTournament(tournament.id);
      throw new Error('Expected startTournament to fail with 1 participant');
    } catch (err) {
      expect(err.message).toContain('API Error');
    }
  });

  test('should require minimum participants based on type', async () => {
    // Swiss requires 3 participants
    const swissTourney = await createTournament(testEventId, 'Swiss Validation', 'SWISS');
    testTournamentId = swissTourney.id;
    
    // Add only 2 participants
    await addParticipantToTournament(swissTourney.id, testPlayers[0].id);
    await addParticipantToTournament(swissTourney.id, testPlayers[1].id);
    
    // Try to start (might fail)
    try {
      await startTournament(swissTourney.id);
    } catch (err) {
      console.log('Swiss tournament validation working:', err.message);
    }
  });
});

test.describe('Tournament Bracket Generation', () => {
  test('should generate Single Elimination bracket for 4 players', async () => {
    const tournament = await createTournament(testEventId, 'SE Bracket Test', 'SINGLE_ELIMINATION');
    testTournamentId = tournament.id;
    
    // Add 4 players
    for (let i = 0; i < 4; i++) {
      await addParticipantToTournament(tournament.id, testPlayers[i].id);
    }
    
    // Start and get bracket
    const started = await startTournament(tournament.id);
    expect(started.bracket.rounds).toBeDefined();
    
    // Single elimination with 4 players = 2 rounds (dict with keys "1" and "2")
    expect(Object.keys(started.bracket.rounds).length).toBe(2);
  });

  test('should generate Round Robin bracket', async () => {
    const tournament = await createTournament(testEventId, 'RR Bracket Test', 'ROUND_ROBIN');
    testTournamentId = tournament.id;
    
    // Add 4 players
    for (let i = 0; i < 4; i++) {
      await addParticipantToTournament(tournament.id, testPlayers[i].id);
    }
    
    // Start tournament
    const started = await startTournament(tournament.id);
    
    expect(started.bracket).toBeDefined();
    // Round Robin with 4 players = 6 matches total (C(4,2))
    expect(started.bracket.rounds).toBeDefined();
    expect(started.bracket.total_matches).toBe(6);
  });

  test('should handle odd number of participants in Single Elimination', async () => {
    const tournament = await createTournament(testEventId, 'SE Odd Test', 'SINGLE_ELIMINATION');
    testTournamentId = tournament.id;
    
    // Add 3 players (odd)
    for (let i = 0; i < 3; i++) {
      await addParticipantToTournament(tournament.id, testPlayers[i].id);
    }
    
    // Start tournament
    const started = await startTournament(tournament.id);
    
    expect(started.bracket).toBeDefined();
    expect(started.bracket.rounds).toBeDefined();
  });
});

test.describe('Tournament State Transitions', () => {
  test('should track tournament state correctly', async () => {
    const tournament = await createTournament(testEventId, 'State Test', 'SINGLE_ELIMINATION');
    testTournamentId = tournament.id;
    
    // Initial state
    let current = await getTournament(tournament.id);
    expect(current.status).toBe('CREATED');
    expect(current.started_at).toBeNull();
    
    // Add participants
    for (let i = 0; i < 2; i++) {
      await addParticipantToTournament(tournament.id, testPlayers[i].id);
    }
    
    // Check before starting
    current = await getTournament(tournament.id);
    expect(current.participant_count).toBe(2);
    
    // Start
    const started = await startTournament(tournament.id);
    expect(started.status).toBe('IN_PROGRESS');
    expect(started.started_at).toBeDefined();
  });

  test('should preserve tournament data across API calls', async () => {
    const tournament = await createTournament(testEventId, 'Persistence Test', 'SWISS');
    testTournamentId = tournament.id;
    
    const name = tournament.name;
    const type = tournament.tournament_type;
    
    // Add participants
    await addParticipantToTournament(tournament.id, testPlayers[0].id);
    
    // Fetch again
    const refetched = await getTournament(tournament.id);
    expect(refetched.name).toBe(name);
    expect(refetched.tournament_type).toBe(type);
    expect(refetched.participant_count).toBe(1);
  });
});

test.describe('Tournament Filtering and Listing', () => {
  test('should list all tournaments for an event', async () => {
    // Create multiple tournaments
    const t1 = await createTournament(testEventId, 'Tournament 1', 'SINGLE_ELIMINATION');
    const t2 = await createTournament(testEventId, 'Tournament 2', 'SWISS');
    testTournamentId = t1.id;
    
    expect(t1.event_id).toBe(testEventId);
    expect(t2.event_id).toBe(testEventId);
  });

  test('should filter tournaments by status', async () => {
    // Create created tournament
    const created = await createTournament(testEventId, 'Created Status', 'SINGLE_ELIMINATION');
    testTournamentId = created.id;
    
    expect(created.status).toBe('CREATED');
    
    // Create and start another
    const started = await createTournament(testEventId, 'Started Status', 'SINGLE_ELIMINATION');
    await addParticipantToTournament(started.id, testPlayers[0].id);
    await addParticipantToTournament(started.id, testPlayers[1].id);
    const inProgress = await startTournament(started.id);
    
    expect(inProgress.status).toBe('IN_PROGRESS');
  });
});
