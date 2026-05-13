from django.contrib import admin

# Register your models here.
# admin.py

from .models import Venue, Event, EnvironmentalData

admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(EnvironmentalData)