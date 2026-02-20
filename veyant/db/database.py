"""
Veyant - Traveler History Database
Core database access layer.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "veyant.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Initialize the database by applying schema.sql."""
    with open(SCHEMA_PATH, "r") as f:
        schema = f.read()
    with get_connection() as conn:
        conn.executescript(schema)
    print(f"Database initialized at: {DB_PATH}")


# --- Travelers ---

def add_traveler(name: str, email: str) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO travelers (name, email) VALUES (?, ?)",
            (name, email)
        )
        return cur.lastrowid


def get_traveler(traveler_id: int) -> sqlite3.Row | None:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM travelers WHERE id = ?", (traveler_id,)
        ).fetchone()


# --- Destinations ---

def add_destination(country: str, city: str = None, region: str = None) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO destinations (country, city, region) VALUES (?, ?, ?)",
            (country, city, region)
        )
        return cur.lastrowid


def get_or_create_destination(country: str, city: str = None, region: str = None) -> int:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id FROM destinations WHERE country = ? AND city IS ? AND region IS ?",
            (country, city, region)
        ).fetchone()
        if row:
            return row["id"]
    return add_destination(country, city, region)


# --- Trips ---

def add_trip(
    traveler_id: int,
    destination_id: int,
    start_date: str,
    end_date: str,
    travel_type: str,
    accommodation_type: str,
    notes: str = None
) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO trips
               (traveler_id, destination_id, start_date, end_date,
                travel_type, accommodation_type, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (traveler_id, destination_id, start_date, end_date,
             travel_type, accommodation_type, notes)
        )
        return cur.lastrowid


def get_trips_for_traveler(traveler_id: int) -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(
            """SELECT tr.*, d.country, d.city, d.region
               FROM trips tr
               JOIN destinations d ON d.id = tr.destination_id
               WHERE tr.traveler_id = ?
               ORDER BY tr.start_date DESC""",
            (traveler_id,)
        ).fetchall()


# --- Preferences ---

def get_traveler_preferences(traveler_id: int) -> sqlite3.Row | None:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM traveler_preferences WHERE traveler_id = ?",
            (traveler_id,)
        ).fetchone()


if __name__ == "__main__":
    init_db()
