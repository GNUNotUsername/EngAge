from django.db						import models
from modules.constants				import STATES
from phonenumber_field.modelfields	import PhoneNumberField
from django.contrib.auth.models		import AbstractUser, User

from datetime import datetime

class StateSuburbs(models.Model):
	"""Codification of locations, used for Users, Events, transport provider coverage"""
	class Meta:
		unique_together = (("state", "suburb"))
	SSID	= models.AutoField(primary_key = True)					# Primary Key
	state	= models.CharField(choices = STATES, max_length = 3)	# Some states have suburbs with the same name
	suburb	= models.CharField(max_length = 50)
	latit	= models.FloatField()									# Post office coords for distance estimation
	longit	= models.FloatField()

class EventProviders(models.Model):
	"""Event organisers registration table"""
	ORG_TYPES = [("I", "Individual"), ("O", "Organisation")]

	class Meta:
		constraints = [
			models.UniqueConstraint(fields = ["name", "email", "phone"], name = "unique_org")
		]

	PID			= models.AutoField(primary_key = True)
	name		= models.CharField(max_length = 100)
	org_type	= models.CharField(choices = ORG_TYPES, max_length = 1)
	email		= models.EmailField()
	phone		= PhoneNumberField()
	location	= models.ForeignKey(StateSuburbs, on_delete = models.PROTECT, related_name = "event_provider_location")

class Interests(models.Model):
	"""Codification of interests with IDs instead of relying on matching strings"""
	class Meta:
		constraints = [
			models.UniqueConstraint(fields = ["interest"], name = "unique_interests")
		]

	interest_id	= models.AutoField(primary_key = True)
	interest	= models.CharField(max_length = 48)

class Events(models.Model):
	"""Events the users can attend"""
	#def save(self, *args, **kwargs):
	#	if self.end_time <= self.start_time:
	#		raise Exception("Event cannot end before it starts")
	#	super(Events, self).save(*args, **kwargs)
	event_id	= models.AutoField(primary_key = True)
	name		= models.CharField(max_length = 100)
	PID			= models.ForeignKey(EventProviders, on_delete = models.CASCADE, related_name = "events_PID")	# ID of event provider
	# Storing SSID and address may seem redundant but it makes things less painful when querying from the table
	address		= models.CharField(max_length = 200)															# Street address of venue
	SSID		= models.ForeignKey(StateSuburbs, on_delete = models.PROTECT, related_name = "event_ssid")		# Suburb used for distance estimation to users
	start_time	= models.DateTimeField(auto_now = False)
	end_time	= models.DateTimeField(auto_now = False)
	description	= models.CharField(max_length = 200)

class EventInterests(models.Model):
	"""Map of relevant interests for each event"""
	class Meta:
		unique_together = (("event", "interest"))

	event		= models.ForeignKey(Events, on_delete = models.CASCADE, related_name = "eventinterests_event")
	interest	= models.ForeignKey(Interests, on_delete = models.CASCADE, related_name = "eventinterests_interest")

class Attending(models.Model):
	"""Listing of users intending to attend each event"""
	class Meta:
		unique_together = (("attending_user", "attending_event"))
	#	#constraints = [
	#	#	models.UniqueConstraint(fields = ["attending_user", "attending_event"], name = "attending_key")
	#	#]
	#att_id			= models.AutoField(primary_key = True)
	attending_user	= models.ForeignKey(User, on_delete = models.CASCADE, related_name = "attending_user")
	attending_event	= models.ForeignKey(Events, on_delete = models.CASCADE, related_name = "attending_event")

class TransportProviders(models.Model):
	"""Registration of companies providing transport to OAPs"""
	#class Meta:
	#	constraints = [
	#		models.UniqueConstraint(fields = ["name"], name="unique_provider_names")
	#	]

	TID					= models.AutoField(primary_key = True)
	name				= models.CharField(max_length = 100)
	#location			= models.ForeignKey(StateSuburbs, on_delete = models.CASCADE, related_name = "transport_provider_location")
	booking_link		= models.URLField(null = True, blank = True)
	booking_phone		= PhoneNumberField(null = True, blank = True)
	min_discount_age	= models.IntegerField()		# Minimum age a client must be for senior discounts
	allow_carers		= models.BooleanField()		# Carers allowed on board transport vehicles
	require_med_list	= models.BooleanField()
	min_days_b4_cancel	= models.IntegerField()		# Minimum days required to cancel bookings and still receive a refund


class TransportCoverage(models.Model):
	"""Map for areas serviced by OAP transport companies"""
	class Meta:
		unique_together = (("TID", "area"))
	TID		= models.ForeignKey(TransportProviders, on_delete = models.CASCADE)
	area	= models.ForeignKey(StateSuburbs, on_delete = models.PROTECT)

class CatersOptions(models.Model):
	"""
	Codification of catering options
	(coeliac/diabetic/low mobility etc)
	which OAP transport companies may cater to
	"""
	class Meta:
		constraints = [
			models.UniqueConstraint(fields = ["caters_to", "caters_id"], name = "catersoptions_key")
		]
	caters_id	= models.AutoField(primary_key = True)
	caters_to	= models.CharField(max_length = 200)

class ProviderCaters(models.Model):
	"""Map of OAP transport companies to their respective catering options"""
	class Meta:
		unique_together = (("cater_provider", "cater_caters"))
	cater_provider	= models.ForeignKey(TransportProviders, on_delete = models.CASCADE, related_name = "cater_provider")
	cater_caters	= models.ForeignKey(CatersOptions, on_delete = models.CASCADE, related_name = "cater_caters")
