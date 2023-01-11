from django.urls import path
from django.contrib.auth import login, authenticate #add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from . import views

urlpatterns = [
    path("event-registration/", views.event_registration, name='event-registration'),
    path("organiser-registration/", views.organiser_registration, name='organiser-registration'),
    path("transport-provider-registration/", views.transport_provider_registration, name='transport-provider-registration')
]

