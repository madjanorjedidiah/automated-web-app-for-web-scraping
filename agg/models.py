from __future__ import unicode_literals
from django.db import models

# Create your models here.
class estates(models.Model):
	property_name = models.CharField(max_length=1000, null=True)
	showers = models.IntegerField(blank=True, null=True)
	beds = models.IntegerField(blank=True, null=True)
	garages = models.IntegerField(blank=True, null=True)
	area =  models.CharField(max_length=400, null=True)
	# description = models.CharField(max_length=100)
	price = models.CharField(max_length=100, null=True)
	currency = models.CharField(max_length=100, null=True)
	rent_period = models.CharField(max_length=500, null=True)
	url = models.URLField( null=True)
	# address = models.CharField(max_length=60)
	time_posted = models.CharField(max_length=200, null=True)

	class Meta:
		ordering = ['-time_posted']



	def __str__(self):
		return self.property_name

