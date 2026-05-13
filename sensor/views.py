from django.shortcuts import render
from . import iot_mqtt
from .models import sensor

# Create your views here.
def index(request):
    return render(request, 'sensor/index.html', context)

def alllist(request):
    sensors =sensor.objects.order_by('-date_created') 
    context = {'sensors' : sensors}
    return render(request, 'sensor/alllist.html', context)