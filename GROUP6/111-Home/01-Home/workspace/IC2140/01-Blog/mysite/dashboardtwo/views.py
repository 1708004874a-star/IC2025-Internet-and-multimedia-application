# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from  smart_campus.models import SensorData


def dashboard_view(request):
    return render(request, 'dashboardtwo/index.html')

def sensor_data(request):
    sensordata = SensorData.objects.all()
    data=serializers.serialize('json',sensordata)
    return JsonResponse(data, safe=False)