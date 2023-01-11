from django.urls import path
from django.contrib.auth import login, authenticate #add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("token-request/", obtain_auth_token, name="token-request"),
    path("auth-test/",  views.AuthTest.as_view(), name="auth-test"),
    path("api-change-password/", views.APIChangePassword.as_view(), name="api-change-password")
]
