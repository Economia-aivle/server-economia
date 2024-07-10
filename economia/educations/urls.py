# blog/urls.py
from django.urls import path
from django.contrib import admin
from . import views

app_name = 'educations'
urlpatterns = [
    path('level_choice/', views.level_choice, name='level_choice'),
    path('tf_quiz/', views.tf_quiz_view, name='tf_quiz'),
    path('tf_quiz/<int:question_id>/', views.tf_quiz_view, name='tf_quiz_detail'),
    path('tf_quiz_page/', views.tf_quiz_page, name='tf_quiz_page'),
    path('choose_tf_chapter/', views.choose_tf_chapter_view, name='choose_tf_chapter'),
    path('blank', views.blank, name='blank'),
    path('multiple', views.multiple, name='multiple'),
    path('previous_quiz_answer', views.previous_quiz_answer, name='previous_quiz_answer'),
    path('previous_quiz', views.previous_quiz, name='previous_quiz'),
    path('study_video/', views.study_view, name='study_video'),
    path('summary_anime', views.summary_anime, name='summary_anime'),
]