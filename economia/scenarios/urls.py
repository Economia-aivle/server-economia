# blog/urls.py
from django.urls import path
from django.contrib import admin
from . import views

app_name = 'scenarios'
urlpatterns = [

    path('previous_scenario/<int:id>', views.previous_scenario, name='previous_scenario'),
    path('scenario_list', views.scenario_list, name='scenario_list'), 
    path('scenario_num/<int:id>', views.scenario, name='scenario_num'),
    path('scenario_datas', views.getScenarioDatas, name="ScenarioDatas"),
    path('scenario/<int:id>', views.getScenarioData, name="scenario"),
    path('create_scenario/', views.create_scenario, name='create_scenario'),
    path('comment_datas/<int:scenario>', views.getCommentData, name='CommentDatas'),
    path('like/', views.like_comment, name='like_comment'),  
    path('submit_answer/', views.submit_answer, name='submit_answer'),
    path('childcomment_datas/<int:comments_id>', views.getChildCommentData, name='childcomment_datas'),
    path('submit_childcomment/', views.submit_childcomment, name='submit_childcomment'),
      path('delete_comment/<int:id>/', views.delete_comment, name='delete_comment'),
    path('delete_childcomment/<int:id>/', views.delete_childcomment, name='delete_childcomment'),
]
