import sqlite3

conn = sqlite3.connect('pingchampions.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(players)")
columns = cursor.fetchall()
print("Players table columns:")
for col in columns:
    print(f"  {col[1]}: {col[2]}")
conn.close()
