from django.urls import path
from django.contrib.auth import login, authenticate #add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from . import views

urlpatterns = [
    path('', views.sessioncheck, name='sessioncheck'),
    path('login/', views.login_request, name="login_request"),
    path("create/", views.create, name="create"),
    path("api-create-account/", views.APICreateAccount.as_view(), name="api-create-account")
]
