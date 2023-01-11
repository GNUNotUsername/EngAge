from django.shortcuts				import render
from django.http					import HttpResponse, JsonResponse
from django							import forms
from django.contrib.auth.forms		import UserCreationForm
from django.contrib.auth			import get_user_model, login
from django.contrib					import messages
from django.shortcuts				import redirect
from django.contrib.auth			import login, authenticate #add this
from django.contrib					import messages
from django.contrib.auth.forms		import AuthenticationForm
from rest_framework.parsers			import JSONParser
from rest_framework.views			import APIView
from rest_framework.response		import Response
from rest_framework.permissions		import IsAuthenticated
from django.views.decorators.csrf	import csrf_exempt
from modules.constants				import INTERESTS
from events.models					import Interests, Events, Attending
from account.models					import Message, PendingContact, UserInterests, Notifications, LastCheckins, PersonalInfo, Contact
from django.db.models				import Q
from django.contrib.auth.models		import AbstractUser, User
from math							import asin, cos, sin,	sqrt
from datetime						import datetime, timedelta

from events.models					import Events, EventProviders, StateSuburbs, EventInterests, TransportProviders, TransportCoverage
from modules.constants				import EARTH_RADIUS

ERROR_INVALID	= Response({"error": "invalid_request"})
ERROR_NOTFOUND	= Response({"error": "not_found"})

# TODO HOFF DOCUMENT THESE

class APIFetchInterests(APIView):
    #permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {}
        for interest in Interests.objects.all():
            content[interest.interest_id] = interest.interest
        return Response(content)

class APIFetchLastCheckin(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {}
        id_counter = 0
        user = request.user
        try:
            last_checkin = LastCheckins.objects.get(user = user)
        except:
            return ERROR_NOTFOUND
        content[id_counter] = last_checkin.login
        return Response(content)

class APIFetchContacts(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {}
        id_counter = 0
        user = request.user
        for contact in Contact.objects.filter(contact_user_1=user):
            content[id_counter] = contact.contact_user_2.email
            id_counter += 1
        for contact in Contact.objects.filter(contact_user_2=user):
            content[id_counter] = contact.contact_user_1.email
            id_counter += 1
        return Response(content)

class APIFetchEventProviders(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = request.user
        content = {}
        id_counter = 0
        for provider in EventProviders.objects.all():
            content[id_counter] = [provider.PID, provider.name, provider.org_type, provider.email, int(str(provider.phone)), provider.location.state, provider.location.suburb]
        return Response(content)

class APIFetchAttendStatus(APIView):
	"""Determine if a user is attending an event

	GET
	event_id	- the ID of the event to query

	return:
		attending		- True iff attending, else False
		invalid_request	- missing event_id field in request
		not_found		- event does not exist
	"""

	#permission_classes = (IsAuthenticated,)
	def get(self, request):
		try:
			uname = request.GET.get("username")
			user = User.objects.filter(username = uname)[0]
		except:
			user	= request.user
		content	= {"attending": False}
		try:
			event_id = int(request.GET.get("event_id"))
		except:
			return ERROR_INVALID
		try:
			event = Events.objects.filter(event_id = event_id)[0]
		except:
			return ERROR_NOTFOUND
		attendance = list(Attending.objects.filter(attending_user = user, attending_event = event))
		if len(attendance):
			content["attending"] = True
		return Response(content)

class APIFetchAttendingEvents(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = request.user
        content = {}
        id_counter = 0
        for attending in Attending.objects.filter(attending_user=user):
            content[id_counter] = [attending.event.name, attending.event.location, attending.event.event_time]
        return Response(content)

class APIFetchAvailableEvents(APIView):
	#permission_classes = (IsAuthenticated,)
	def get(self, request):
		#user = request.user
		#try:
		#	uname = request.GET.get("username")
		#	user = User.objects.filter(username = uname)[0]
		#except:
		user = request.user
			#return Response({"no_user": uname})
		try:
			n_events = int(request.GET.get("n_events"))
		except:
			return ERROR_INVALID
		try:
			details = PersonalInfo.objects.filter(user = user)[0]
			#details = PersonalInfo.objects.filter(user = user)#.first()
			#u_dets	= details[0]
		except:
			return Response({"error_nodetails": user.username})# len(details)})
		radius		= details.travel_dist
		user_suburb	= details.SSID
		try:
			u_interests	= set([u.interest.interest for u in UserInterests.objects.filter(user = user)])
		except:
			return Response({"error_missingui"})
		no_user_ints = len(u_interests)

		cands = []
		for event in Events.objects.all():
			event_suburb = event.SSID
			dist = ss_distance(user_suburb, event_suburb)
			if dist <= radius:
				cands.append(event)

		if cands == []:
			return Response({"error_nothing"})

		ranks = []
		for c in cands:
			try:
				event_qs = EventInterests.objects.filter(event = c)
				cand_interests = set([i.interest.interest for i in event_qs])
			except:
				return Response({"error_missingei": (c.name, len(event_qs))})
			overlap	= cand_interests.intersection(u_interests)
			sim	= 0
			if no_user_ints:
				sim	= (len(overlap) / no_user_ints)
			ranks.append((sim, c))
		ranks.sort(key = lambda r: r[0])
		ranks.reverse()
		if n_events > len(ranks):
			n_events = len(ranks)
		out = [(r.event_id, r.name, r.address, r.start_time, r.description) for _, r in ranks[:n_events]]
		return Response(out)

class APIFetchProviderCaters(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {}
        id_counter = 0
        try:
            cater_provider = request.GET.get("cater_provider")
        except:
            return ERROR_INVALID
        cater_provider_obj = TransportProviders.objects.get(cater_provider=cater_provider)
        if not cater_provider_obj.exists():
            return ERROR_NOTFOUND
        for cater_provides in ProviderCaters.objects.filter(cater_provider=cater_provider_obj):
            content[id_counter] = cater_provides.cater_caters
        return content

class APIFetchTransportCoverage(APIView):
	# TODO DELETE ME
	#permission_classes = (IsAuthenticated,)
	def get(self, request):
		#id_counter = 0
		#try:
		#    tid = int(request.GET.get("tid"))
		#except:
		#    return ERROR_INVALID
		transport_coverage = list(TransportCoverage.objects.all())
		if len(transport_coverage) == 0:
			return Response({"all ur providers are hecked"})
		content = {p.TID.TID: [] for p in transport_coverage}
		for p in transport_coverage:
			tid = p.TID.TID
			if tid in content:
				content[tid].append((p.area.SSID, p.area.state, p.area.suburb))
			else:
				content[tid] = [(p.area.SSID, p.area.state, p.area.suburb)]
		for tid in content:
			content[tid].sort()
		return Response(content)

class APIFetchSentPendingContacts(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {}
        user = request.user
        id_counter = 0
        for pending_contact in PendingContact(pending_user_1=user, user_2_conf=False):
            content[id_counter] = pending_contact.pending_user_2.username
            id_counter += 1
        return content

class APIFetchReceivedPendingContacts(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {}
        user = request.user
        for pending_contact in PendingContact(pending_user_2=user):
            content[id_counter] = pending_contact.pending_user_1.username
            id_counter += 1
        return content

class APIFetchUserInterests(APIView):
	#permission_classes = (IsAuthenticated,)
	def get(self, request):
		content = {}
		try:
			uname = request.GET.get("username")
			user = User.objects.filter(username = uname)[0]
		except:
			user = request.user
		try:
			user_interests = list(UserInterests.objects.filter(user = user))
		except:
			return Response({"error_missingui": uname})
		interests = {ui.interest.interest_id: ui.interest.interest for ui in user_interests}
		return Response(interests)

class APIFetchOrderedMessages(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {}
        msg_index = 0
        user = request.user
        print(request.GET)
        try:
            start_date = request.GET.get("start_date")
        except:
            return ERROR_INVALID
        if start_date is None:
            start_date = "1970-01-01"
        message_history = Message.objects.filter(recipient=user, timestamp__gte=start_date).order_by('-timestamp')
        for message in message_history:
            content[f"{message.sender}~{message.timestamp}"] = [message.timestamp, message.sender.email, message.recipient.email, message.content]
            msg_index += 1
        return Response(content)

class APIFetchUserMessageHistory(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {}
        msg_index = 0
        user = request.user
        print(request.GET)
        try:
            user_2_username = request.GET.get("user_2")
            start_date = request.GET.get("start_date")
        except:
            return ERROR_INVALID
        try:
            user_2 = User.objects.get(username=user_2_username)
        except:
            return ERROR_NOTFOUND
        message_history = Message.objects.filter(Q(sender=user, recipient=user_2, timestamp__gte=start_date) | Q(sender=user_2, recipient=user, timestamp__gte=start_date))
        for message in message_history:
            content[msg_index] = [message.timestamp, message.sender.email, message.recipient.email, message.content]
            msg_index += 1
        return Response(content)

class APIFetchUsers(APIView):
	"""TODO DELETE ME"""
	def get(self, request):
		optus = [u.username for u in User.objects.all()]
		return Response(optus)

class APIFetchNotifications(APIView):
	"""Pull notifications for a user.

	GET
	username		- the user whose notifications to pull

	return:
		timestamp	- timestamp of notification
		type		- class of notification
		text		- text body of notification
		link_event	- ID of relevant event
		link_user	- ID of relevant user

		not_found	- user does not exist
	"""

	permission_classes = (IsAuthenticated,)
	def get(self, request):
		user = request.user
		notifs	= Notifications.objects.filter(recipient = user)
		content	= []
		for n in notifs:
			names	= ["timestamp", "content", "type", "link_event", "link_user"]
			link_uname = ""
			if n.link_user is not None:
				link_uname = n.link_user.username
			link_eid = ""
			if n.link_event is not None:
				link_eid = n.link_event.event_id
			vals	= [n.timestamp, n.content, n.notif_type, link_eid, link_uname]
			add		= dict(zip(names, vals))
			content.append(add)
		content.reverse()
		return Response(content)

class APIViewAllSSIDs(APIView):
	"""TODO DELETE THIS LATER"""
	#permission_classes = (IsAuthenticated,)
	def get(self, request):
		out = StateSuburbs.objects.all()
		ssids = [(ss.SSID, ss.state, ss.suburb) for ss in out]
		#results = dict(zip(ssids, out))
		return Response([len(ssids)] + ssids)

class APIFetchEventInfo(APIView):
	"""Fetch info of event with given ID.

	GET
	event_id	- ID of event to pull info of

	return:
		name		- name of event
		address		- street address of event
		start_time	- event start time
		end_tim		- event end time

		invalid_request	- missing event_id field
		not_found		- event ID does not exist.
	"""

	#permission_classes = (IsAuthenticated,)
	def get(self, request):
		try:
			event_id = request.GET.get("event_id")
		except:
			return ERROR_INVALID
		try:
			event_info = Events.objects.filter(event_id=event_id)[0]
		except:
			return ERROR_NOTFOUND
		#return Response({event_id: [event_info.name, event_info.address, event_info.start_time, event_info.end_time, event_info.description]})
		return Response([event_id, event_info.name, event_info.address, event_info.start_time, event_info.description])

class APIFetchTransportReccomendations(APIView):
	"""Receive a list of transport providers
	who can transport the given user to the given event.

	GET
	username	- email address of user being transported
	event_id	- ID of event being attended

	return:
		provider ID
		provider name
		provider booking link
		provider booking phone number
	"""

	#permission_classes = (IsAuthenticated,)
	def get(self, request):
		try:
			username = request.GET.get("username")
			user = User.objects.filter(username = username)[0]
		except:
			user = request.user
		try:
			event_id	= int(request.GET.get("event_id"))
		except:
			return ERROR_INVALID
		try:
			event = Events.objects.filter(event_id = event_id)[0]
		except:
			return ERROR_NOTFOUND
		try:
			user_details = PersonalInfo.objects.filter(user = user)[0]
		except:
			return Response({"error_missingui": user.username})
		event_ssid	= event.SSID
		user_ssid	= user_details.SSID
		dist		= ss_distance(event_ssid, user_ssid)
		providers	= TransportProviders.objects.all()
		cands = []
		for p in providers:
			coverage = set([c.area for c in TransportCoverage.objects.filter(TID = p)])
			if event_ssid in coverage and user_ssid:
				cands.append([p.TID, p.name, p.booking_link, str(p.booking_phone)])

		return Response(cands)

def fetchbase(_):
    return HttpResponse("FetchBase")

def ss_distance(ss1, ss2):
	"""Find Euclidean distance between two suburbs.

	Should use haversine distance but this is easier and Earth's curvature
	won't cause any significant differences at this scale
	(unless people are travelling across the entire country)
	but no one's gonna do that

	ss1		- SSID entry of first suburb
	ss2		- SSID entry of second suburb

	return	- <float> Haversine distance between the suburbs
	"""

	lat_1, lat_2	= ss1.latit, ss2.latit
	d_lats			= abs(lat_1 - lat_2)
	d_longs			= abs(ss1.longit - ss2.longit)

	"""
	# Formula from https://www.omnicalculator.com/other/latitude-longitude-distance
	haversine		= 2 * EARTH_RADIUS * asin(sqrt(
						((sin(d_lats) ** 2) / 2) +
						(cos(lat_1) * cos(lat_2) *
						((sin(d_longs) ** 2) / 2))))
	lol that didn't work
	"""

	return ((d_lats ** 2) + (d_longs ** 2)) ** 0.5
	#return haversine
