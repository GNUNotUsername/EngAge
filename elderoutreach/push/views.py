from django.shortcuts				import render
from django.http					import HttpResponse, JsonResponse
from django							import forms
from django.contrib.auth.forms		import UserCreationForm
from django.contrib.auth			import get_user_model
from django.contrib.auth			import login
from django.contrib					import messages
from django.shortcuts				import redirect
from django.contrib.auth			import login, authenticate #add this
from django.contrib					import messages
from django.contrib.auth.forms		import AuthenticationForm
from rest_framework.parsers			import JSONParser
from rest_framework.views			import APIView
from rest_framework.response		import Response
from rest_framework.permissions		import IsAuthenticated
from rest_framework.authtoken.views	import obtain_auth_token
from modules.grandom				import gen_woop_state
from events.models					import Interests, CatersOptions, TransportCoverage, TransportProviders, StateSuburbs, EventProviders, Events, EventInterests, Attending
from account.models					import PendingContact, Message, PersonalInfo, Notifications, LastCheckins, UserInterests, Contact
from wellbeing.models import WoopScoreIndividual, EmoteScoreIndividual, WoopScoreSS, WoopScoreState, EmoteScoreSS
from modules.constants				import ADMIN_AUTH, GENESIS
from django.db.models				import Q
from django.contrib.auth.models		import AbstractUser, User

from modules.tree					import SSTREE
from modules.constants				import EARTH_RADIUS

from math							import asin, cos, sin,	sqrt
from datetime						import datetime, timedelta
from requests						import post

from random import randint

ERROR_INVALID	= Response({"error":	"invalid_request"})
ERROR_NOTFOUND	= Response({"error":	"not_found"})
ERROR_SAVEERROR	= Response({"error":	"save_error"})
ERROR_BADAUTH	= Response({"error":	"not_authorized"})
REQ_SUCCESS		= Response({"status":	"success"})

REMIND			= 1
PING_MATES		= 3
TIME_SPLIT		= "%Y-%m-%d %H:%M"
REMIND_TEXT		= "Remember to fill in your wellness check"
PHONE_A_FRIEND	= " hasn't checked in recently. Send a message?"
RECCO_TEXT		= "You may be interested in this event: "
ACCEPT			= "Friend request accepted by "
REJECT			= "Friend request rejected by "
FRIEND_REQ		= "You have a friend request from "
GOOD_WOOPS		= range(6, 31)
GOOD_EMOTES		= range(1, 6)
WEEK			= 7

def pushbase():
    return HttpResponse("PushBase")

def flat_cut(raw, delims):
	"""Split over multiple delimeters and flatten"""
	existing = [raw]
	for d in delims:
		cuts = []
		for e in existing:
			individuals = e.split(d)
			cuts += [j.title() for j in filter(lambda i: i != "", individuals)]
		existing = cuts

	return existing

class APIPushInterests(APIView):
    """TODO HOFF DOCUMENT ME"""
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        if str(request.auth) != ADMIN_AUTH:
            return ERROR_BADAUTH
        try:
            data = request.POST.getlist("interests")
        except:
            return ERROR_INVALID
        for interest in data:
            if Interests.objects.filter(interest=interest).exists():
                continue
            new_interest = Interests(interest=interest)
            try:
                new_interest.save()
            except Exception as e:
                return ERROR_SAVEERROR
        return REQ_SUCCESS

class APIPushNewEvent(APIView):
	"""Add a new event to the events DB.
	Requires existing DB organiser to be registered.

	POST
	event_name	- name of the event to register
	event_pid	- name of the event organiser (previously registered)
	location	- street address, suburb and state of the event venue
	start		- YYYY-MM-DD HH:mm event start time
	end			- YYYY-MM-DD HH:mm event end time
	keywords	- interests associated with this event
	description	- long description of the event

	return:
		success			- event lodged successfully
							- keywords successfully associated with event
		invalid_request	- missing request field
		bad_times		- malformed start or end time string
		invalid_address	- malformed event field
		not_found		- event organiser does not exist
		bad_geography	- suburb not within state
	"""

	#permission_classes = (IsAuthenticated,)
	def post(self, request):
		user = request.user
		try:
			content			= request.POST
			event_name		= content.get("event_name")
			provider_name	= content.get("event_pid")
			event_location	= content.get("location")
			start			= content.get("start_time")
			end				= content.get("end_time")
			keywords		= content.get("keywords")
			description		= content.get("description")
		except:
			return ERROR_INVALID
		try:
			start_time = datetime.strptime(start, TIME_SPLIT)
			end_time = datetime.strptime(end, TIME_SPLIT)
		except:
			return Response({"bad_times": (start, end)})
		try:
			address, suburb, state = tuple(event_location.split(", "))
		except:
			return Response({"invalid_address": address})
		try:
			PID = EventProviders.objects.filter(name = provider_name)[0]
		except:
			return Response({"not_found": provider_name})
		try:
			SSID = StateSuburbs.objects.filter(state = state, suburb = suburb)[0]
		except:
			return Response({"bad_geography": (state, suburb)})
		new_event = Events(name = event_name, PID = PID, address = address, SSID = SSID, start_time = start_time, end_time = end_time, description = description)
		new_event.save()

		keywords = flat_cut(keywords, ", ")
		good_keys = []
		for key in keywords:
			try:
				interest = Interests.objects.filter(interest = key)[0]
				event_keywords = EventInterests(event = new_event, interest = interest)
				event_keywords.save()
				good_keys.append(key)
			except:
				# Either it was a non existent keyword or a duplicate keyword
				# Nothing to worry about either way.
				pass

		return Response({"success": [new_event.event_id, new_event.name] + good_keys})

class APIPushConfirmContact(APIView):
	"""TODO HOFF DOCUMENT ME"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		user = request.user
		try:
			user_1_username	= request.POST.get("user_1")
			user_1			= User.objects.get(username=user_1_username)
			choice			= request.POST.get("choice").lower()
		except:
			return ERROR_INVALID
		if choice not in {"accept", "reject"}:
			return Response({"bad mode": choice})
		pending_contact = PendingContact.objects.filter(pending_user_2=user, pending_user_1=user_1)
		try:
			user_2_name	= PersonalInfo.objects.filter(user = user)[0].real_name
		except:
			return Response({"error_missingui": user.username})
		if not pending_contact.exists():
			return ERROR_NOTFOUND
		if choice == "accept":
			new_contact	= Contact(contact_user_1=user_1, contact_user_2=user)
			new_contact2 = Contact(contact_user_1=user, contact_user_2=user_1)
			accept_msg	= Notifications(recipient = user_1, notif_type = "FA", content = ACCEPT + user_2_name, link_user = user, timestamp = datetime.now())
			try:
				new_contact.save()
				accept_msg.save()
			except:
				return ERROR_SAVEERROR
			pending_contact.delete()
		else:
			pending_contact.delete()
			reject_msg = Notifications(recipient = user_1, notif_type = "FR", content = REJECT + user_2_name, timestamp = datetime.now())
			try:
				reject_msg.save()
			except:
				return ERROR_SAVEERROR
		try:
			request_notif = Notifications.objects.filter(recipient = user, link_user = user_1)[0]
			request_notif.delete()
		except:
			# Somehow the friend request notification has vanished.
			# Just pretend like it's fine
			# because there's too many changes to undo
			pass
		return REQ_SUCCESS

class APIPushUpcomingReminders(APIView):
	#permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			username = request.POST.get("username")
			user = User.objects.filter(username = username)[0]
		except:
			user = request.user
			#return Response({"not_found": username})
		attending = Attending.objects.filter(attending_user = user)
		today = datetime.today().astimezone()
		pings = 0
		for att in attending:
			event = att.attending_event
			#return Response({str(event.start_time)})
			days_rem = (event.start_time.astimezone() - today).days
			if days_rem < WEEK:
				# First check that there isn't an existing reminder
				user_notifs = list(Notifications.objects.filter(recipient = user, notif_type = "UE", link_event = event))
				if not len(user_notifs):
					pings += self._remind(user, event)
				else:
					date = user_notifs[0].timestamp.astimezone()
					days_until = date - today
					if days_until == 1:
						pings += self._remind(user, event)
		return Response({"success": pings})

	def _remind(self, recip, event):
		out = 0
		ping = Notifications(recipient = recip, notif_type = "UE", content = UPCOMING + event.name, link_event = event, timestamp = datatime.now())
		try:
			ping.save()
			out = 1
		except:
			pass
		return out

class APIPushPendingContact(APIView):
	"""TODO HOFF DOCUMENT ME"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		user = request.user
		try:
			user_2_username = request.POST.get("user_2")
		except:
			return ERROR_INVALID
		try:
			user_2 = User.objects.filter(username=user_2_username)[0]
			if user == user_2:
				return Response({"error": "cannot befriend yourself"})
		except:
			return ERROR_NOTFOUND
		try:
			user_2_details = PersonalInfo.objects.filter(user = user_2)[0]
			user_details = PersonalInfo.objects.filter(user = user)[0]
		except:
			return Response({"error_missingui": user_2_username})
		tstamp = datetime.now()
		new_contact = PendingContact(pending_user_1=user, pending_user_2=user_2, user_1_conf=True, user_2_conf=False)
		friend_req_notif = Notifications(recipient = user_2, notif_type = "FQ", content = FRIEND_REQ + user_details.real_name, link_user = user, timestamp = tstamp)
		try:
			friend_req_notif.save()
		except:
			return Response({"save_error": "notification"})
		try:
			new_contact.save()
		except:
			friend_req.delete()
			return ERROR_SAVEERROR
		return REQ_SUCCESS

class APIPushNewTransportProvider(APIView):
	"""Register a new transport provider company.

	POST
	name				- name of company
	booking_link		- link to bookings page
	booking_phone		- phone number for bookings line
	city				- city of operation
	min_discount_age	- minimum age at which seniors discounts are offered
	allow_carers		- whether or not carers are allowed on tranport
	require_med_list	- whether or not a list of medications are required from clients
	cancel_warning		- min number of days' warning required for a cancellation

	return:
		success			- provider was registered successfully
		invalid_request	- missing request field
		save_error		- transport provider could not save to database
		not_found		- invalid city entered
	"""

	#permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			content			= request.POST
			provider_name	= content.get("name")
			booking_link	= content.get("booking_link")
			booking_phone	= content.get("booking_phone")
			provider_city	= content.get("city")
			discount_age	= content.get("min_discount_age")
			allow_carers	= content.get("allow_carers")
			require_meds	= content.get("require_med_list")
			cancel_warning	= content.get("cancel_warning")
		except:
			return ERROR_INVALID
		new_provider = TransportProviders(name = provider_name, booking_link = booking_link, booking_phone = booking_phone, min_discount_age = discount_age, allow_carers = allow_carers, require_med_list = require_meds, min_days_b4_cancel = cancel_warning)
		try:
			new_provider.save()
		except:
			return ERROR_SAVEERROR

		coverage = {}
		for state in SSTREE:
			provider_suburbs		= SSTREE[state].get(provider_city)
			if provider_suburbs is not None:
				suburbs				= list(provider_suburbs)
				coverage[state]		= len(suburbs)
				coverage["done"]	= 0
				coverage["covers"]	= []
				for sub in list(provider_suburbs):
					suburb = sub[0]
					SSID		= StateSuburbs.objects.filter(state = state, suburb = suburb)[0]
					new_cover	= TransportCoverage(TID = new_provider, area = SSID)
					try:
						new_cover.save()
						coverage["covers"].append(SSID.suburb)
						coverage["done"] += 1
					except:
						pass
						# Probably some dual key error from a quirky suburb name.
						# There's enough suburbs for us to safely pretend it doesn't exist.
				break
		if coverage == {}:
			new_provider.delete()
			return ERROR_NOTFOUND

		return Response({"success": new_provider.TID})

class APIPushNewEventProvider(APIView):
	"""Register a new event organiser.

	POST
	name	- name of event organiser
	type	- O for organisation, I for individual
	email	- name of event organiser
	phone	- phone number of event organiser
	state	- state of event organiser
	suburb	- suburb of event organiser

	return:
		success			- organiser addedd successfully
		invalid_request	- missing request field
		not_found		- suburb is not within state
		save_error		- could not save event provider to database
	"""

	#permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			content		= request.POST
			name		= content.get("name")
			org_type	= content.get("type")
			email		= content.get("email")
			phone		= content.get("phone")
			state		= content.get("state")
			suburb		= content.get("suburb")
		except:
			return ERROR_INVALID
		try:
			location = StateSuburbs.objects.filter(state = state, suburb = suburb)[0]
		except:
			return ERROR_NOTFOUND
		new = EventProviders(name = name, org_type = org_type, email = email, phone = phone, location = location)
		try:
			new.save()
		except:
			return ERROR_SAVEERROR

		return REQ_SUCCESS

class KILL_EVERYTHING(APIView):
	"""PROHOBITED GO AWAY"""
	def get(self, request):
		#return Response({"GO AWAY"})
		jedi_temple = [
			#TransportCoverage,
			#TransportProviders,
			#EventInterests,
			#Events,
			#EventProviders,
			#PersonalInfo,
			#Notifications,
			#Contact,
			#LastCheckins,
			#UserInterests,
			PendingContact,
			#WoopScoreIndividual,
			#WoopScoreSS,
			#WoopScoreState,
			#EmoteScoreIndividual,
			#EmoteScoreSS
		]

		for room in jedi_temple:
			for youngling in room.objects.all():
				youngling.delete()
		return Response({"I saw Djanakin... dropping rows..."})

class APIPushNewCatersOption(APIView):
	"""TODO HOFF DOCUMENT ME"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			caters_to = request.POST.get("caters_to")
		except:
			return ERROR_INVALID
		new_caters_option = CatersOptions(caters_to=caters_to)
		new_caters_option.save()

		return REQ_SUCCESS

class APIPushNewProviderCaters(APIView):
    """TODO HOFF DOCUMENT ME"""
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            cater_provider = request.POST.get("cater_provider")
            cater_caters = request.POST.get("cater_caters")
        except:
            return ERROR_INVALID
        new_provider_caters = ProviderCaters(cater_provider=cater_provider, cater_caters=cater_caters)
        new_provider_caters.save()
        return REQ_SUCCESS

class APIPushNewCheckin(APIView):
	"""Send wellbeing data to the wellbeing database

	POST
	username	- email address of user whose wellbeing to send
	woop		- the user's woop score (6-30)
	emote		- the user's emoji score (1-5)

	return:
		success			- all wellbeing values saved successfully and checkin recorded
		invalid-request	- missing request field
		bad-woop		- woop score out of range
		bad-emote		- emoji score out of range
		fails			- names of db entries which could not save (woop, emote, checkin)
	"""
	#permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			content		= request.POST
			username	= content.get("username")
			woop		= int(content.get("woop"))
			emote		= int(content.get("emote"))
		except:
			return ERROR_INVALID
		try:
			user = User.objects.filter(username = username)[0]
		except:
			username	= request.user
			return ERROR_NOTFOUND
		if woop not in GOOD_WOOPS:
			return Response({"bad-woop": woop})
		if emote not in GOOD_EMOTES:
			return Response({"bad-emote": emote})
		new_woop = WoopScoreIndividual(UID = user, rsp = woop)
		new_emote = EmoteScoreIndividual(UID = user, rsp = emote)
		new_checkin = LastCheckins(user = user)
		content = {"fails": []}
		#try:
		new_woop.save()
		#except:
		#	content["fails"].append({"woop": woop})
		try:
			new_emote.save()
		except:
			content["fails"].append("emote")
		try:
			new_checkin.save()
		except:
			content["fails"].append("checkin")
		if content["fails"] != []:
			return Response(content)
		return REQ_SUCCESS

class APIPushNewMessage(APIView):
    """TODO HOFF DOCUMENT ME"""
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user = request.user
        try:
            user_2_username = request.POST.get("user_2")
            data = request.POST.get("content")
        except:
            return ERROR_INVALID
        user_2 = User.objects.get(username=user_2_username)
        if not Contact.objects.filter(Q(contact_user_1=user, contact_user_2=user_2) | Q(contact_user_1=user_2, contact_user_2=user)).exists():
            return Response({"error": "not_contacts"})
        new_message = Message(sender=user, recipient=user_2, content=data)
        new_message.save()
        return REQ_SUCCESS

class APIPushDummyData(APIView):
	"""TESTING DO NOT USE FOR REAL"""
	def post(self, request):
		try:
			uname = request.POST.get("username")
			user = User.objects.filter(username = uname)[0]
		except:
			return ERROR_INVALID
		today = datetime.today()
		succs = 0
		for i in range(1, 35):
			date = today - timedelta(days = i)
			new_woop = WoopScoreIndividual(UID = user, dat = date, rsp = randint(5, 31))
			new_emo = EmoteScoreIndividual(UID = user, dat = date, rsp = randint(1, 6))
			new_woop.save()
			new_emo.save()
			succs += 1
		return Response({"success": succs})

class APIPushEventSignOn(APIView):
	"""Register a user as attending an event, or remove their intention to attend.

	POST
	event_id	- ID of event to change attendance status of
	choice		- "attend" / "leave"

	return:
		success			- attendance updated successfully
		error_invalid	- missing request field
		bad_choice		- invalid choice value
		bad_event		- event doesn't exist
		save_error		- attendance record could not be saved (probably duplicate attendance)
		bad_attendance	- tried to remove attendance for user not attending event
	"""

	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			uname		= request.POST.get("username")
			user		= User.objects.filter(username = uname)[0] # DELETEME
		except:
			user = request.user
			#return Response({"bad_user": uname})
		try:
			eid			= request.POST.get("event_id")
			event_id	= int(request.POST.get("event_id"))
			choice		= request.POST.get("choice").lower()
		except:
			return ERROR_INVALID
		if choice not in {"attend", "leave"}:
			return Response({"bad_choice": choice})
		try:
			event = Events.objects.filter(event_id = event_id)[0]
		except:
			return Response({"bad_event": event_id})
		if choice == "attend":
			new_attending = Attending(attending_user = user, attending_event = event)
			try:
				new_attending.save()
			except:
				return Response({"save_error": (event.name, event.event_id, user.username)})
		else:
			try:
				remove = Attending.objects.filter(attending_user = user, attending_event = event)[0]
				remove.delete()
			except:
				return Response({"bad_attendance": (user.username, event.name)})
		return REQ_SUCCESS

class APIPushUserDetails(APIView):
	"""Register some bare minimum information about the users.

	POST
	username	- email of user
	state		- user's state of residence
	suburb		- user's suburb of residence
	real_name	- user's display name
	travel_dist	- maximum distance (km) user is willing to travel

	return:
		success			- personal details were registered successfully
		invalid_request	- missing event field
		bad_username	- user email not in Users table
		bad_location	- suburb not in state or state does not exist
		save_error		- personal details were not able to be saved to DB
	"""

	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			content		= request.POST
			username	= content.get("username")
			state		= content.get("state")
			suburb		= content.get("suburb")
			name		= content.get("real_name")
			travel_dist	= int(content.get("travel_dist"))
		except:
			return ERROR_INVALID
		try:
			user = User.objects.filter(username = username)[0]
		except:
			user = request.user
			return Response({"bad_username": username})
		try:
			SSID = StateSuburbs.objects.filter(state = state, suburb = suburb)[0]
		except:
			return Response({"bad_location": (state, suburb)})
		new_optus	= PersonalInfo(user = user, SSID = SSID, real_name = name, travel_dist = travel_dist)
		try:
			new_optus.save()
		except:
			return Response({"cunt": [user.username, SSID.state, SSID.suburb, travel_dist]})
			return ERROR_SAVEERROR
		return REQ_SUCCESS

class APIPushCheckinPings(APIView):
	"""Send reminders to log in / reminders to contact friends.

	POST
	username	- name of user to remind / draw concern to

	return:
		success			- appropriate notifications generated successfully
		invalid_request	- missing username field
		not_found		- user doesn't exist
		no_checkins		- user has never checked in
		save_error		- couldn't send user reminder to check in.
	"""

	#permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			target_name	= request.POST.get("username")
		except:
			return ERROR_INVALID
		try:
			target		= User.objects.filter(username = target_name)[0]
		except:
			return Response({"not_found": target_name})
		today	= datetime.today().date()
		now		= datetime.now()
		try:
			latest	= LastCheckins.objects.filter(user = target).latest("login").login
		except:
			# Should never reach here; investigate immediately if it does
			return Response({"no_checkins"})
		offset	= (today - latest).days
		if offset <= REMIND:
			reminder = Notifications(recipient = target, notif_type = "CI", content = REMIND_TEXT, link_event = None, timestamp = now)
			try:
				reminder.save()
			except:
				return ERROR_SAVEERROR
		if offset <= PING_MATES:
			real_name = PersonalInfo.objects.filter(user = target)[0].real_name
			notif_body = real_name + PHONE_A_FRIEND
			friends = Contact.objects.filter(contact_user_1 = target)
			for friend in friends:
				ping = Notifications(recipient = friend.contact_user_2, notif_type = "FC", content = notif_body, link_event = None, link_user = target, timestamp = now)
				try:
					ping.save()
				except:
					# There's really no reason why this should fail.
					# In any case, just ignore the error
					# and ping the rest of the friends.
					pass
		return REQ_SUCCESS

class APIPushAnyNotification(APIView):
	"""TODO DELETE ME LATER"""
	#permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			content	= request.POST
			target	= User.objects.filter(username = content.get("target"))[0]
		except:
			return Response({"bad user"})
		try:
			n_type	= content.get("type")
			text	= content.get("content")
		except:
			return Response({"bad content"})
		try:
			new		= Notifications(recipient = target, notif_type = n_type, content = text, timestamp = datetime.now())
			new.save()
		except:
			return ERROR_INVALID
		return REQ_SUCCESS

class APIFakeFriends(APIView):
	"""TODO DELETE ME LATER"""
	#permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			u1 = User.objects.filter(username = request.POST.get("t1"))[0]
			u2 = User.objects.filter(username = request.POST.get("t2"))[0]
			clarence = Contact(contact_user_1 = u1, contact_user_2 = u2)
			clarence.save()
			clazzo = Contact(contact_user_1 = u2, contact_user_2 = u1)
			clazzo.save()
		except:
			return Response({"NO"})
		return Response({"clazzo mate how u goin"})

class APISetUserInterests(APIView):
	"""Add or remove a user's interest

	POST
	username	- name of user whose interests to modify
	interests	- ids of interest to add or remove

	return:
		success			- >= 1 interests added or dropped successfully
		invalid_request	- missing request field
		bad_mode		- invalid mode option
		not_found		- user or interest doesn't exist
		all_fails		- every interest failed to update
	"""

	#permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			username	= request.POST.get("username")
			target		= User.objects.filter(username = username)[0]
		except:
			target		= request.user
		try:
			inter_ids	= request.POST.get("interests").split(",")
			int_ids = []
			for i in inter_ids:
				int_ids.append(int(i))
			#int_ids	= [int(i) for i in ]#flat_cut(inter_ids)]
		except:
			return Response({"error": "invalid_interests"})
		#return Response((int_ids, request.POST.get("interests")))
		"""
		int_names	= flat_cut(int_names, ", ")
		interests	= []
		int_ids		= []
		try:
			for i in interests:
				interest = Interests.objects.filter(interest = i)[0]
				int_ids.append(interest.interes_id)
		#if mode not in {"add", "remove"}:
		#	return Response({"bad_mode": mode})
		"""
		try:
			interests	= [Interests.objects.filter(interest_id = i)[0] for i in int_ids]
		except:
			return ERROR_NOTFOUND
		worked	= []
		fails	= 0

		die = UserInterests.objects.filter(user = target)
		for d in die:
			die.delete()

		#if mode == "add":
		for interest in interests:
			user_interest	= UserInterests(user = target, interest = interest)
			try:
				user_interest.save()
				worked.append(interest.interest)
			except:
				fails += 1
				# Individual write errors aren't a problem
				pass
		"""
		else:
			for interest in interests:
				try:
					to_kill	= UserInterests.objects.filter(user = target, interest = interest)[0]
					to_kill.delete()
					worked.append(interest.interest)
				except:
					# Individual delete errors aren't a problem
					pass
		"""
		if len(worked) == 0:
			return Response({"all_fails"})
		return Response({"success": worked, "fails": fails})

class APIAddSSID(APIView):
	"""TODO DELETE THIS LATER"""
	#permission_classes = (IsAuthenticated,)
	def post(self, request):
		#return GO_AWAY
		p		= request.POST
		state	= p.get("state")
		suburb	= p.get("suburb")
		latit	= p.get("latit")
		longit	= p.get("longit")
		new		= StateSuburbs(state = state, suburb = suburb, latit = latit, longit = longit)
		try:
			new.save()
		except:
			return Response({"FAIL"})
		return REQ_SUCCESS

class APISendRecommendations(APIView):
	"""Generate new event recommendations notifications for a user.
	Don't rerun this successively or duplicate notifications will stack up.

	POST
	username	- email address of user to generate recommendations for

	return:
		success			- recommendation sent successfully
		error_invalid	- missing username field in request
		error_nothing	- no events can be recommended
		error_notfound	- user doesn't exist
		error_nodetails	- user's details aren't registered	- investigate NOW
		error_missingei	- event has no interests registered	- investigate NOW
		error_missingui	- user interests aren't registered	- investigate NOW
	"""

	#permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			username = request.POST.get("username")
		except:
			return ERROR_INVALID
		try:
			user = User.objects.filter(username = username)[0]
		except:
			return ERROR_NOTFOUND
		try:
			details = PersonalInfo.objects.filter(user = user)[0]
		except:
			return Response({"error_nodetails"})
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
				cand_interests = set([i.interest.interest for i in EventInterests.objects.filter(event = c)])
			except:
				return Response({"error_missingei": c.name})
			overlap	= cand_interests.intersection(u_interests)
			sim		= 0
			if no_user_ints != 0:
				sim		= len(overlap) / no_user_ints
			ranks.append((sim, c))#, u_interests, cand_interests))
		ranks.sort(key = lambda x: x[0])
		#return Response([r[1].name for r in ranks])

		_, recco = ranks.pop(-1)
		push = Notifications(recipient = user, notif_type = "RE", content = RECCO_TEXT + recco.name, link_event = recco, timestamp = datetime.now())
		try:
			push.save()
		except:
			return ERROR_SAVEERROR

		return Response({"Success": [recco.name, len(cands), len(ranks)]})



def ss_distance(ss1, ss2):
	"""Find Haversine distance between two suburbs.
	Could just use Euclid and ignore the
	tiny amount of curvature involved at this scale
	but this looks cooler.

	ss1		- SSID entry of first suburb
	ss2		- SSID entry of second suburb

	return	- <float> Haversine distance between the suburbs
	"""

	lat_1, lat_2	= ss1.latit, ss2.latit
	d_lats			= abs(lat_1 - lat_2)
	d_longs			= abs(ss1.longit - ss2.longit)

	# Formula from https://www.omnicalculator.com/other/latitude-longitude-distance
	"""
	haversine		= 2 * EARTH_RADIUS * asin(sqrt(
						((sin(d_lats) ** 2) / 2) +
						(cos(lat_1) * cos(lat_2) *
						((sin(d_longs) ** 2) / 2))))
	lol that didn't work
	"""

	return ((d_lats ** 2) + (d_longs ** 2)) ** 0.5
	#return haversine
