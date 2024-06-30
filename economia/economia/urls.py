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

urlpatterns = [
    path("",index),
    path("mode1/",index1),
    path("mode2/",index2),
    path("mode3/",index3),
    path("mode4/",index4),
    path("mode5/",index5)
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
