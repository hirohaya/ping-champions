"""Add COLLATE NOCASE to player names for case-insensitive search

Revision ID: 9c1f8e3a2b1c
Revises: f4d825fe9491
Create Date: 2025-11-11 10:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c1f8e3a2b1c'
down_revision: Union[str, Sequence[str], None] = 'f4d825fe9491'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Add COLLATE NOCASE to player names."""
    # SQLite: Recreate players table with COLLATE NOCASE on name column
    # This is necessary because SQLite doesn't support modifying column constraints directly
    op.execute("""
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
    op.execute("""
    INSERT INTO players_new 
    SELECT id, name, event_id, elo_rating, score, ranking, active
    FROM players
    """)
    
    # Drop old table
    op.execute("DROP TABLE players")
    
    # Rename new table to original name
    op.execute("ALTER TABLE players_new RENAME TO players")


def downgrade() -> None:
    """Downgrade schema - Remove COLLATE NOCASE from player names."""
    # SQLite: Recreate players table without COLLATE NOCASE on name column
    op.execute("""
    CREATE TABLE players_new (
        id INTEGER NOT NULL, 
        name VARCHAR(100) NOT NULL, 
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
    op.execute("""
    INSERT INTO players_new 
    SELECT id, name, event_id, elo_rating, score, ranking, active
    FROM players
    """)
    
    # Drop old table
    op.execute("DROP TABLE players")
    
    # Rename new table to original name
    op.execute("ALTER TABLE players_new RENAME TO players")
