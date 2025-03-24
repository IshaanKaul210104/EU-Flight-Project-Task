import os
import requests
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight_project.settings')
django.setup()

from flights.models import Airport, Airline, Flight

API_KEY = "8b5b8f2b3ab03474ed8b32d791fc5a3e"
API_URL = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}"

def parse_datetime(datetime_str):
    """ Convert ISO datetime string to Django timezone-aware datetime """
    if datetime_str:
        dt = datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            return timezone.make_aware(dt)
        return dt
    return None

def fetch_live_flights():
    response = requests.get(API_URL)
    if response.status_code != 200:
        print("❌ Failed to fetch flight data")
        return

    data = response.json()
    flights = data.get("data", [])

    print(f"✅ Fetched {len(flights)} flights from API")

    for flight in flights:
        flight_number = flight.get("flight", {}).get("iata")

        # ✅ Skip flights with missing flight numbers
        if not flight_number:
            print("❌ Skipping flight due to missing flight number:", flight)
            continue

        departure_airport_code = flight.get("departure", {}).get("iata", "UNKNOWN")
        arrival_airport_code = flight.get("arrival", {}).get("iata", "UNKNOWN")

        if departure_airport_code == "UNKNOWN" or arrival_airport_code == "UNKNOWN":
            print(f"❌ Skipping flight {flight_number} due to missing airport codes")
            continue

        scheduled_departure = parse_datetime(flight.get("departure", {}).get("estimated"))
        scheduled_arrival = parse_datetime(flight.get("arrival", {}).get("estimated"))
        actual_departure = parse_datetime(flight.get("departure", {}).get("actual"))
        actual_arrival = parse_datetime(flight.get("arrival", {}).get("actual"))

        flight_status = flight.get("flight_status", "unknown")

        if not scheduled_departure:
            print(f"❌ Skipping flight {flight_number} due to missing scheduled departure")
            continue

        if not scheduled_arrival:
            scheduled_arrival = scheduled_departure + timedelta(hours=2)

        print(f"Processing flight: {flight_number} | {departure_airport_code} → {arrival_airport_code} | Status: {flight_status}")

        departure_airport, _ = Airport.objects.update_or_create(
            iata_code=departure_airport_code,
            defaults={
                "name": departure_airport_code,
                "latitude": flight.get("departure", {}).get("latitude", 0.0),
                "longitude": flight.get("departure", {}).get("longitude", 0.0),
                "icao_code": flight.get("departure", {}).get("icao", "UNKNOWN")
            }
        )

        arrival_airport, _ = Airport.objects.update_or_create(
            iata_code=arrival_airport_code,
            defaults={
                "name": arrival_airport_code,
                "latitude": flight.get("arrival", {}).get("latitude", 0.0),
                "longitude": flight.get("arrival", {}).get("longitude", 0.0),
                "icao_code": flight.get("arrival", {}).get("icao", "UNKNOWN")
            }
        )

        airline_name = flight.get("airline", {}).get("name", "Unknown Airline")
        airline_iata = flight.get("airline", {}).get("iata")
        airline_icao = flight.get("airline", {}).get("icao")

        if not airline_iata and not airline_icao:
            print(f"❌ Skipping airline for flight {flight_number} due to missing IATA/ICAO code")
            continue

        if not airline_iata:
            airline_iata = "UNKNOWN"
        if not airline_icao:
            airline_icao = "UNKNOWN"

        airline, _ = Airline.objects.update_or_create(
            iata_code=airline_iata,
            icao_code=airline_icao,
            defaults={"name": airline_name}
        )

        flight_obj, created = Flight.objects.update_or_create(
            flight_number=flight_number,
            defaults={
                "airline": airline,
                "departure_airport": departure_airport,
                "arrival_airport": arrival_airport,
                "scheduled_departure": scheduled_departure,
                "scheduled_arrival": scheduled_arrival,
                "actual_departure": actual_departure,
                "actual_arrival": actual_arrival,
                "status": flight_status,
                "source": "live"
            }
        )

        if created:
            print(f"✅ Flight {flight_number} saved successfully!")
        else:
            print(f"🔄 Flight {flight_number} updated!")

    print("✅ Live flights added successfully!")

if __name__ == "__main__":
    fetch_live_flights()