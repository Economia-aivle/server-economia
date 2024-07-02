from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            # 로그인 실패 메시지 추가
            return render(request, 'admin_login.html', {'error': '잘못된 사용자 이름 또는 비밀번호입니다.'})
    return render(request, 'admin_login.html')

@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')