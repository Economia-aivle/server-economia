from django.shortcuts import render, redirect
from .form import PlayerForm
from economia.models import Player
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string

verification_codes = {}

def delete_account(request):
    return render(request, 'delete_account.html')

def find_id(request):
    return render(request, 'find_id.html')

def send_code(request):
    email = request.POST.get('email')
    code = get_random_string(length=6, allowed_chars='1234567890')
    verification_codes[email] = code

    # 이메일로 인증번호 전송
    send_mail(
        '인증번호 발송',
        f'인증번호는 {code} 입니다.',
        'your_email@example.com',
        [email],
        fail_silently=False,
    )

    return JsonResponse({'message': '인증번호가 발송되었습니다.'})

def verify_code(request):
    email = request.POST.get('email')
    code = request.POST.get('code')

    if verification_codes.get(email) == code:
        user = User.objects.get(email=email)
        return JsonResponse({'success': True, 'username': user.username})
    else:
        return JsonResponse({'success': False, 'error': '인증번호가 올바르지 않습니다.'})

def show_id(request):
    username = request.GET.get('username')
    return render(request, 'show_id.html', {'username': username})

# Create your views here.
def char_create(request):
    return render(request,'char_create.html')

def char_delete(request):
    return render(request,'char_delete.html')

def notice(request):
    return render(request,'notice.html')

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
        user_id = request.POST.get('user_id')
        confirm_password = request.POST.get('confirm_password')
        password = request.POST.get('password')
        email = request.POST.get('email')
        name = request.POST.get('name')
        school_name = request.POST.get('school_name')
        nickname = request.POST.get('nickname')
        
        if Player.objects.filter(player_id=user_id).exists():
            return JsonResponse({'error': '중복된 아이디입니다.'}, status=400)
        if confirm_password != password:
            return JsonResponse({'error': '비밀번호를 다시 확인해주세요'}, status=400)
        if Player.objects.filter(email=email).exists():
            return JsonResponse({'error': '중복된 이메일입니다'}, status=400)
        if Player.objects.filter(nickname=nickname).exists():
            return JsonResponse({'error': '중복된 닉네임입니다'}, status=400)

        Player.objects.create(player_id=user_id, password=password, email=email, player_name=name, school=school_name, nickname=nickname, admin_tf=True)
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

