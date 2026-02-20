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
            "INSERT OR IGNORE INTO travelers (name, email) VALUES (?, ?)",
            (name, email)
        )
        if cur.lastrowid:
            return cur.lastrowid
        row = conn.execute(
            "SELECT id FROM travelers WHERE email = ?", (email,)
        ).fetchone()
        return row["id"]


def get_traveler(traveler_id: int) -> sqlite3.Row | None:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM travelers WHERE id = ?", (traveler_id,)
        ).fetchone()


def list_travelers() -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM travelers ORDER BY id").fetchall()


def update_traveler(traveler_id: int, name: str, email: str) -> bool:
    with get_connection() as conn:
        cur = conn.execute(
            "UPDATE travelers SET name = ?, email = ? WHERE id = ?",
            (name, email, traveler_id)
        )
        return cur.rowcount > 0


def delete_traveler(traveler_id: int) -> bool:
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM travelers WHERE id = ?", (traveler_id,))
        return cur.rowcount > 0


# --- Destinations ---

def add_destination(country: str, city: str = None, region: str = None) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO destinations (country, city, region) VALUES (?, ?, ?)",
            (country, city, region)
        )
        return cur.lastrowid


def get_destination(destination_id: int) -> sqlite3.Row | None:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM destinations WHERE id = ?", (destination_id,)
        ).fetchone()


def list_destinations() -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM destinations ORDER BY country, city").fetchall()


def update_destination(destination_id: int, country: str, city: str = None, region: str = None) -> bool:
    with get_connection() as conn:
        cur = conn.execute(
            "UPDATE destinations SET country = ?, city = ?, region = ? WHERE id = ?",
            (country, city, region, destination_id)
        )
        return cur.rowcount > 0


def delete_destination(destination_id: int) -> bool:
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM destinations WHERE id = ?", (destination_id,))
        return cur.rowcount > 0


def get_or_create_destination(country: str, city: str = None, region: str = None) -> int:
    with get_connection() as conn:
        row = conn.execute(
            """SELECT id FROM destinations
               WHERE country = ?
                 AND (city = ? OR (city IS NULL AND ? IS NULL))
                 AND (region = ? OR (region IS NULL AND ? IS NULL))""",
            (country, city, city, region, region)
        ).fetchone()
        if row:
            return row["id"]
        cur = conn.execute(
            "INSERT INTO destinations (country, city, region) VALUES (?, ?, ?)",
            (country, city, region)
        )
        return cur.lastrowid


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


def get_trip(trip_id: int) -> sqlite3.Row | None:
    with get_connection() as conn:
        return conn.execute(
            """SELECT tr.*, d.country, d.city, d.region
               FROM trips tr
               JOIN destinations d ON d.id = tr.destination_id
               WHERE tr.id = ?""",
            (trip_id,)
        ).fetchone()


def list_trips() -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(
            """SELECT tr.*, d.country, d.city, d.region
               FROM trips tr
               JOIN destinations d ON d.id = tr.destination_id
               ORDER BY tr.start_date DESC"""
        ).fetchall()


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


def update_trip(trip_id: int, traveler_id: int, destination_id: int,
                start_date: str, end_date: str, travel_type: str,
                accommodation_type: str, notes: str = None) -> bool:
    with get_connection() as conn:
        cur = conn.execute(
            """UPDATE trips
               SET traveler_id = ?, destination_id = ?, start_date = ?,
                   end_date = ?, travel_type = ?, accommodation_type = ?, notes = ?
               WHERE id = ?""",
            (traveler_id, destination_id, start_date, end_date,
             travel_type, accommodation_type, notes, trip_id)
        )
        return cur.rowcount > 0


def delete_trip(trip_id: int) -> bool:
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM trips WHERE id = ?", (trip_id,))
        return cur.rowcount > 0


# --- Preferences ---

def get_traveler_preferences(traveler_id: int) -> sqlite3.Row | None:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM traveler_preferences WHERE traveler_id = ?",
            (traveler_id,)
        ).fetchone()


if __name__ == "__main__":
    init_db()
