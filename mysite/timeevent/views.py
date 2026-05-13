from django.shortcuts import render
from .models import Venue, Event
from smart_campus.models import SensorData
from django.db.models import Avg, Q
from datetime import datetime
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

def time_event_data(request):
    venues = Venue.objects.all()
    selected_venues = {}
    error_message = None
    
    if request.method == 'POST':
        venue_ids = request.POST.getlist('venue[]')
        start_datetime_str = request.POST.get('start_datetime')
        end_datetime_str = request.POST.get('end_datetime')
        
        if not venue_ids:
            error_message = "Please select at least one venue."
        elif not start_datetime_str or not end_datetime_str:
            error_message = "Please select both start and end date/time."
        else:
            try:
                start_datetime = timezone.make_aware(datetime.fromisoformat(start_datetime_str))
                end_datetime = timezone.make_aware(datetime.fromisoformat(end_datetime_str))
                
                for venue_id in venue_ids:
                    try:
                        venue = Venue.objects.get(id=venue_id)
                        
                        events = Event.objects.filter(
                            venue=venue
                        ).filter(
                            Q(start_datetime__lt=end_datetime, end_datetime__gt=start_datetime) |
                            Q(start_datetime__exact=start_datetime) |
                            Q(end_datetime__exact=end_datetime)
                        ).order_by('start_datetime')
                        
                        sensors = SensorData.objects.filter(
                            loc=venue.name,
                            date_created__range=[start_datetime, end_datetime]
                        )
                        
                        sensor_count = sensors.count()
                        logger.info(f"Venue: {venue.name}, Sensors found: {sensor_count}")
                        
                        env_data = sensors.aggregate(
                            avg_temperature=Avg('temp'),
                            avg_humidity=Avg('hum'),
                            avg_light=Avg('light'),
                            avg_sound=Avg('snd')
                        )
                        
                        event_environment_data = {}
                        for event in events:
                            
                            event_start = event.start_datetime
                            event_end = event.end_datetime
                            
                            event_sensors = SensorData.objects.filter(
                                loc=venue.name,
                                date_created__range=[event_start, event_end]
                            )
                            
                            event_sensor_count = event_sensors.count()
                            
                            event_env_data = event_sensors.aggregate(
                                avg_temperature=Avg('temp'),
                                avg_humidity=Avg('hum'),
                                avg_light=Avg('light'),
                                avg_sound=Avg('snd')
                            )
                            
                            event_environment_data[event.id] = {
                                'event_name': event.event_name,
                                'start_datetime': event.start_datetime,
                                'end_datetime': event.end_datetime,
                                'sensor_count': event_sensor_count,
                                **event_env_data  
                            }
                        
                        selected_venues[venue] = {
                            'events': events,
                            'env_data': env_data,
                            'sensor_count': sensor_count,
                            'event_environment_data': event_environment_data  
                        }
                        
                    except Venue.DoesNotExist:
                        continue
            
            except ValueError as e:
                error_message = f"Invalid date/time format: {e}. Please use YYYY-MM-DDTHH:MM"
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
                logger.error(f"Error in time_event_data: {str(e)}", exc_info=True)
    
    return render(request, 'timeevent/index.html', {
        'venues': venues,
        'selected_venues': selected_venues,
        'start_datetime': request.POST.get('start_datetime'),
        'end_datetime': request.POST.get('end_datetime'),
        'error_message': error_message,
    })