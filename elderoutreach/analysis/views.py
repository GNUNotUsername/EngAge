from django.shortcuts			import render
from django.http				import HttpResponse, JsonResponse
from django						import forms
from django.contrib.auth.forms	import UserCreationForm
from django.contrib.auth		import get_user_model
from django.contrib.auth		import login
from django.contrib				import messages
from django.shortcuts			import redirect
from django.contrib.auth		import login, authenticate #add this
from django.contrib				import messages
from django.contrib.auth.forms	import AuthenticationForm
from rest_framework.parsers		import JSONParser
from rest_framework.views		import APIView
from rest_framework.response	import Response
from rest_framework.permissions	import IsAuthenticated

from datetime					import datetime

from modules.grandom			import gen_woop_state
from events.models				import Interests, StateSuburbs
from wellbeing.models			import WoopScoreState, WoopScoreSS, EmoteScoreSS
from modules.constants			import ADMIN_AUTH, GENESIS

ONLY			= 0

TODAY			= datetime.today()
STATES			= {"ACT", "JBT", "NSW", "NT", "QLD", "SA", "TAS", "VIC", "WA", ""}
SCORE_TYPES		= {"EMOJI", "WOOP"}

SUCCESS			= Response({"success"})
INVALID_REQUEST	= Response({"error": "invalid_request"})
NOT_SUPPORTED	= Response({"bad_combo": "Statewide emoji scores are not supported"})

avg				= lambda data			: \
	0 if len(dat) == 0 else sum(data) / len(data)
unauthorised	= lambda token			: \
	Response({"error": "not authorised", "auth": f"{token}"})
bad_value		= lambda field, value	: \
	Response({"bad_value": (field, value)})
bad_ss			= lambda state, suburb	: \
	Response({"bad_ss": (state, suburb)})

class APIAggregateWellbeingMetrics(APIView):
	"""Generate new wellbeing aggregates

	GET
	days	- the number of days' worth of data to aggregate

	return:
		success			- data was able to be aggregated
		error			- days field missing or malformed
		not_authorised	- request not of admin level authorisation
	"""

	#permission_classes = (IsAuthenticated,)
	def get(self, request):
		#if str(request.auth) != ADMIN_AUTH:
		#	return unauthorised(request.auth)
		try:
			days = int(request.GET["days"])
		except:
			return INVALID_REQUEST

		for state in STATES:
			ssids, ss_emote_avgs, ss_woop_avgs, state_woop_avg = self._pull_state_avgs(state, days)
			self._dump_area_scores(ssids, ss_emote_avgs, EmoteScoreSS)
			self._dump_area_scores(ssids, ss_woop_avgs, WoopScoreSS)
			self._dump_area_scores([state], state_woop_avg, WoopScoreState)

		return SUCCESS

	def _pull_state_avgs(self, state, days):
		"""Pull ssids, emoji score averages and woop averages per suburb,
		and the overal state woop average from the wellbeing DB

		state	- the state to pull data for
		days	- the number of days' worth of data to pull

		return	- IDs of the state's suburbs
				- average emoji score for each suburb
				- average woop score for each suburb
				- the state's overall average woop score
		"""

		ssids			= list(StateSuburbs.objects.filter(state = state))
		ss_emote_avgs	= [avg(self._ss_average(ss, days, EmoteScoreIndividual)) for ss in ssids]
		ss_woop_avgs	= [avg(self._ss_average(ss, days, WoopScoreIndividual)) for ss in ssids]
		state_woop_avg	= avg(ss_woop_avgs)

		return ssids, ss_emote_avgs, ss_woop_avgs, state_woop_avg

	def _ss_average(self, ssid, days, table):
		"""Determine the average score for the given SSID in the given table over the given timespan.

		ssid	- the suburb to aggregate data for
		days	- the number of days' worth of data to aggregate
		table	- the table holding the data to aggregate

		return	- the average score for the given SSID in the given table over the given timespan.
		"""

		usernames	= [u.username for u in User.objects.all()]
		ss_emotes	= []
		for u in usernames:
			user_resps	= []
			responses	= list(table.objects.filter(UID = u))
			for r in responses:
				ago = (TODAY - r.dat).days
				if ago <= days:
					user_resps.append(r.rsp)
			usr_avg	= avg(user_resps)
			ss_emotes.append(usr_avg)
		ss_avg	= avg(ss_emotes)

		return ss_avg

	def _dump_area_scores(self, areas, scores, table):
		"""Write new entries for the given area keys to the given table

		areas	- the area keys (ssids / state names) to write the new scores for
		scores	- the scores for each SSID
		table	- the table to write to
		"""

		pairs = zip(area, scores)
		for area, score in pairs:
			entry = table(area = ssid, score = score, date = TODAY)
			entry.save()

class APIGetAreaAggregate(APIView):
	"""Retrieve aggregate wellbeing data from the wellbeing DB.

	GET
	score-type	- WOOP score or EMOJI score
	state		- element of STATES
	suburb		- suburb with state, or empty string for statewide
	date		- date of aggregation

	return:
		date			- date of aggregation, or closest previous found
		data			- aggregated data value

		error			- request field missing
		bad_combo		- requested statewide emoji score -- not supported
		bad_value		- request field contents malformed
		bad_ss			- suburb is not within state
		not_authorised	- request not of admin level authorisation
	"""

	#permission_classes = (IsAuthenticated,)
	def get(self, request):
		#if str(request.auth) != ADMIN_AUTH:
		#	return unauthorised(request.auth)
		try:
			score_type	= request.GET["score-type"].upper()
			state		= request.GET["state"].upper()
			suburb		= request.GET["suburb"].title()
			date		= datetime.strptime(request.GET["date"], DATE_SPLIT)
		except:
			return INVALID_REQUEST
		if score_type not in SCORE_TYPES:
			return bad_value("score-type", score_type)
		if state not in STATES:
			return bad_value("state", state)

		SSID	= None
		area	= None
		table	= None

		if len(suburb):
			try:
				SSID	= StateSuburbs.objects.filter(state = state, suburb = suburb)[ONLY].SSID
			except:
				return bad_ss(state, suburb)

		if score_type == "EMOJI":
			if SSID is None:
				return NOT_SUPPORTED
			area, table = SSID, EmojiScoreSS
		else:
			area, table = (SSID, WoopScoreSS) if len(suburb) else (state, WoopScoreState)
			"""
			if suburb == "":
				area, table = state, WoopScoreState
				#score = self._look_back(state, WoopScoreState, date)
			else
				area, table = SSID, WoopScoreSS
			"""

		score, q_date = self_look_back(area, table)

		return Response({"date": q_date, "data": score})

	def _look_back(self, area, table, start):
		"""Find the latest entry in the given table for the given area

		area	- area key for the table
		table	- the table to search through
		start	- the start date to scan backwards from

		return	- latest score for that area; None if none exist
				- date of latest found entry; GENESIS if none exist
		"""

		rows	= []
		offset	= 0
		score	= None
		q_date	= None

		while len(rows) == 0:
			q_date	= start_date - datetime.timedelta(days = offset)
			if q_date <= GENESIS:
				# This table has no entries for this area
				break
			rows = table.objects.filter(area = area, date = date)

		if len(rows) != 0:
			score = rows[ONLY].score

		return score, q_date

class APIGetSS(APIView):
	"""DEPRECATED :("""
	#permission_classes = (IsAuthenticated,)
	def get(self, request):
		return Response({"Don't use this"})
		try:
			date		= request.GET["date"]
			filter_val	= request.GET["data"]
			req_type	= request.GET["type"]
		except:
			return INVALID_REQUEST
		query_set = []
		#if str(request.auth) != ADMIN_AUTH:
		#	return unauthorised(request.auth)
		if req_type == "state":
			query_set = list(WoopScoreState.objects.filter(date = date, state = filter_val))
		if req_type == "suburb":
			query_set = list(WoopScoreSS.objects.filter(date = date, suburb = filter_val))
		try:
			query_obj = query_set[0]
		except IndexError:
			return Response({"error": "no_data"})
		score = query_obj.woop
		response_content = {"score": f"{score}", "parameters": f"{date}, {filter_val}", "auth": f"{request.auth}"}
		return Response(response_content)

class APIPopulateDB(APIView):
	#permission_classes = (IsAuthenticated,)
	def get(self, request):
		#if str(request.auth) != ADMIN_AUTH:
		#	return unauthorised(request.auth)
		try:
			number = request.GET["number"]
			req_type = request.GET["type"]
		except:
			return INVALID_REQUEST
		try:
			number = int(number)
		except ValueError:
			return Response({"error": "bad_number"})
		if req_type not in ["state"]:
			return Response({"error": "bad_type"})
		for _ in range(number):
			new_object = None
			if req_type == "state":
				new_row = gen_woop_state()
				new_object = WoopScoreState(woop = new_row[0], state = new_row[1], date = new_row[2])
			if new_object is not None:
				try:
					new_object.save()
				except:
					pass
		return Response({"success"})
