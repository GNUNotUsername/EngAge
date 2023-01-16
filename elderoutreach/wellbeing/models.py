from django.db import models

from events.models				import StateSuburbs
from modules.constants			import STATES
from django.contrib.auth.models	import User

WOOP_RANGE	= range(6, 31)
WOOP_MIN	= 6
WOOP_MAX	= 30
EMOTE_MIN	= 1
EMOTE_MAX	= 5

class EmoteScoreIndividual(models.Model):
	"""Lists of each user's daily emoji wellbeing responses"""
		#constraints = [
		#	models.UniqueConstraint(fields = ["UID", "dat"], name = "daily-emotions")
		#]

	# From the pain scale on prototype
	EMOTIONS = [
		(1, "HAPPY"),
		(2, "SATISFIED"),
		(3, "NEUTRAL"),
		(4, "SAD"),
		(5, "DISTRESSED")
	]

	key = models.AutoField(primary_key = True)
	UID	= models.ForeignKey(User, on_delete = models.CASCADE, related_name = "daily_emotions")#, db_constraint = False, db_index = False)	# User
	dat	= models.DateField(auto_now_add = True)					# Response timestamp
	rsp	= models.PositiveSmallIntegerField(choices = EMOTIONS)	# Value of emoji selected

class WoopScoreIndividual(models.Model):
	"""Lists of each user's daily WOOP wellbeing responses"""
	key = models.AutoField(primary_key = True)
	UID	= models.ForeignKey(User, on_delete = models.CASCADE, related_name = "daily_woop")	# User
	dat	= models.DateField(auto_now_add = True)					# Response timestamp
	rsp	= models.PositiveSmallIntegerField()					# Woop score, 7 <= X <= 35

	def save(self, *args, **kwargs):
		if self.rsp not in WOOP_RANGE:
			raise Exception(f"WOOP score must be in [6, 30] range, got {self.rsp}")
		super(WoopScoreIndividual, self).save(*args, **kwargs)

class WoopScoreState(models.Model):
	"""Average WOOP score in the past month per state"""
	area	= models.CharField(choices = STATES, max_length = 3)
	score	= models.FloatField()
	date	= models.DateField(auto_now = False)

	def save(self, *args, **kwargs):
		if self.score < WOOP_MIN or self.score > WOOP_MAX:
			raise Exception(f"WOOP score must be in [6, 30] range, got {rsp}")
		super(WoopScoreState, self).save(*args, **kwargs)

class WoopScoreSS(models.Model):
	"""Average WOOP score in the past month per suburb"""
	key = models.AutoField(primary_key = True)
	area	= models.ForeignKey(StateSuburbs, on_delete = models.PROTECT)
	score	= models.FloatField()
	date	= models.DateField(auto_now = False)

	def save(self, *args, **kwargs):
		if self.score < WOOP_MIN or self.score > WOOP_MAX:
			raise Exception(f"WOOP score must be in [6, 30] range, got {rsp}")
		super(WoopScoreSS, self).save(*args, **kwargs)

class EmoteScoreSS(models.Model):
	"""Average emoji score in the past month per suburb"""
	key = models.AutoField(primary_key = True)
	area	= models.ForeignKey(StateSuburbs, on_delete = models.PROTECT)
	score	= models.FloatField()
	date	= models.DateField(auto_now = False)

	def save(self, *args, **kwargs):
		if self.score < EMOTE_MIN or self.score > EMOTE_MAX:
			raise Exception(f"Emote score must be in [6, 30] range, got {rsp}")
		super(EmoteScoreSS, self).save(*args, **kwargs)

# Average emoji score per state is a bit pointless; not including it.
