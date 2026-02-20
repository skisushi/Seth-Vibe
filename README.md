# Veyant - Traveler History Database

A Python/SQLite tool for managing and querying traveler trip history.

## Running locally with Docker

**Prerequisites:** Docker and Docker Compose installed.

### 1. Initialize the DB and load sample data

```bash
docker compose up --build
```

This seeds the database with 3 sample travelers and their trips.
The SQLite file (`veyant.db`) is created in `veyant/db/` on your host machine and persists between runs.

### 2. Re-run seed (reset data)

```bash
docker compose run --rm veyant python seed.py
```

### 3. Only initialize the schema (no sample data)

```bash
docker compose run --rm veyant python database.py
```

### 4. Open an interactive Python shell

```bash
docker compose run --rm veyant python
```

Then import and use the library:

```python
from database import init_db, get_traveler, get_trips_for_traveler
init_db()
trips = get_trips_for_traveler(1)
for t in trips:
    print(dict(t))
```

## Running locally without Docker

No external dependencies - only Python 3.12+ required.

```bash
cd veyant/db
python seed.py      # initialize DB and load sample data
python database.py  # initialize schema only
```

## Project structure

```
veyant/db/
  database.py   - SQLite access layer (travelers, destinations, trips)
  schema.sql    - Table definitions and traveler_preferences view
  seed.py       - Sample data loader
```
