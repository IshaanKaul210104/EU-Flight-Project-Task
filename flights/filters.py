import django_filters
from .models import Flight

class FlightFilter(django_filters.FilterSet):
    departure_airport = django_filters.CharFilter(field_name='departure_airport__iata_code', lookup_expr='iexact')
    arrival_airport = django_filters.CharFilter(field_name='arrival_airport__iata_code', lookup_expr='iexact')
    airline = django_filters.CharFilter(field_name='airline__name', lookup_expr='icontains')
    status = django_filters.CharFilter(field_name='status', lookup_expr='iexact')

    class Meta:
        model = Flight
        fields = ['departure_airport', 'arrival_airport', 'airline', 'status']