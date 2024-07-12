# blog/urls.py
from django.urls import path
from django.contrib import admin
from . import views

app_name = 'users'
urlpatterns = [ 

    path('signup', views.signup, name='signup'),
    path('find_account_id', views.find_account_id, name='find_account_id'),
    path('check_id/<str:player_id>', views.check_id, name='check_id'),
    path('ranking', views.ranking, name='ranking'),
    path('char_create/', views.character_create_view, name='char_create'),
    path('get_character/<int:player_id>/', views.get_character_view, name='get_character'),
    path('char_update/', views.character_update_view, name='char_update'),
    path('find_account_pwd/', views.find_account_pwd, name='find_account_pwd'),
    path('check_pwd/<str:password>', views.check_pwd, name='check_pwd'),


]
