"""
Remove speech_scripts table
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from sqlalchemy import text
from ai_slides.database.database import engine


def upgrade():
    """Drop speech_scripts table"""
    with engine.connect() as conn:
        try:
            # Drop speech_scripts table
            conn.execute(text("DROP TABLE IF EXISTS speech_scripts"))
            print("Dropped speech_scripts table")
        except Exception as e:
            print(f"Error dropping speech_scripts table: {e}")

        conn.commit()
        print("Speech scripts table removal completed successfully!")


def downgrade():
    """Recreate speech_scripts table"""
    with engine.connect() as conn:
        try:
            # Recreate speech_scripts table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS speech_scripts (
                    id INTEGER PRIMARY KEY,
                    project_id VARCHAR(36) NOT NULL,
                    slide_index INTEGER NOT NULL,
                    slide_title VARCHAR(255) NOT NULL,
                    script_content TEXT NOT NULL,
                    estimated_duration VARCHAR(50),
                    speaker_notes TEXT,
                    generation_type VARCHAR(20) NOT NULL,
                    tone VARCHAR(50) NOT NULL,
                    target_audience VARCHAR(100) NOT NULL,
                    custom_audience TEXT,
                    language_complexity VARCHAR(20) NOT NULL,
                    speaking_pace VARCHAR(20) NOT NULL,
                    custom_style_prompt TEXT,
                    include_transitions BOOLEAN DEFAULT 1 NOT NULL,
                    include_timing_notes BOOLEAN DEFAULT 0 NOT NULL,
                    created_at FLOAT NOT NULL,
                    updated_at FLOAT NOT NULL,
                    FOREIGN KEY (project_id) REFERENCES projects(project_id)
                )
            """))
            print("Recreated speech_scripts table")

            # Recreate indexes
            conn.execute(text("CREATE INDEX IF NOT EXISTS ix_speech_scripts_id ON speech_scripts (id)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS ix_speech_scripts_project_id ON speech_scripts (project_id)"))

            conn.commit()
            print("Speech scripts table recreated successfully!")
        except Exception as e:
            print(f"Error during downgrade: {e}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Remove speech_scripts table migration')
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
