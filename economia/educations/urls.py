# blog/urls.py
from django.urls import path
from django.contrib import admin
from . import views
from .views import TFQuizAPIView, ChooseTFChapterView, TFQuizView

app_name = 'educations'
urlpatterns = [

    path('level_choice', views.level_choice, name='level_choice'),
    path('tfquiz/', TFQuizAPIView.as_view(), name='tfquiz'),
    path('choose_tf_chapter/', ChooseTFChapterView.as_view(), name='choose_tf_chapter'),
    path('submit_tf_answer/', TFQuizView.as_view(), name='tf_quiz'),
    path('blank', views.blank, name='blank'),
    path('multiple', views.multiple, name='multiple'),
    path('previous_quiz_answer', views.previous_quiz_answer, name='previous_quiz_answer'),
    path('previous_quiz', views.previous_quiz, name='previous_quiz'),
    path('study_video/', views.study_view, name='study_video'),
    path('summary_anime', views.summary_anime, name='summary_anime'),

]
