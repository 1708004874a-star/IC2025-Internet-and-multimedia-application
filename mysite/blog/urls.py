from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index',),
    path('blog/', views.blog),
    path('add/', views.add),
]