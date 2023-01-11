from django.urls import path
from django.contrib.auth import login, authenticate #add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from . import views

urlpatterns = [
	path("",									views.pushbase,									name = "pushbase"),
	path("api-push-interests/",					views.APIPushInterests.as_view(),				name = "api-push-interests"),
	path("api-push-new-checkin/",				views.APIPushNewCheckin.as_view(),				name = "api-push-new-checkin"),
	path("api-push-pending-contact/",			views.APIPushPendingContact.as_view(),			name = "api-push-pending-contact"),
	path("api-push-confirm-contact/",			views.APIPushConfirmContact.as_view(),			name = "api-push-confirm-contact"),
	path("api-push-new-message/",				views.APIPushNewMessage.as_view(),				name = "api-push-new-message"),
	path("api-push-event-sign-on/",				views.APIPushEventSignOn.as_view(),				name = "api-push-event-sign-on"),
	path("api-push-new-transport-provider/",	views.APIPushNewTransportProvider.as_view(),	name = "api-push-new-transport-provider"),
	path("api-push-new-caters-option/",			views.APIPushNewCatersOption.as_view(),			name = "api-push-new-caters-option"),
	path("api-push-new-event-provider/",		views.APIPushNewEventProvider().as_view(),		name = "api-push-new-event-provider"),
	path("api-push-new-event/",					views.APIPushNewEvent.as_view(),				name = "api-push-new-event"),
	path("DEATH/",								views.KILL_EVERYTHING().as_view(),				name = "DELETE-THIS"),
	path("api-push-user-details/",				views.APIPushUserDetails().as_view(),			name = "api-push-user-details"),
	path("api-push-any-notification/", 			views.APIPushAnyNotification().as_view(),		name = "DELETE-THIS"),
	path("api-fake-friends/", 					views.APIFakeFriends().as_view(),				name = "DELETE-THIS"),
	path("api-push-checkin-pings/",				views.APIPushCheckinPings().as_view(),			name = "api-push-checkin-pings"),
	path("api-push-new-ssid/",					views.APIAddSSID.as_view(),						name = "DELETE-THIS"),
	path("api-set-user-interests/",				views.APISetUserInterests.as_view(),			name = "api-edit-user-interests"),
	path("api-send-recommendations/",			views.APISendRecommendations.as_view(),			name = "api-send-recommendations"),
	path("api-push-upcoming-reminders/",			views.APIPushUpcomingReminders.as_view(),		name = "api-push-upcoming_reminders"),
	path("api-push-dummy-data/",					views.APIPushDummyData.as_view(),				name = "api-push-dummmy-data"),
]
