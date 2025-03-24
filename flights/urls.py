from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AirportViewSet, AirlineViewSet, FlightViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'airports', AirportViewSet)
router.register(r'airlines', AirlineViewSet)
router.register(r'flights', FlightViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Includes all API routes
]