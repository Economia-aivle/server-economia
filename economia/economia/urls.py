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
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth.views import LogoutView

def index(request):
    return render(request,'index.html')
def chapter(request):
    return render(request,'chapter.html')
def home(request):
    return render(request,'home.html')
def mypage(request):
    return render(request,'mypage.html')
def onboarding(request):
    return render(request,'onboarding.html')
def update_info(request):
    return render(request,'update_info.html')



urlpatterns = [
    path("",index),
    path('users/', include('users.urls')),
    path('educations/', include('educations.urls')),
    path('scenarios/', include('scenarios.urls')),
    path("chapter", chapter),
    path("home", home),
    path("mypage", mypage),
    path("onboarding", onboarding),
    path("update_info", update_info),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)