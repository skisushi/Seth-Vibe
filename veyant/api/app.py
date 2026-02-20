"""
Veyant - REST API
Flask server exposing traveler/trip/destination endpoints.

Run:
    cd veyant/api
    python app.py
"""

import sys
import os

# Make the db package importable from this directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from flask import Flask, jsonify, request
from flask_cors import CORS
from db.database import (
    init_db,
    get_connection,
    add_traveler,
    get_traveler,
    get_or_create_destination,
    add_trip,
    get_trips_for_traveler,
    get_traveler_preferences,
)

app = Flask(__name__)
CORS(app)


# ---------------------------------------------------------------------------
# Travelers
# ---------------------------------------------------------------------------

@app.route("/api/travelers", methods=["GET"])
def list_travelers():
    """Return all travelers ordered by most recently added."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM travelers ORDER BY created_at DESC"
        ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/travelers", methods=["POST"])
def create_traveler():
    """Add a new traveler. Body: {name, email}"""
    data = request.get_json() or {}
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "name and email are required"}), 400
    try:
        traveler_id = add_traveler(data["name"], data["email"])
    except Exception as exc:
        return jsonify({"error": str(exc)}), 409
    traveler = get_traveler(traveler_id)
    return jsonify(dict(traveler)), 201


@app.route("/api/travelers/<int:traveler_id>", methods=["GET"])
def get_traveler_detail(traveler_id):
    """Return a single traveler by id."""
    traveler = get_traveler(traveler_id)
    if not traveler:
        return jsonify({"error": "Traveler not found"}), 404
    return jsonify(dict(traveler))


# ---------------------------------------------------------------------------
# Trips
# ---------------------------------------------------------------------------

@app.route("/api/travelers/<int:traveler_id>/trips", methods=["GET"])
def get_traveler_trips(traveler_id):
    """Return all trips for a traveler, newest first."""
    trips = get_trips_for_traveler(traveler_id)
    return jsonify([dict(t) for t in trips])


@app.route("/api/trips", methods=["POST"])
def create_trip():
    """
    Add a new trip.
    Body: {traveler_id, country, city?, region?, start_date, end_date,
           travel_type, accommodation_type, notes?}
    """
    data = request.get_json() or {}
    required = ["traveler_id", "country", "start_date", "end_date",
                "travel_type", "accommodation_type"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    dest_id = get_or_create_destination(
        data["country"],
        data.get("city") or None,
        data.get("region") or None,
    )
    try:
        trip_id = add_trip(
            traveler_id=data["traveler_id"],
            destination_id=dest_id,
            start_date=data["start_date"],
            end_date=data["end_date"],
            travel_type=data["travel_type"],
            accommodation_type=data["accommodation_type"],
            notes=data.get("notes") or None,
        )
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({"id": trip_id}), 201


# ---------------------------------------------------------------------------
# Preferences (analytics view)
# ---------------------------------------------------------------------------

@app.route("/api/travelers/<int:traveler_id>/preferences", methods=["GET"])
def get_preferences(traveler_id):
    """Return the aggregated preference summary for a traveler."""
    prefs = get_traveler_preferences(traveler_id)
    if not prefs:
        return jsonify({"error": "Not found"}), 404
    return jsonify(dict(prefs))


# ---------------------------------------------------------------------------
# Destinations
# ---------------------------------------------------------------------------

@app.route("/api/destinations", methods=["GET"])
def list_destinations():
    """Return all known destinations."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM destinations ORDER BY country, city"
        ).fetchall()
    return jsonify([dict(r) for r in rows])


# ---------------------------------------------------------------------------
# Seed (dev helper)
# ---------------------------------------------------------------------------

@app.route("/api/seed", methods=["POST"])
def seed_database():
    """Populate the database with sample traveler data."""
    import importlib.util, pathlib
    seed_path = pathlib.Path(__file__).parent.parent / "db" / "seed.py"
    spec = importlib.util.spec_from_file_location("seed", seed_path)
    seed_mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(seed_mod)
        seed_mod.seed()
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
    return jsonify({"message": "Database seeded successfully"}), 200


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import os as _os
    init_db()
    host  = _os.environ.get("FLASK_HOST",  "127.0.0.1")
    port  = int(_os.environ.get("FLASK_PORT",  "5000"))
    debug = _os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    print(f"Veyant API running at http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)
