from django.shortcuts import render
from .models import SensorData
from django.db.models import Avg, Count, Max
from django.utils import timezone
from datetime import timedelta
from . import mqtt_handler


def index(request):
    
    location = request.GET.get('location', '')
    node_id = request.GET.get('node_id', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    
    
    sensor_data = SensorData.objects.all().order_by("-date_created")
    
    
    if location:
        sensor_data = sensor_data.filter(loc=location)
    
    if node_id:
        sensor_data = sensor_data.filter(node_id=node_id)
    
    if start_date:
        sensor_data = sensor_data.filter(date_created__gte=start_date)
    
    if end_date:
        sensor_data = sensor_data.filter(date_created__lte=end_date)
    
    
    locations = SensorData.objects.order_by('loc').values_list('loc', flat=True).distinct()
    node_ids = SensorData.objects.order_by('node_id').values_list('node_id', flat=True).distinct()
    
    
    stats = {
        'avg_temp': sensor_data.aggregate(avg=Avg('temp'))['avg'] or 0,
        'avg_hum': sensor_data.aggregate(avg=Avg('hum'))['avg'] or 0,
        'avg_light': sensor_data.aggregate(avg=Avg('light'))['avg'] or 0,
        'avg_snd': sensor_data.aggregate(avg=Avg('snd'))['avg'] or 0,
        'total_nodes': SensorData.objects.values('node_id').distinct().count(),
        'total_locations': SensorData.objects.values('loc').distinct().count(),
    }
    
    
    context = {
        "sensor_data": sensor_data[:100],  
        "locations": locations,
        "node_ids": node_ids,
        "stats": stats,
        "selected_location": location,
        "selected_node_id": node_id,
        "selected_start_date": start_date,
        "selected_end_date": end_date,
    }
    
    return render(request, "smart_campus/index.html", context)

def sensor_data(request):
    sensordata = SensorData.objects.all()
    data = serializers.serialize('json', sensordata) #Translating Django models into JSON formats
    return JsonResponse(data, safe=False) #Returns a string that contains an array object