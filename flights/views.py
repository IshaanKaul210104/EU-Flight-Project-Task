from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import F, Q
from datetime import timedelta
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination  # ✅ Added pagination
from .models import Airport, Airline, Flight
from .serializers import AirportSerializer, AirlineSerializer, FlightSerializer

# ✅ Custom Pagination Class (limits results per page)
class FlightPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50

# Airport API View
class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

# Airline API View
class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    
# Flight API View
class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related("airline", "departure_airport", "arrival_airport").order_by("scheduled_departure")  # ✅ Optimized DB queries
    serializer_class = FlightSerializer
    lookup_field = 'flight_number'
    pagination_class = FlightPagination  # ✅ Enabled pagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    # ✅ Improved filtering (related fields added, case-insensitive search)
    filterset_fields = [
        'departure_airport__iata_code', 'arrival_airport__iata_code',
        'airline__name', 'airline__iata_code', 'status', 'source'
    ]

    # ✅ Enable search by flight number & airport codes
    search_fields = ['flight_number', 'departure_airport__iata_code', 'arrival_airport__iata_code']

    # 🔹 API to get only live flights
    @action(detail=False, methods=['get'])
    def live(self, request):
        live_flights = Flight.objects.filter(source__iexact="live").order_by("scheduled_departure")
        if not live_flights.exists():
            return Response({"message": "No live flights available"}, status=200)

        page = self.paginate_queryset(live_flights)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(live_flights, many=True)
        return Response(serializer.data)

    # 🔹 API to filter only delayed flights
    @action(detail=False, methods=['get'])
    def delayed(self, request):
        delayed_flights = Flight.objects.filter(
            actual_departure__isnull=False,  # ✅ Ensures actual departure is not None
            actual_departure__gt=F('scheduled_departure') + timedelta(hours=2)
        )

        if not delayed_flights.exists():
            return Response({"message": "No delayed flights available"}, status=200)

        page = self.paginate_queryset(delayed_flights)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(delayed_flights, many=True)
        return Response(serializer.data)
