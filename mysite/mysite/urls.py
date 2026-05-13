"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')), #Inlcude app "blog/urls.py"
    path('inventory/', include('inventory.urls')), #Inlcude app "inventory/urls.py"
    path('iot/', include('iot.urls')), #Inlcude app "iot/urls.py"
    path('dashboard/', include('dashboard.urls')),
    path('smart_campus/', include('smart_campus.urls')),
    path('dashboardtwo/', include('dashboardtwo.urls')),
    path('dashboard_2nd/', include('dashboard_2nd.urls')),
    path('timeevent/', include('timeevent.urls')),
    path('checkpoint2/', include('checkpoint2.urls')),
]
