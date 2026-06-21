import sqlite3
import os

DB_PATH = "verdaterra.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Read schema
    with open("schema.sql", "r") as f:
        cursor.executescript(f.read())
        
    # Read seed data if empty
    cursor.execute("SELECT COUNT(*) FROM facilities")
    if cursor.fetchone()[0] == 0:
        with open("seed_data.sql", "r") as f:
            cursor.executescript(f.read())
            
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    # Ensure running from database directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    init_db()
