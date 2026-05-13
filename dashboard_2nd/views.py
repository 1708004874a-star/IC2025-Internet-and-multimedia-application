from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from sensor.models import sensor
from django.db.models import Avg, Max, Min

def index(request):
    return render(request, 'dashboard_2nd/index.html')
# Create your views here.
def temp_data(request):
    events = sensor.objects.all()
    data = serializers.serialize('json', events) #Translating Django models into JSON formats
    return JsonResponse(data, safe=False)
def summary(request):
    # 1. Get all sensor data
    sensor_data = sensor.objects.all()
    
    # 2. Calculate summary statistics
    summary = sensor.objects.aggregate(
        avg_temp=Avg('temp'),
        max_temp=Max('temp'),
        min_temp=Min('temp')
    )
    
    # 3. Prepare context for template
    context = {
        'sensor_data': sensor_data,
        'summary': summary
    }
    return render(request, 'dashboard_2nd/summary.html', context)