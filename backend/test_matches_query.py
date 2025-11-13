#!/usr/bin/env python3
"""Test script to debug matches query"""

import sys
from database import SessionLocal
from models import Match, Event

def test_matches_query():
    db = SessionLocal()
    try:
        # First verify event exists
        event = db.query(Event).filter(Event.id == 7).first()
        if event:
            print(f"✅ Event found: {event.id} - {event.name}")
        else:
            print("❌ Event 7 not found")
            return
        
        # Now query matches
        matches = db.query(Match).filter(Match.event_id == 7).all()
        print(f"✅ Query successful: Found {len(matches)} matches")
        
        for match in matches:
            print(f"  - Match {match.id}: Player {match.player1_id} vs {match.player2_id}, winner: {match.winner_id}")
            
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_matches_query()
