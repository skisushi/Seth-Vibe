"""
Veyant - FastAPI CRUD API for Traveler History.
Run: uvicorn veyant.api:app --reload
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

from .db.database import (
    init_db,
    add_traveler, get_traveler, list_travelers, update_traveler, delete_traveler,
    add_destination, get_destination, list_destinations, update_destination, delete_destination,
    get_or_create_destination,
    add_trip, get_trip, list_trips, get_trips_for_traveler, update_trip, delete_trip,
    get_traveler_preferences,
)

app = FastAPI(title="Veyant", description="Traveler History API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


# ---------- Pydantic schemas ----------

class TravelerIn(BaseModel):
    name: str
    email: str

class TravelerOut(BaseModel):
    id: int
    name: str
    email: str
    created_at: str | None = None

class DestinationIn(BaseModel):
    country: str
    city: str | None = None
    region: str | None = None

class DestinationOut(BaseModel):
    id: int
    country: str
    city: str | None = None
    region: str | None = None

class TripIn(BaseModel):
    traveler_id: int
    destination_id: int
    start_date: str
    end_date: str
    travel_type: str
    accommodation_type: str
    notes: str | None = None

class TripOut(BaseModel):
    id: int
    traveler_id: int
    destination_id: int
    start_date: str
    end_date: str
    duration_days: int | None = None
    travel_type: str
    accommodation_type: str
    notes: str | None = None
    created_at: str | None = None
    country: str | None = None
    city: str | None = None
    region: str | None = None

class PreferencesOut(BaseModel):
    traveler_id: int
    name: str
    email: str
    total_trips: int
    countries_visited: str | None = None
    travel_types: str | None = None
    accommodation_types: str | None = None
    avg_trip_duration_days: float | None = None


# ---------- Travelers ----------

@app.get("/api/travelers", response_model=list[TravelerOut])
def api_list_travelers():
    return [dict(r) for r in list_travelers()]


@app.get("/api/travelers/{traveler_id}", response_model=TravelerOut)
def api_get_traveler(traveler_id: int):
    row = get_traveler(traveler_id)
    if not row:
        raise HTTPException(404, "Traveler not found")
    return dict(row)


@app.post("/api/travelers", response_model=TravelerOut, status_code=201)
def api_create_traveler(body: TravelerIn):
    tid = add_traveler(body.name, body.email)
    return dict(get_traveler(tid))


@app.put("/api/travelers/{traveler_id}", response_model=TravelerOut)
def api_update_traveler(traveler_id: int, body: TravelerIn):
    if not update_traveler(traveler_id, body.name, body.email):
        raise HTTPException(404, "Traveler not found")
    return dict(get_traveler(traveler_id))


@app.delete("/api/travelers/{traveler_id}", status_code=204)
def api_delete_traveler(traveler_id: int):
    if not delete_traveler(traveler_id):
        raise HTTPException(404, "Traveler not found")


# ---------- Destinations ----------

@app.get("/api/destinations", response_model=list[DestinationOut])
def api_list_destinations():
    return [dict(r) for r in list_destinations()]


@app.get("/api/destinations/{destination_id}", response_model=DestinationOut)
def api_get_destination(destination_id: int):
    row = get_destination(destination_id)
    if not row:
        raise HTTPException(404, "Destination not found")
    return dict(row)


@app.post("/api/destinations", response_model=DestinationOut, status_code=201)
def api_create_destination(body: DestinationIn):
    did = get_or_create_destination(body.country, body.city, body.region)
    return dict(get_destination(did))


@app.put("/api/destinations/{destination_id}", response_model=DestinationOut)
def api_update_destination(destination_id: int, body: DestinationIn):
    if not update_destination(destination_id, body.country, body.city, body.region):
        raise HTTPException(404, "Destination not found")
    return dict(get_destination(destination_id))


@app.delete("/api/destinations/{destination_id}", status_code=204)
def api_delete_destination(destination_id: int):
    if not delete_destination(destination_id):
        raise HTTPException(404, "Destination not found")


# ---------- Trips ----------

@app.get("/api/trips", response_model=list[TripOut])
def api_list_trips():
    return [dict(r) for r in list_trips()]


@app.get("/api/trips/{trip_id}", response_model=TripOut)
def api_get_trip(trip_id: int):
    row = get_trip(trip_id)
    if not row:
        raise HTTPException(404, "Trip not found")
    return dict(row)


@app.get("/api/travelers/{traveler_id}/trips", response_model=list[TripOut])
def api_get_traveler_trips(traveler_id: int):
    if not get_traveler(traveler_id):
        raise HTTPException(404, "Traveler not found")
    return [dict(r) for r in get_trips_for_traveler(traveler_id)]


@app.post("/api/trips", response_model=TripOut, status_code=201)
def api_create_trip(body: TripIn):
    if not get_traveler(body.traveler_id):
        raise HTTPException(404, "Traveler not found")
    if not get_destination(body.destination_id):
        raise HTTPException(404, "Destination not found")
    tid = add_trip(
        body.traveler_id, body.destination_id,
        body.start_date, body.end_date,
        body.travel_type, body.accommodation_type, body.notes
    )
    return dict(get_trip(tid))


@app.put("/api/trips/{trip_id}", response_model=TripOut)
def api_update_trip(trip_id: int, body: TripIn):
    if not update_trip(
        trip_id, body.traveler_id, body.destination_id,
        body.start_date, body.end_date,
        body.travel_type, body.accommodation_type, body.notes
    ):
        raise HTTPException(404, "Trip not found")
    return dict(get_trip(trip_id))


@app.delete("/api/trips/{trip_id}", status_code=204)
def api_delete_trip(trip_id: int):
    if not delete_trip(trip_id):
        raise HTTPException(404, "Trip not found")


# ---------- Preferences ----------

@app.get("/api/travelers/{traveler_id}/preferences", response_model=PreferencesOut)
def api_get_preferences(traveler_id: int):
    row = get_traveler_preferences(traveler_id)
    if not row:
        raise HTTPException(404, "Traveler not found")
    return dict(row)
