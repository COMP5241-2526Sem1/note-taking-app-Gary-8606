#!/usr/bin/env python3
"""
Migration script to add order_index column to existing notes
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

import sqlite3

def migrate_database():
    # Path to the database
    ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.path.join(ROOT_DIR, 'database', 'app.db')
    
    print(f"Migrating database at: {DB_PATH}")
    
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if order_index column already exists
        cursor.execute("PRAGMA table_info(note)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'order_index' in columns:
            print("order_index column already exists. No migration needed.")
            return
        
        print("Adding order_index column to note table...")
        
        # Add the order_index column with default value 0
        cursor.execute("ALTER TABLE note ADD COLUMN order_index INTEGER DEFAULT 0")
        
        # Get all existing notes ordered by updated_at desc (current default order)
        cursor.execute("SELECT id FROM note ORDER BY updated_at DESC")
        note_ids = [row[0] for row in cursor.fetchall()]
        
        # Update each note with its index position
        for index, note_id in enumerate(note_ids):
            cursor.execute("UPDATE note SET order_index = ? WHERE id = ?", (index, note_id))
        
        conn.commit()
        print(f"Migration completed successfully. Updated {len(note_ids)} notes.")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()