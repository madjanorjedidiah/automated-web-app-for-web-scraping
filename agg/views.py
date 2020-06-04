from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from agg.models import *
from modules.tasks import scrape
from django.contrib import messages






def index(request):
	real_estate = estates.objects.all()
	
	# return HttpResponse(real_estate)
	return render(request, 'index.html', {'real_estate':real_estate})


def saveToDb(request):
	res = scrape.delay()
	scraped = res.get(timeout=40)
	
	old_data = estates.objects.count()

	for a in scraped:

		estate = estates()
		
		
		estate.property_name = a['property_name']
		estate.showers = a['showers']
		estate.beds = a['beds']
		estate.garages = a['garages']
		estate.area = a['area']
		estate.price = a['price']
		estate.currency = a['currency']
		estate.rent_period = a['rent_period']
		estate.url = a['url']

		if estates.objects.filter(property_name=estate.property_name).exists():
			continue
		else:
			estate.time_posted = a['time_posted']
			estate.save()		

	new_data = estates.objects.count()
	if old_data != new_data:
		sub = new_data - old_data
		messages.success(request, '%s homes added'% sub)
	else:
		messages.success(request, 'There are no new homes added')

	real_estate = estates.objects.all()

	return render(request, 'index.html', {'real_estate':real_estate})

