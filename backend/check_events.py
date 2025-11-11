import sqlite3

conn = sqlite3.connect('pingchampions.db')
cursor = conn.cursor()

# Check if event 39 exists
cursor.execute("SELECT * FROM events WHERE id = 39")
result = cursor.fetchone()

if result:
    print(f"[OK] Event 39 exists:")
    print(f"  ID: {result[0]}")
    print(f"  Name: {result[1]}")
    print(f"  Date: {result[2]}")
    print(f"  Time: {result[3]}")
    print(f"  Active: {result[4]}")
else:
    print("[ERROR] Event 39 does not exist")

# List all events
print("\nAll events in database:")
cursor.execute("SELECT id, name, active FROM events ORDER BY id DESC LIMIT 10")
events = cursor.fetchall()
for event in events:
    status = "Active" if event[2] else "Inactive"
    print(f"  ID: {event[0]}, Name: {event[1]}, Status: {status}")

conn.close()
