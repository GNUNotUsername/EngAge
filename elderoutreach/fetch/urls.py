from django.urls import path
from django.contrib.auth import login, authenticate #add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from . import views

urlpatterns = [
	path('',									views.fetchbase,									name = 'fetchbase'),
	path('api-fetch-interests',					views.APIFetchInterests.as_view(),					name = "api-fetch-interests"),
	path('api-fetch-contacts',					views.APIFetchContacts.as_view(),					name = "api-fetch-contacts"),
	path('api-fetch-ordered-messages',			views.APIFetchOrderedMessages.as_view(),			name = "api-fetch-ordered-messages"),
	path('api-fetch-last-checkin',				views.APIFetchLastCheckin.as_view(),				name = "api-fetch-last-checkin"),
	path('api-fetch-available-events',			views.APIFetchAvailableEvents.as_view(),			name = "api-fetch-available-events"),
	path('api-fetch-attending-events',			views.APIFetchAttendingEvents.as_view(),			name = "api-fetch-attending-events"),
	path('api-fetch-transport-coverage',		views.APIFetchTransportCoverage.as_view(),			name = "api-fetch-transport-coverage"),
	path('api-fetch-received-pending-contact',	views.APIFetchReceivedPendingContacts.as_view(),	name = "api-fetch-received-pending-contact"),
	path("api-fetch-sent-pending-contact",		views.APIFetchSentPendingContacts.as_view(),		name = "api-fetch-sent-pending-contact"),
	path("api-fetch-event-providers",			views.APIFetchEventProviders.as_view(),				name = "api-fetch-event-providers"),
	path("api-fetch-attend-status",				views.APIFetchAttendStatus.as_view(),				name = "api-fetch-attend-status"),
	path("api-fetch-users",						views.APIFetchUsers.as_view(),						name = "DELETE-ME"),
	path("api-fetch-notifications",				views.APIFetchNotifications.as_view(),				name = "api-fetch-notifications"),
	path("api-fetch-ssids",						views.APIViewAllSSIDs.as_view(),					name = "DELETE-ME"),
	path("api-fetch-event-info", 				views.APIFetchEventInfo.as_view(),					name = "api-fetch-event-info"),
	path("api-fetch-transport-recommendations",	views.APIFetchTransportReccomendations.as_view(),	name = "api-fetch-transport-recommendations"),
	path("api-fetch-user-interests",			views.APIFetchUserInterests.as_view(),				name = "api-fetch-user-interests"),
]
