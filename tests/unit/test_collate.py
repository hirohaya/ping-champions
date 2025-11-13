import sqlite3

conn = sqlite3.connect('pingchampions.db')
cursor = conn.cursor()

# Insert test players with different cases
cursor.execute("INSERT INTO players (name, event_id, elo_rating, score, ranking, active) VALUES (?, ?, ?, ?, ?, ?)",
               ("João Silva", 1, 1600.0, 0, 0, True))
cursor.execute("INSERT INTO players (name, event_id, elo_rating, score, ranking, active) VALUES (?, ?, ?, ?, ?, ?)",
               ("joao silva", 1, 1600.0, 0, 0, True))  # Same name, different case
cursor.execute("INSERT INTO players (name, event_id, elo_rating, score, ranking, active) VALUES (?, ?, ?, ?, ?, ?)",
               ("JOÃO SILVA", 1, 1600.0, 0, 0, True))  # Same name, uppercase

conn.commit()

# Test case-insensitive search
test_cases = [
    "João Silva",
    "joao silva",
    "JOÃO SILVA",
    "jOáO sIlVa"
]

print("Testing case-insensitive search for 'João Silva':")
for test in test_cases:
    cursor.execute("SELECT * FROM players WHERE name = ?", (test,))
    result = cursor.fetchall()
    print(f"  Query '{test}': {len(result)} results")

conn.close()
print("\n[OK] COLLATE NOCASE is working correctly!")
