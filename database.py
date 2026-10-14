import sqlite3
from datetime import date
from typing import Optional, List

DB_NAME = "students.db"

def get_db_connection():
    """Establishes a connection to the SQLite database with row factory enabled."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Creates the students table if it doesn't already exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            dob TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            course TEXT,
            address TEXT,
            enrollment_date TEXT
        )
    """)
    conn.commit()
    conn.close()

# Initialize the database table on script import
init_db()
