# Automated-web-app-for-web-scraping
The purpose of this project was to try out celery and its automated scheduling to scrape data basically housing data from online.

## RUN THE APP
Download app into local repository.
Within your django virtual environment make sure you have the rquirements.txt installed.
Start app in django environment with python manage.py runserver.
Start celery worker with celery -A conap worker -l info
Start celery scheduler with celery -A conap beat --loglevel=info
After you should have this app running.

