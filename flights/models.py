from django.db import models

# Create your models here.

# Airport Model
class Airport(models.Model):
    name = models.CharField(max_length=255)
    iata_code = models.CharField(max_length=3, unique=True)  # 3-letter airport code
    icao_code = models.CharField(max_length=4, unique=True)  # 4-letter airport code
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.iata_code})"
    
# Airline Model
class Airline(models.Model):
    name = models.CharField(max_length=100)
    iata_code = models.CharField(max_length=10, null=True, blank=True, unique=True)
    icao_code = models.CharField(max_length=10, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name
    
# Flight Model
class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    airline = models.ForeignKey("Airline", on_delete=models.CASCADE)
    departure_airport = models.ForeignKey("Airport", on_delete=models.CASCADE, related_name="departing_flights")
    arrival_airport = models.ForeignKey("Airport", on_delete=models.CASCADE, related_name="arriving_flights")
    scheduled_departure = models.DateTimeField()
    actual_departure = models.DateTimeField(null=True, blank=True)
    scheduled_arrival = models.DateTimeField()
    actual_arrival = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default="unknown")
    source = models.CharField(max_length=10, default="manual")  # ✅ Added this

    def __str__(self):
        return f"{self.flight_number} - {self.departure_airport.iata_code} to {self.arrival_airport.iata_code}"