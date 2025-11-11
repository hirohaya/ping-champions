import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('pingchampions.db')
cursor = conn.cursor()

# Create test events
events = [
    ("Championship 2024", "2024-12-25", "19:00"),
    ("Spring Tournament", "2025-03-20", "14:00"),
    ("Summer Games", "2025-06-15", "18:00"),
    ("Fall League", "2025-09-10", "15:00"),
    ("Winter Cup", "2025-12-01", "20:00"),
]

for name, date, time in events:
    cursor.execute(
        "INSERT INTO events (name, date, time, active) VALUES (?, ?, ?, ?)",
        (name, date, time, True)
    )

conn.commit()

# Verify
cursor.execute("SELECT COUNT(*) FROM events")
count = cursor.fetchone()[0]
print(f"[OK] Created {count} test events")

cursor.execute("SELECT id, name, date, time FROM events ORDER BY id")
for row in cursor.fetchall():
    print(f"  Event {row[0]}: {row[1]} ({row[2]} {row[3]})")

conn.close()
