import sqlite3

conn = sqlite3.connect('pingchampions.db')
cursor = conn.cursor()

try:
    # Create new players table with COLLATE NOCASE
    cursor.execute("""
    CREATE TABLE players_new (
        id INTEGER NOT NULL, 
        name VARCHAR(100) COLLATE NOCASE NOT NULL, 
        event_id INTEGER NOT NULL, 
        elo_rating FLOAT, 
        score INTEGER, 
        ranking INTEGER, 
        active BOOLEAN,
        PRIMARY KEY (id), 
        FOREIGN KEY(event_id) REFERENCES events (id) ON DELETE CASCADE
    )
    """)
    
    # Copy data from old table to new table
    cursor.execute("""
    INSERT INTO players_new 
    SELECT id, name, event_id, elo_rating, score, ranking, active
    FROM players
    """)
    
    # Drop old table
    cursor.execute("DROP TABLE players")
    
    # Rename new table to original name
    cursor.execute("ALTER TABLE players_new RENAME TO players")
    
    conn.commit()
    print("[OK] Successfully added COLLATE NOCASE to player names")
    
except Exception as e:
    print(f"[ERROR] {e}")
    conn.rollback()

finally:
    conn.close()
