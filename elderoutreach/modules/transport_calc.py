from django.contrib.auth.models	import User
from account.models				import PersonalInfo
from events.models				import Events, TransportCoverage
from constants					import f, TOP
from csv						import reader
from hashlib					import sha256
from datetime					import datetime
from os							import exists

TID_IND		= 0
SSID_IND	= 1
PRIME		= 31

def transport_to_event(event_id, username):
	"""Suggest a list of transport companies which can take a user to an event

	event_id	- ID of event user intends to travel to
	username	- ID of user intending to attend the event

	return		- <list> IDs of transport providers who can service this user.
	"""

	user_loc	= f(PersonalInfo)(username == username)[TOP].SSID
	event_loc	= f(Events)(event_id == event_id)[TOP].SSID
	providers	= a(TransportCoverage)
	cut_covers	= [(p.TID, p.location) for p in providers]
	cover_maps	= {pair[TID_IND]: [] for pair in cut_covers}
	for pair in cut_covers:
		cover_maps[pair[TID_IND]].append(pair[SSID_IND])

	prov_cands	= [k for k in cover_maps if ((user_loc in cover_maps[k]) and (event_loc in cover_maps[k]))]

	return prov_cands

def lookup_city_coverage(city):
	f = validate_file(TREE, TREE_CSUM)
	f.close()
	from sstree import SSTREE as tree
	for state in tree:
		if city in tree[state]:
			return tree[state][city]

def generate_coverage(TID, city):
	"""Generate SSIDs for each new registered transport provider in their respective city"""
	pass

if __name__ == "__main__":
	format_city_maps()
