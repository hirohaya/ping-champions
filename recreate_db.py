#!/usr/bin/env pythonimport sys

"""Database recreation utility - drops and recreates the database schema"""import os

sys.path.insert(0, 'backend')

import sys

import os# Remove the database file

import timedb_path = os.path.join(os.getcwd(), 'backend', 'pingchampions.db')



sys.path.insert(0, 'backend')# Close any connections first

from database import engine

# Remove the database fileengine.dispose()

db_path = os.path.join(os.getcwd(), 'backend', 'pingchampions.db')

# Wait a moment

# Close any connections firstimport time

from database import enginetime.sleep(1)

engine.dispose()

# Try to remove the file

# Wait a momentif os.path.exists(db_path):

time.sleep(1)    try:

        os.remove(db_path)

# Try to remove the file        print(f'✓ Removed old database')

if os.path.exists(db_path):    except Exception as e:

    try:        print(f'⚠️  Could not remove: {e}')

        os.remove(db_path)else:

        print(f'✓ Removed old database')    print('✓ Database file does not exist')

    except Exception as e:

        print(f'⚠️  Could not remove: {e}')# Now create fresh database

else:from database import Base

    print('✓ Database file does not exist')from models import Event, Player, Match



# Now create fresh database# Drop all tables and recreate

from database import BaseBase.metadata.drop_all(bind=engine)

from models import Event, Player, Matchprint('✓ Dropped all tables')



# Drop all tables and recreateBase.metadata.create_all(bind=engine)

Base.metadata.drop_all(bind=engine)print('✓ Created fresh database with updated schema')

print('✓ Dropped all tables')

# Verify

Base.metadata.create_all(bind=engine)from sqlalchemy import inspect

print('✓ Created fresh database with updated schema')inspector = inspect(engine)

tables = inspector.get_table_names()

# Verifyprint(f'✓ Tables: {tables}')

from sqlalchemy import inspect

inspector = inspect(engine)for table in tables:

tables = inspector.get_table_names()    cols = inspector.get_columns(table)

print(f'✓ Tables: {tables}')    col_names = [c["name"] for c in cols]

    print(f'  - {table}: {col_names}')

for table in tables:
    cols = inspector.get_columns(table)
    col_names = [c["name"] for c in cols]
    print(f'  - {table}: {col_names}')
