# blog/urls.py
from django.urls import path
from django.contrib import admin
from . import views

app_name = 'scenarios'
urlpatterns = [

    path('previous_scenario', views.previous_scenario, name='previous_scenario'),
    path('scenario_list', views.scenario_list, name='scenario_list'), 
    path('scenario', views.scenario, name='scenario'),

]
