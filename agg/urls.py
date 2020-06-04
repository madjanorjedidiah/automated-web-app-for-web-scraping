from django.urls import path
from . import views


app_name = 'agg'

urlpatterns = [
    path('', views.index, name='home'),
    path('save', views.saveToDb, name='save'),

]