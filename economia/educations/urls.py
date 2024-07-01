# blog/urls.py
from django.urls import path
from django.contrib import admin
from . import views

app_name = 'educations'
urlpatterns = [

    path('level_choice', views.level_choice, name='level_choice'),
    path('tfquiz', views.tfquiz, name='tfquiz'), 
    path('blank', views.blank, name='blank'),
    path('multiple', views.multiple, name='multiple'),
    path('previous_quiz_answer', views.previous_quiz_answer, name='previous_quiz_answer'),
    path('previous_quiz', views.previous_quiz, name='previous_quiz'),
    path('study', views.study, name='study'),
    path('summary_anime', views.summary_anime, name='summary_anime'),

]
