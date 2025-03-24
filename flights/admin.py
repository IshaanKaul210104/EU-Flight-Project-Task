from django.contrib import admin
from .models import Airport, Airline, Flight

# Register your models here.

admin.site.register(Airport)
admin.site.register(Airline)
admin.site.register(Flight)