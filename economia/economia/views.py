from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.models import LogEntry
from django.contrib import messages

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, '잘못된 사용자 이름 또는 비밀번호입니다.')
    return render(request, 'admin_login.html')

@login_required
def admin_dashboard(request):
    recent_actions = LogEntry.objects.all()[:10]  # 최근 10개의 활동을 가져옵니다
    context = {
        'user': request.user,
        'recent_actions': recent_actions,
    }
    return render(request, 'admin_dashboard.html', context)

def admin_logout(request):
    logout(request)
    return redirect('admin_login')