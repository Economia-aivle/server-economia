from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

def index(request):
    return render(request, 'index.html')

def chapter(request):
    return render(request, 'chapter.html')

def home(request):
    return render(request, 'home.html')

def mypage(request):
    return render(request, 'mypage.html')

def onboarding(request):
    return render(request, 'onboarding.html')

def update_info(request):
    return render(request, 'update_info.html')

# URL Patterns
urlpatterns = [
    path("", index),
    path('users/', include('users.urls')),
    path('educations/', include('educations.urls')),
    path('scenarios/', include('scenarios.urls')),
    path("chapter", chapter),
    path("home", home),
    path("mypage", mypage),
    path("onboarding", onboarding),
    path("update_info", update_info),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
