from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.urls import include
from django.conf import settings
from . import views
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)




urlpatterns = [
    path("", views.index),
    path('users/', include('users.urls')),
    path('educations/', include('educations.urls')),
    path('scenarios/', include('scenarios.urls')),
    path("chapter", views.chapter),
    path("home/<int:subject_id>", views.home, name='home'),
    path("mypage", views.mypage),
    path("onboarding", views.onboarding),
    path("onboarding/re", views.LoginView.as_view(), name='login'),
    path("onboarding/logout", views.LogoutView.as_view(), name='logout'),
    path("update_info", views.update_info),
    path('register', views.register, name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]



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
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
