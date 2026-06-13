# Create your views here.
from django.shortcuts import render
from .models import SensorData
from . import mqtt_handler


mqtt_handler.client.loop_start()

def index(request):
    sensor_data = SensorData.objects.all().order_by("-date_created")
    context = {"sensor_data": sensor_data}
    return render(request, "checkpoint2/index.html", context)