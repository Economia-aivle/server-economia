from django.shortcuts import render, redirect
from .form import PlayerForm
from .models import Player
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer

# Create your views here.
def char_create(request):
    return render(request,'char_create.html')

def char_delete(request):
    return render(request,'char_delete.html')

def check_username(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if Player.objects.filter(player_id=user_id).exists():
            return JsonResponse({'available': False})
        else:
            return JsonResponse({'available': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def register(request):  # 함수 이름을 'register'로 변경
    if request.method == 'POST':
        user_id = request.POST.get('user_id1')
        password = request.POST.get('password1')
        
        if not Player.objects.filter(player_id=user_id).exists():
            return JsonResponse({'error': '존재하지 않는 아이디입니다.'}, status=400)
        data = Player.objects.get(player_id=user_id)
        serializer = ProductSerializer(data)
        if serializer.data['pwd'] != password:
            return JsonResponse({'error': '비밀번호를 다시 확인해주세요'}, status=400)
        return JsonResponse({'success': '회원가입이 완료되었습니다.'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def signup(request):  # 함수 이름을 'signup'으로 변경
    return render(request, 'signup.html')  # 템플릿 이름을 'signup.html'로 변경

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

def success(request):
    return render(request,'success.html')

