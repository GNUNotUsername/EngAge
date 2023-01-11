from django.urls import path
from django.contrib.auth import login, authenticate #add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from . import views

urlpatterns = [
    path("api-get-ss",						views.APIGetSS.as_view(),						name = "deprecated"),
    path("api-populate-db",					views.APIPopulateDB.as_view(),					name = "api-populate-db"),
    path("api-aggregate-wellbeing-metrics",	views.APIAggregateWellbeingMetrics.as_view(),	name = "api-aggregate-wellbeing_metrics"),
    path("api-get-area-aggregate",			views.APIGetAreaAggregate.as_view(),			name = "api-get-area-aggregate"),
]
