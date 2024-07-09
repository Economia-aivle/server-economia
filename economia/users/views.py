from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Notice


# Create your views here.
def char_create(request):
    return render(request,'char_create.html')

def char_delete(request):
    return render(request,'char_delete.html')

def signup(request):
    return render(request,'signup.html')

def find_account_pwd(request):
    return render(request,'find_account_pwd.html')

def find_account_id(request):
    return render(request,'find_account_id.html')

def find_account(request):
    return render(request,'find_account.html')

def check_id(request):
    return render(request,'check_id.html')

def ranking(request):
    return render(request,'ranking.html')

# 추가된 뷰 함수들
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid credentials or not an admin'})
    return render(request, 'admin_login.html')


def notice_list(request):
    notices = Notice.objects.all().order_by('-created_at')
    return render(request, 'notice.html', {'notices': notices})


def notice_detail(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    return render(request, 'notice_detail.html', {'notice': notice})
@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

class AdminLoginAPI(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials or not an admin"}, status=status.HTTP_400_BAD_REQUEST)
        
        

