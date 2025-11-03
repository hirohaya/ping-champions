import sys
import os
sys.path.insert(0, 'backend')

# Remove the database file
db_path = os.path.join(os.getcwd(), 'backend', 'pingchampions.db')

# Close any connections first
from database import engine
engine.dispose()

# Wait a moment
import time
time.sleep(1)

# Try to remove the file
if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print(f'✓ Removed old database')
    except Exception as e:
        print(f'⚠️  Could not remove: {e}')
else:
    print('✓ Database file does not exist')

# Now create fresh database
from database import Base
from models import Event, Player, Match

# Drop all tables and recreate
Base.metadata.drop_all(bind=engine)
print('✓ Dropped all tables')

Base.metadata.create_all(bind=engine)
print('✓ Created fresh database with updated schema')

# Verify
from sqlalchemy import inspect
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f'✓ Tables: {tables}')

for table in tables:
    cols = inspector.get_columns(table)
    col_names = [c["name"] for c in cols]
    print(f'  - {table}: {col_names}')
