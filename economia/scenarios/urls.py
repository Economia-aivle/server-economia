# blog/urls.py
from django.urls import path
from django.contrib import admin
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'scenarios'
urlpatterns = [

    path('previous_scenario/<int:id>', views.previous_scenario, name='previous_scenario'),
    path('scenario_list', views.scenario_list, name='scenario_list'), 
    path('scenario_num/<int:id>', views.scenario, name='scenario_num'),
    path('scenario_datas', views.getScenarioDatas, name="ScenarioDatas"),
    path('scenario/<int:id>', views.getScenarioData, name="scenario"),
    path('create_scenario/', views.create_scenario, name='create_scenario'),
    path('comment_datas/<int:scenario>', views.getCommentData, name='CommentDatas'),
    path('like/comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('submit_answer/', views.submit_answer, name='submit_answer'),
    path('childcomment_datas/<int:comments_id>', views.getChildCommentData, name='childcomment_datas'),
    path('submit_childcomment/', views.submit_childcomment, name='submit_childcomment'),
    path('delete_comment/<int:id>/', views.delete_comment, name='delete_comment'),
    path('delete_childcomment/<int:id>/', views.delete_childcomment, name='delete_childcomment'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('chapter/<str:subjects>/', views.delete_childcomment, name='delete_childcomment'),
    
]
