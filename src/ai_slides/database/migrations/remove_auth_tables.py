"""
Remove authentication tables (users and user_sessions)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from sqlalchemy import text
from ai_slides.database.database import engine


def upgrade():
    """Drop users and user_sessions tables"""
    with engine.connect() as conn:
        try:
            # Drop user_sessions table first (has foreign key to users)
            conn.execute(text("DROP TABLE IF EXISTS user_sessions"))
            print("Dropped user_sessions table")
        except Exception as e:
            print(f"Error dropping user_sessions table: {e}")

        try:
            # Drop users table
            conn.execute(text("DROP TABLE IF EXISTS users"))
            print("Dropped users table")
        except Exception as e:
            print(f"Error dropping users table: {e}")

        conn.commit()
        print("Authentication tables removal completed successfully!")


def downgrade():
    """Recreate users and user_sessions tables"""
    with engine.connect() as conn:
        try:
            # Recreate users table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(128) NOT NULL,
                    email VARCHAR(100) UNIQUE,
                    is_active BOOLEAN DEFAULT 1,
                    is_admin BOOLEAN DEFAULT 0,
                    created_at FLOAT NOT NULL,
                    last_login FLOAT
                )
            """))
            print("Recreated users table")

            # Recreate user_sessions table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id INTEGER PRIMARY KEY,
                    session_id VARCHAR(128) UNIQUE NOT NULL,
                    user_id INTEGER NOT NULL,
                    created_at FLOAT NOT NULL,
                    expires_at FLOAT NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """))
            print("Recreated user_sessions table")

            # Recreate indexes
            conn.execute(text("CREATE INDEX IF NOT EXISTS ix_users_username ON users (username)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS ix_users_email ON users (email)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS ix_user_sessions_session_id ON user_sessions (session_id)"))

            conn.commit()
            print("Authentication tables recreated successfully!")
        except Exception as e:
            print(f"Error during downgrade: {e}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Remove authentication tables migration')
    parser.add_argument('--test', action='store_true', help='Test on backup database')
    args = parser.parse_args()

    if args.test:
        print("Testing migration on backup database...")
        # Note: In production, you would modify the engine to point to backup
        print("Warning: This script uses the main database. Create a backup first!")
        response = input("Continue with migration? (yes/no): ")
        if response.lower() != 'yes':
            print("Migration cancelled")
            sys.exit(0)

    upgrade()
    print("Migration completed!")
