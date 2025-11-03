#!/usr/bin/env python
"""Database recreation utility"""
import os
import sys
import time
sys.path.insert(0, 'backend')
from database import engine, Base
from models import Event, Player, Match
db_path = os.path.join(os.getcwd(), 'backend', 'pingchampions.db')
engine.dispose()
time.sleep(1)
if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print('[OK] Removed old database')
    except Exception as e:
        print(f'[ERROR] {e}')
else:
    print('[OK] Database file does not exist')
Base.metadata.drop_all(bind=engine)
print('[OK] Dropped all tables')
Base.metadata.create_all(bind=engine)
print('[OK] Created fresh database')
from sqlalchemy import inspect
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f'[OK] Tables: {tables}')
for table in tables:
    cols = inspector.get_columns(table)
    col_names = [c["name"] for c in cols]
    print(f'  - {table}: {col_names}')
