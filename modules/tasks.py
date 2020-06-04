from __future__ import absolute_import, unicode_literals
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
from bulk_sync import bulk_sync
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from django.http import HttpResponseRedirect, HttpResponse
from agg.models import estates
from celery import shared_task

import datetime
from celery.schedules import crontab
from modules.celery import app





# disable UTC so that Celery can use local time
app.conf.enable_utc = True



def if_exists_int(x):
    if x is not None:
        return x.text
    else:
        return 0


def if_exists_str(x):
    if x is not None:
        return x.text
    else:
        return 'None'

@shared_task
def scrape():

	session = requests.Session()
	retry = Retry(connect=3, backoff_factor=0.5)
	adapter = HTTPAdapter(max_retries=retry)
	session.mount('https://meqasa.com/houses-for-rent-in-ghana', adapter)
	session.mount('https://meqasa.com/houses-for-rent-in-ghana', adapter)

	results = session.get('https://meqasa.com/houses-for-rent-in-ghana')
	soup = BeautifulSoup(results.content, 'lxml')
	listings = soup.find_all('div', {'class':'mqs-featured-prop-inner-wrap'})

	real_estate = []


	for tag in listings:
	    property_name = if_exists_str(tag.find('h2')).replace('\n', '')
	    beds =  int(if_exists_int(tag.find('li', {'class':'bed'})))
	    garages = int(if_exists_int(tag.find('li', {'class':'garage'})))
	    showers = int(if_exists_int(tag.find('li', {'class':'shower'})))
	    area = if_exists_str(tag.find('li', {'class':'area'}))
	    # description = if_exists(a.find_all('p'))[1]
	    price = if_exists_str(tag.find('p', {'class':'h3'})).replace('\nPrice', '').replace('/ month\n', '').replace('[Price disclosed on request] \n', '')
	    currency = if_exists_str(tag.find('p', {'class':'h3'})).replace('\nPrice', '').replace('/ month\n', '').replace('[Price disclosed on request] \n', '')
	    currency = re.sub('\d', '', currency)
	    rent = if_exists_str(tag.find('p', {'class':'h3'})).replace('\nPrice$', '').replace('\nPriceGH₵', '').replace('\n', '').replace('PricePricedisclosedonrequest', '')
	    c = re.sub('\d.....\W', '', rent)
	    d = re.sub('\d....\W', '', c)
	    rentperiod = re.sub('\W', '', d)
	    url = tag.find('a')['href']
	    url = 'https://meqasa.com/houses-for-rent-in-ghana' + url
	    # address = if_exists(a.find('h2')).replace('\n', '').split('at')[1]
	    time_posted = if_exists_str(tag.find('p', {'class': 'wsnr'}))




	    real_estate.append(
	    	{
	            'property_name': property_name,             
	            'showers': showers,
	            'beds': beds,            
	            'garages': garages,
	            'area': area,
	            # 'description': description,
	            'price': price,
	            'currency': currency,
	            'rent_period': rentperiod,
	            'url': url,  
	            # 'address': address,
	            'time_posted': time_posted,
	            
	        }
	    )

	
	return real_estate


# add "birthdays_today" task to the beat schedule
app.conf.beat_schedule = {
    "scrape-task": {
        "task": "tasks.scrape",
        "schedule": crontab(minute=0, hour=0)
    }
}


