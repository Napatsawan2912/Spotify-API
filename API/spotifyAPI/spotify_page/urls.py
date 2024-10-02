from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_spotify, name='get_spotify'),
]
