import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).with_name('assignments.sqlite3')

SCHEMA = '''
CREATE TABLE IF NOT EXISTS assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    attending_name TEXT NOT NULL,
    resident_name TEXT NOT NULL,
    service TEXT,
    room TEXT,
    UNIQUE(date, attending_name)
);
CREATE TABLE IF NOT EXISTS attendings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attending_name TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    phone TEXT
);
'''

@contextmanager
def connect():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()

def init_db():
    with connect() as c:
        c.executescript(SCHEMA)

def upsert_assignment(a):
    with connect() as c:
        c.execute('''INSERT INTO assignments(date, attending_name, resident_name, service, room)
                     VALUES(?,?,?,?,?)
                     ON CONFLICT(date, attending_name) DO UPDATE SET
                        resident_name=excluded.resident_name,
                        service=excluded.service,
                        room=excluded.room
                 ''', (a.date.isoformat(), a.attending_name, a.resident_name, a.service, a.room))

def upsert_attending(att):
    with connect() as c:
        c.execute('''INSERT INTO attendings(attending_name, email, phone)
                     VALUES(?,?,?)
                     ON CONFLICT(attending_name) DO UPDATE SET
                        email=excluded.email,
                        phone=excluded.phone
                 ''', (att.attending_name, att.email, att.phone))

def get_attending_email(name: str) -> str | None:
    with connect() as c:
        cur = c.execute('SELECT email FROM attendings WHERE attending_name = ?', (name,))
        row = cur.fetchone()
        return row[0] if row else None

def get_assignments_for_date(iso_date: str):
    with connect() as c:
        cur = c.execute('SELECT date, attending_name, resident_name, service, room FROM assignments WHERE date = ?', (iso_date,))
        return cur.fetchall()
