# blog/urls.py
from django.urls import path
from django.contrib import admin
from . import views

app_name = 'educations'
urlpatterns = [
    path('level_choice/<int:characters>/<str:subject>/<int:chapter>/', views.level_choice, name='level_choice'),
    path('chapter_summary', views.chapter_summary, name='chapter_summary'),
    path('tfquiz', views.tfquiz, name='tfquiz'), 
    path('blank/<int:characters>/<str:subject>/<int:chapter>/<int:num>', views.blank, name='blank'),
    path('multiple', views.multiple, name='multiple'),
    path('previous_quiz_answer', views.previous_quiz_answer, name='previous_quiz_answer'),
    path('previous_quiz/<int:characters>', views.previous_quiz, name='previous_quiz'),
    path('study', views.study, name='study'),
    path('wrong_explanation', views.wrong_explanation, name='wrong_explanation'),
    path('summary_anime', views.summary_anime, name='summary_anime'),
    path('blankdatas/<int:characters>', views.getBlankDatas, name="BlankDatas"),
    path('multipledatas/<int:characters>', views.getMultipleDatas, name="MultipleDatas"),
    path('tfdatas/<int:characters>', views.getTfDatas, name="TfDatas"),
    path('tfdatas/<int:characters>', views.getTfDatas, name="TfDatas"),
    path('getSubjectDatas/<str:subjects>/', views.getSubjectDatas, name='get_subject_datas'),
    path('chapter/<str:subjects>/', views.chapter, name='chapter'),
    path('getStageDatas/<int:characters>/', views.getStageDatas, name='StageDatas'),
]
