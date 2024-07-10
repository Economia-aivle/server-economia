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

def admin_dashboard(request):
    return render(request,'admin_dashboard.html')
def admin_login(request):
    return render(request,'admin_login.html')

def ask(request):
    return render(request,'ask.html')
def service_agree(request):
    return render(request,'terms/service_agree.html')
def account_term(request):
    return render(request,'terms/account_term.html')
def community_term(request):
    return render(request,'terms/community_term.html')
def service_term(request):
    return render(request,'terms/service_term.html')
def teen_term(request):
    return render(request,'terms/teen_term.html')



urlpatterns = [
    path("",index),
    path('users/', include('users.urls')),
    path('educations/', include('educations.urls')),
    path('scenarios/', include('scenarios.urls')),
    path("chapter", chapter),
    path("home", home, name='home'),
    path("mypage", mypage, name='mypage'),
    path("onboarding", onboarding),
    path("update_info", update_info),
    path("admin_dashboard", admin_dashboard),
    path("admin_login", admin_login),
    path('community_term/', community_term, name='community_term'),
    path('account_term/', account_term, name='account_term'),
    path('service_term/', service_term, name='service_term'),
    path('teen_term/', teen_term, name='teen_term'),
    path('service_agree/', service_agree, name='service_agree'),
    path('ask', ask, name='ask'),

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)