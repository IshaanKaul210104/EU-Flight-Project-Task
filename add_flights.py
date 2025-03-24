import os
import django
import random
from datetime import datetime, timedelta
from django.utils import timezone

# Tell Django which settings file to use
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flight_project.settings")
django.setup()  # This initializes Django

from flights.models import Airport, Airline, Flight  # Import models AFTER django.setup()

# Fetch all airports
airports = list(Airport.objects.all())
airline1 = Airline.objects.get(name="Lufthansa")
airline2 = Airline.objects.get(name="Eurowings")

for i in range(10):
    departure = random.choice(airports)
    arrival = random.choice(airports)

    while arrival == departure:
        arrival = random.choice(airports)

    # Generate a unique flight number
    while True:
        flight_number = f"LH{random.randint(1000, 9999)}"
        if not Flight.objects.filter(flight_number=flight_number).exists():
            break

    scheduled_departure = timezone.now() + timedelta(hours=i)
    scheduled_arrival = scheduled_departure + timedelta(hours=2)
    actual_departure = scheduled_departure + timedelta(minutes=random.choice([0, 30, 120]))
    actual_arrival = actual_departure + timedelta(hours=2)

    status = "on_time" if actual_departure == scheduled_departure else "delayed"

    Flight.objects.create(
        flight_number=flight_number,
        airline=airline1 if i % 2 == 0 else airline2,
        departure_airport=departure,
        arrival_airport=arrival,
        scheduled_departure=scheduled_departure,
        scheduled_arrival=scheduled_arrival,
        actual_departure=actual_departure,
        actual_arrival=actual_arrival,
        status=status
    )

print("✅ Sample flights added successfully!")