from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from smart_campus.models import SensorData
from django.db.models import Avg, Max, Min


def dashboard_view(request):
    return render(request, 'dashboardtwo/index.html')


def sensor_data(request):
    sensordata = SensorData.objects.all()
    data = serializers.serialize('json', sensordata)
    return JsonResponse(data, safe=False)


def summary(request):
    sensor_data = SensorData.objects.all()

    summary = SensorData.objects.aggregate(
        avg_temp=Avg('temp'),
        max_temp=Max('temp'),
        min_temp=Min('temp'),
        avg_hum=Avg('hum'),
        avg_light=Avg('light'),
        avg_snd=Avg('snd'),
    )

    context = {
        'sensor_data': sensor_data,
        'summary': summary
    }
    return render(request, 'dashboardtwo/summary.html', context)
