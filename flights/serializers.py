from rest_framework import serializers
from .models import Airport, Airline, Flight

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'  # Returns all fields in JSON

class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = '__all__'

class FlightSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()  # ✅ Added duration field

    class Meta:
        model = Flight
        fields = "__all__"

    def get_duration(self, obj):
        """Calculate flight duration in minutes"""
        if obj.scheduled_departure and obj.scheduled_arrival:
            duration = obj.scheduled_arrival - obj.scheduled_departure
            return duration.total_seconds() // 60  # Return minutes
        return None  # Return None if data is missing