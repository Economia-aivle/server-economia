from django.urls import path, include
from django.contrib import admin
from . import views

app_name = 'users'



urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('find_account_id', views.find_account_id, name='find_account_id'),
    path('find_account', views.find_account, name='find_account'),
    path('check_id/<str:player_id>', views.check_id, name='check_id'),
    path('find_account_pwd/', views.find_account_pwd, name='find_account_pwd'),
    path('check_password/<str:pwd>', views.check_password, name='check_password'),
    path('ranking/', views.ranking, name='ranking'),
    path('char_create/', views.character_create_view, name='char_create'),
    path('get_character/<int:player_id>/', views.get_character_view, name='get_character'),
    path('char_update/', views.character_update_view, name='char_update'),
    path('login/', views.admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('api/login/', views.AdminLoginAPI.as_view(), name='admin_login_api'),
    path('notice/', views.notice_list, name='notice'),
    path('notice/<int:notice_id>/', views.notice_detail, name='notice_detail'),
    path('api/subjects/', views.getSubjectsDatas, name='subjects'),
    path('api/scores/<int:subject_id>/', views.getSubjectsScoreDatas, name='subjects_score'),
    path('delete/account/<str:player_id>/', views.delete_account, name='delete_account'),
    path('success/', views.success, name='success'),
    path('check/username/', views.check_username, name='check_username'),
    path('register/', views.register, name='register'),
    path('success', views.success, name='success'),
    
]
