"""
URL configuration for economia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import render

def index(request):
    return render(request,'index.html')
def index1(request):
    return render(request,'previous_scenario.html')
def index2(request):
    return render(request,'ranking.html')
def index3(request):
    return render(request,'scenario_list.html')
def index4(request):
    return render(request,'scenario.html')
def index5(request):
    return render(request,'summary_anime.html')

def study(request):
    return render(request,'study.html')

def tfquiz(request):
    return render(request,'tfquiz.html')

def blank(request):
    return render(request,'blank.html')

def multiple(request):
    return render(request,'multiple.html')

def wrong_explanation(request):
    return render(request,'wrong_explanation.html')

def chapter_summary(request):
    return render(request,'chapter_summary.html')

def level_choice(request):
    return render(request,'level_choice.html')

urlpatterns = [
    path("",level_choice),
    path("blank",blank),
    path("chapter_summary",chapter_summary),
    path("level_choice",level_choice),
    path("multiple",multiple),
    path("study",study),
    path("tfquiz",tfquiz),
    path("wrong_explanation",wrong_explanation),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)