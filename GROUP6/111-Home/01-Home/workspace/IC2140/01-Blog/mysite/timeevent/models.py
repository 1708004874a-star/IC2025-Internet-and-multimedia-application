from django.db import models
from django.utils import timezone
from smart_campus.models import SensorData  

class Venue(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Event(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='events')
    start_datetime = models.DateTimeField()  
    end_datetime = models.DateTimeField()    
    event_name = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.event_name} at {self.venue} on {self.start_datetime}"

class EnvironmentalData(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='environmental_data')
    timestamp = models.DateTimeField(default=timezone.now)
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"Env. data for {self.venue} at {self.timestamp}"    