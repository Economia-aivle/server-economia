from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.urls import include
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)




urlpatterns = [
    path("", views.index, name='home'),  # Combined and named "home"
    path('educations/', include('educations.urls')),
    path('scenarios/', include('scenarios.urls')),
    path("chapter", views.chapter),
    path("mypage", views.mypage),
    path("onboarding", views.onboarding),
    path("update_info", views.update_info),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
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

# URL Patterns
urlpatterns = [
    path("", index),
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
