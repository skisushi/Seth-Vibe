"""
Veyant - Seed sample traveler history data.
Run: python seed.py
"""

from database import init_db, add_traveler, get_or_create_destination, add_trip, get_traveler_preferences

SAMPLE_DATA = [
    {
        "traveler": {"name": "Alex Rivera", "email": "alex@example.com"},
        "trips": [
            {"country": "Japan", "city": "Tokyo", "start": "2024-03-10", "end": "2024-03-20",
             "type": "leisure", "accommodation": "hotel"},
            {"country": "Japan", "city": "Kyoto", "start": "2024-03-20", "end": "2024-03-25",
             "type": "leisure", "accommodation": "hotel"},
            {"country": "Thailand", "city": "Bangkok", "start": "2024-09-01", "end": "2024-09-14",
             "type": "adventure", "accommodation": "airbnb"},
        ]
    },
    {
        "traveler": {"name": "Morgan Lee", "email": "morgan@example.com"},
        "trips": [
            {"country": "France", "city": "Paris", "start": "2024-06-15", "end": "2024-06-22",
             "type": "couple", "accommodation": "hotel"},
            {"country": "Italy", "city": "Rome", "start": "2024-06-22", "end": "2024-06-29",
             "type": "couple", "accommodation": "airbnb"},
            {"country": "USA", "city": "New York", "start": "2024-11-10", "end": "2024-11-13",
             "type": "business", "accommodation": "hotel"},
        ]
    },
    {
        "traveler": {"name": "Jordan Kim", "email": "jordan@example.com"},
        "trips": [
            {"country": "Costa Rica", "city": "San Jose", "start": "2024-01-05", "end": "2024-01-15",
             "type": "adventure", "accommodation": "hostel"},
            {"country": "Peru", "city": "Cusco", "start": "2024-07-20", "end": "2024-08-02",
             "type": "adventure", "accommodation": "hostel"},
            {"country": "New Zealand", "city": "Queenstown", "start": "2024-12-01", "end": "2024-12-15",
             "type": "adventure", "accommodation": "camping"},
        ]
    },
]


def seed():
    init_db()
    print("\nSeeding traveler history...\n")

    for entry in SAMPLE_DATA:
        t = entry["traveler"]
        traveler_id = add_traveler(t["name"], t["email"])
        print(f"Added traveler: {t['name']} (id={traveler_id})")

        for trip in entry["trips"]:
            dest_id = get_or_create_destination(trip["country"], trip["city"])
            add_trip(
                traveler_id=traveler_id,
                destination_id=dest_id,
                start_date=trip["start"],
                end_date=trip["end"],
                travel_type=trip["type"],
                accommodation_type=trip["accommodation"]
            )
            print(f"  -> Trip to {trip['city']}, {trip['country']} ({trip['type']})")

        prefs = get_traveler_preferences(traveler_id)
        print(f"  Preferences summary: {dict(prefs)}\n")


if __name__ == "__main__":
    seed()
