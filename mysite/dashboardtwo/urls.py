from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view),
    path('sensor_data', views.sensor_data, name='sensor_data'),
]