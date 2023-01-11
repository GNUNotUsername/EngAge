from datetime						import datetime
from django.db						import models
from django.contrib.auth.models		import AbstractUser, User
from modules.constants				import STATES
from events.models					import Events, EventProviders, Interests, StateSuburbs, TransportProviders

from random import randint

class LastCheckins(models.Model):
	"""Listing of last check in per user, for monitoring wellbeing"""
	user	= models.OneToOneField(User, on_delete=models.CASCADE)
	login	= models.DateField(auto_now = True)

class PersonalInfo(models.Model):
	"""Bare minimum user personal info required for backend functionality"""
	user		= models.OneToOneField(User, on_delete = models.CASCADE)
	SSID		= models.ForeignKey(StateSuburbs, on_delete = models.PROTECT, related_name = "user_location")	# State & Suburb of residence
	real_name	= models.CharField(max_length = 100)
	travel_dist	= models.FloatField()																			# Maximum distance user willing to travel for events

class Contact(models.Model):
	"""Friends / contacts each user has registered"""
	class Meta:
		unique_together = (("contact_user_1", "contact_user_2"))
		#constraints = [
		#	models.UniqueConstraint(fields = ["contact_user_1", "contact_user_2"], name = "unique_contacts")
		#]

	# https://stackoverflow.com/questions/35096607/how-to-enforce-different-values-in-multiple-foreignkey-fields-for-django
	def save(self, *args, **kwargs):
		if self.contact_user_1 == self.contact_user_2:
			raise Exception("User cannot add themself as a contact")
		super(Contact, self).save(*args, **kwargs)\

	contact_id		= models.AutoField(primary_key = True)
	contact_user_1	= models.ForeignKey(User, on_delete = models.CASCADE, related_name = "contact_user_1")
	contact_user_2	= models.ForeignKey(User, on_delete = models.CASCADE, related_name = "contact_user_2")

class PendingContact(models.Model):
	"""Friend requests which have not been confirmed by both sides yet"""
	class Meta:
		unique_together = (("pending_user_1", "pending_user_2"))
		#constraints = [
		#	models.UniqueConstraint(fields = ["pending_user_1", "pending_user_2"], name = "unique_pending")
		#]
	def save(self, *args, **kwargs):
		if self.pending_user_1 == self.pending_user_2:
			raise Exception("User cannot add themself as a contact")
		super(PendingContact, self).save(*args, **kwargs)
	pending_user_1	= models.ForeignKey(User, on_delete = models.PROTECT, related_name = "pending_user_1")
	pending_user_2	= models.ForeignKey(User, on_delete = models.PROTECT, related_name = "pending_user_2")
	user_1_conf	= models.BooleanField()
	user_2_conf	= models.BooleanField()

class Message(models.Model):
	"""Messages sent between users"""
	class Meta:
		unique_together = (("sender", "recipient", "timestamp"))
		#constraints = [
		#	models.UniqueConstraint(fields = ["sender", "recipient", "timestamp"], name = "unique_messages")
		#]
	sender		= models.ForeignKey(User, on_delete = models.PROTECT, related_name = "sender")
	recipient	= models.ForeignKey(User, on_delete = models.PROTECT, related_name = "recipient")
	content		= models.CharField(max_length = 2500)
	timestamp	= models.DateTimeField(auto_now_add = True)

class UserInterests(models.Model):
	"""List of interests for each user"""
	class Meta:
		unique_together = (("user", "interest"))
		#constraints = [
		#	models.UniqueConstraint(fields = ["user", "interest"], name = "surjective ints")
		#]
	user		= models.ForeignKey(User, on_delete = models.CASCADE, related_name = "user")
	interest	= models.ForeignKey(Interests, on_delete = models.PROTECT, related_name = "user_interest")

class Notifications(models.Model):
	"""List of notifications for each user"""
	NOTIF_CLASSES = [
		("CI", "Remember to fill in your wellness check"),	("FC", " hasn't checked in recently. Send a message?"),
		("FA", "Friend request accepted"),					("FQ", "You have a friend request from "),
		("FR", "Friend request rejected"),					("RE", "You may be interested in this event: "),
        ("UE", "An event you are interested in is upcoming: ")
	]

	notif_id	= models.AutoField(primary_key = True)
	recipient	= models.ForeignKey(User, on_delete = models.CASCADE, related_name = "notifications_user_1")
	notif_type	= models.CharField(max_length = 2, choices = NOTIF_CLASSES)											# Notification type determines icon to show
	content		= models.CharField(max_length = 100)
	link_event	= models.ForeignKey(Events, on_delete = models.CASCADE, related_name = "link_event", null = True, blank = True)	# For types UE and RE, link to relevant event
	link_user	= models.ForeignKey(User, on_delete = models.CASCADE, related_name = "link_user", null = True, blank = True)
	timestamp	= models.DateTimeField()
