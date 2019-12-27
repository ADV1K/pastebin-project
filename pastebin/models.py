import datetime

from django.db import models
from django.utils import timezone


class Paste(models.Model):
	paste_title = models.CharField(max_length=100)
	paste_code = models.TextField()  # max paste size is 4kb
	paste_format = models.CharField(max_length=20)  # the paste is written in... ...python, bash, lua, etc
	pub_date = models.DateTimeField('date published')
	# paste_expiration = models.DateTimeField()  # datetime.timedelta might be helpful
	# paste_exposure = models.CharField(max_length=20)  # public, private, unlisted

	def __str__(self):
		return self.paste_title
