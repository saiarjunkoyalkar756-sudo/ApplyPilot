import sqlite3
import os

# Use a robust path for the database
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the SQLite database with required tables."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Jobs Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT,
            salary TEXT,
            description TEXT,
            url TEXT UNIQUE,
            posting_date TEXT,
            match_score REAL,
            status TEXT DEFAULT 'new',
            applied_date TEXT
        )
    ''')

    # Applications Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            applied_date TEXT,
            resume_version TEXT,
            status TEXT DEFAULT 'Applied',
            notes TEXT,
            FOREIGN KEY (job_id) REFERENCES jobs (id)
        )
    ''')

    conn.commit()
    conn.close()

def add_job(job_data):
    """Adds a new job to the database or ignores if URL already exists."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO jobs (title, company, location, salary, description, url, posting_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            job_data.get('title'),
            job_data.get('company'),
            job_data.get('location'),
            job_data.get('salary'),
            job_data.get('description'),
            job_data.get('url'),
            job_data.get('posting_date')
        ))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def update_job_score(job_id, score):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE jobs SET match_score = ? WHERE id = ?', (score, job_id))
    conn.commit()
    conn.close()

def record_application(job_id, resume_version):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE jobs SET status = "applied" WHERE id = ?', (job_id,))
    cursor.execute('''
        INSERT INTO applications (job_id, applied_date, resume_version)
        VALUES (?, date('now'), ?)
    ''', (job_id, resume_version))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
