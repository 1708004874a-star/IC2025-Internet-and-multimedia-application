from django.shortcuts import render
# from . import iot_mqtt  # disabled: this module connects to the campus MQTT broker at import time; not needed to view saved data
from .models import Event
# Create your views here.
def index(request):
    events = Event.objects.order_by('-date_created') # date_created descending order
    context = {'events' : events} # Store the data in "context" dictionaries
    return render(request, 'iot/index.html', context) # Pass the context to HTML template