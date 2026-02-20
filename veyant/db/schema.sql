-- Veyant: Traveler History Database
-- Tracks traveler history to identify preferences

CREATE TABLE IF NOT EXISTS travelers (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    email       TEXT UNIQUE NOT NULL,
    created_at  TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS destinations (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    country     TEXT NOT NULL,
    city        TEXT,
    region      TEXT,
    UNIQUE(country, city, region)
);

CREATE TABLE IF NOT EXISTS trips (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    traveler_id         INTEGER NOT NULL REFERENCES travelers(id),
    destination_id      INTEGER NOT NULL REFERENCES destinations(id),
    start_date          TEXT NOT NULL,
    end_date            TEXT NOT NULL,
    duration_days       INTEGER GENERATED ALWAYS AS (
                            CAST((julianday(end_date) - julianday(start_date)) AS INTEGER)
                        ) VIRTUAL,
    travel_type         TEXT CHECK(travel_type IN ('business','leisure','adventure','family','solo','couple')),
    accommodation_type  TEXT CHECK(accommodation_type IN ('hotel','airbnb','hostel','resort','camping','other')),
    notes               TEXT,
    created_at          TEXT DEFAULT (datetime('now'))
);

-- View: traveler preference summary
CREATE VIEW IF NOT EXISTS traveler_preferences AS
SELECT
    t.id                        AS traveler_id,
    t.name,
    t.email,
    COUNT(tr.id)                AS total_trips,
    GROUP_CONCAT(DISTINCT d.country)            AS countries_visited,
    GROUP_CONCAT(DISTINCT tr.travel_type)       AS travel_types,
    GROUP_CONCAT(DISTINCT tr.accommodation_type) AS accommodation_types,
    ROUND(AVG(tr.duration_days), 1)             AS avg_trip_duration_days
FROM travelers t
LEFT JOIN trips tr ON tr.traveler_id = t.id
LEFT JOIN destinations d ON d.id = tr.destination_id
GROUP BY t.id;
