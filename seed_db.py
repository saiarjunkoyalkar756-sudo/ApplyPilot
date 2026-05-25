import sqlite3
import os

DB_PATH = "job-copilot/database.db"

def seed_jobs():
    jobs = [
        {
            "title": "Junior Python Developer",
            "company": "TechInnovate Solutions",
            "location": "Remote",
            "salary": "$80k - $100k",
            "description": "We are looking for a Junior Python Developer to build scalable backend services. Experience with Django, SQLite, and REST APIs is a plus.",
            "url": "https://example.com/jobs/python-dev-1",
            "posting_date": "2026-05-24"
        },
        {
            "title": "Frontend React Engineer",
            "company": "WebFlow Systems",
            "location": "San Francisco, CA",
            "salary": "$110k - $140k",
            "description": "Join our frontend team to build beautiful user interfaces using React.js and Redux. Knowledge of CSS and responsive design is essential.",
            "url": "https://example.com/jobs/react-eng-2",
            "posting_date": "2026-05-23"
        },
        {
            "title": "Full Stack Intern",
            "company": "DataBridge AI",
            "location": "Remote",
            "salary": "Stipend based",
            "description": "As a Full Stack Intern, you will work with Python (Django) and React.js to develop AI-driven dashboards. Great opportunity for students!",
            "url": "https://example.com/jobs/fullstack-intern-3",
            "posting_date": "2026-05-25"
        },
        {
            "title": "Data Analyst (Power BI)",
            "company": "Insights Corp",
            "location": "Remote",
            "salary": "$90k - $110k",
            "description": "Looking for a Data Analyst to create interactive Power BI dashboards and perform SQL-based data analysis.",
            "url": "https://example.com/jobs/data-analyst-4",
            "posting_date": "2026-05-22"
        }
    ]

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Ensure tables exist
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
            status TEXT DEFAULT 'new'
        )
    ''')

    for job in jobs:
        try:
            cursor.execute('''
                INSERT INTO jobs (title, company, location, salary, description, url, posting_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (job['title'], job['company'], job['location'], job['salary'], job['description'], job['url'], job['posting_date']))
            print(f"Added: {job['title']} at {job['company']}")
        except sqlite3.IntegrityError:
            print(f"Skipped (already exists): {job['title']}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed_jobs()
