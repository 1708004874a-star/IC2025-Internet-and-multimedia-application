from django.urls import path
from . import views

urlpatterns = [
    path('', views.time_event_data),
]