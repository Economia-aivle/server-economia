from django.urls import path, include
from django.contrib import admin
from . import views

app_name = 'users'
urlpatterns = [

    path('notice', views.notice, name='notice'),
    path('signup', views.signup, name='signup'),
    path('find_account_pwd', views.find_account_pwd, name='find_account_pwd'), 
    path('find_account_id', views.find_account_id, name='find_account_id'),
    path('find_account', views.find_account, name='find_account'),
    path('check_id', views.check_id, name='check_id'),
    path('char_create', views.char_create, name='char_create'),
    path('char_delete', views.char_delete, name='char_delete'),
    path('ranking', views.ranking, name='ranking'),
    path('api/subjects', views.getSubjectsDatas, name='subjects'),
    path('api/scores/<int:subject_id>', views.getSubjectsScoreDatas, name='subjects_score'),
    path('delete_account/<str:player_id>/', views.delete_account, name='delete_account'),
    

]
