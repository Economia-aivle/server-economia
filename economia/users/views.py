from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from django.db import IntegrityError
from django.db.models import Q
from django.conf import settings
from django.contrib import messages
from rest_framework.decorators import api_view
from .form import PlayerForm
from .models import Player, Notice, Characters, VerificationCode, Subjects, SubjectsScore
from .serializers import CreateCharacterSerializer, SubjectsSerializer, SubjectsScoreSerializer
import json
import random
from django.http import JsonResponse, HttpResponseBadRequest
from django.db import IntegrityError
from django.conf import settings
from django.contrib import messages
import json
import random
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from economia.models import *
from .serializers import *


verification_codes = {}

def delete_account(request, player_id):
    if request.method == "POST":
        try:
            # player_id에 해당하는 플레이어 가져오기
            player = Player.objects.get(player_id=player_id)

            # 관련된 데이터 삭제
            Characters.objects.filter(player=player).delete()
            ChildComments.objects.filter(player=player).delete()
            Comments.objects.filter(characters__player=player).delete()
            Tf.objects.filter(characters__player=player).delete()
            Blank.objects.filter(characters__player=player).delete()
            Multiple.objects.filter(characters__player=player).delete()
            Stage.objects.filter(characters__player=player).delete()
            SubjectsScore.objects.filter(characters__player=player).delete()
            Blank.objects.filter(characters__player=player).delete()

            # 플레이어 삭제
            player.delete()

            messages.success(request, "회원 탈퇴가 완료되었습니다.")
            return redirect('onboarding')  # 회원 탈퇴 후 리디렉션할 페이지
        except Player.DoesNotExist:
            messages.error(request, "사용자를 찾을 수 없습니다.")
            return redirect('mypage')  # 에러 발생 시 리디렉션할 페이지

    return render(request, 'delete_account.html', {'player_id': player_id})

def find_id(request):
    return render(request, 'find_id.html')

def send_code(request):
    email = request.POST.get('email')
    code = get_random_string(length=6, allowed_chars='1234567890')
    verification_codes[email] = code

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

def notice(request):
    return render(request, 'notice.html')

def char_create(request):
    return render(request, 'char_create.html')

def char_delete(request):
    return render(request, 'char_delete.html')

def check_username(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if Player.objects.filter(player_id=user_id).exists():
            return JsonResponse({'available': False})
        else:
            return JsonResponse({'available': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def register(request):
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

def signup(request):
    return render(request, 'signup.html')

def find_account_pwd(request):
    return render(request, 'find_account_pwd.html')

def find_account_id(request):
    return render(request, 'find_account_id.html')

def find_account(request):
    return render(request, 'find_account.html')

def check_id(request):
    return render(request, 'check_id.html')

@csrf_exempt
def get_character_view(request, player_id):
    if request.method == 'GET':
        try:
            character = Characters.objects.get(player_id=player_id)
            return JsonResponse({"id": character.id, "kind": character.kind, "kind_url": character.kind_url}, status=200)
        except Characters.DoesNotExist:
            return JsonResponse({"error": "Character not found"}, status=404)
    return HttpResponseBadRequest("Invalid request method")

# 캐릭터 생성하기
@csrf_exempt
def character_create_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        player_id = data.get('player_id')
        if not player_id:
            return JsonResponse({"error": "Missing player_id"}, status=400)

        existing_character = Characters.objects.filter(player_id=player_id).first()
        if existing_character:
            return JsonResponse({"error": "Character already exists for this player"}, status=400)

        serializer = CreateCharacterSerializer(data=data)
        if serializer.is_valid():
            try:
                character = serializer.save()
                return JsonResponse({"id": character.id, **serializer.data}, status=201)
            except IntegrityError:
                return JsonResponse({"error": "Character creation failed. Possible duplicate."}, status=400)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'GET':
        return render(request, 'char_create.html')
    return HttpResponseBadRequest("Invalid request method")

@csrf_exempt
def character_update_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        character_id = data.get('character_id')
        new_image_url = data.get('new_image_url')

        if not character_id or not new_image_url:
            return JsonResponse({"error": "Missing character_id or new_image_url"}, status=400)

        try:
            character = Characters.objects.get(pk=character_id)
        except Characters.DoesNotExist:
            return JsonResponse({"error": "Character not found"}, status=404)

        character.kind_url = new_image_url
        character.save()
        return JsonResponse({"message": "Character image updated successfully"}, status=200)

    return HttpResponseBadRequest("Invalid request method")

@api_view(['GET'])
def getSubjectsDatas(request):
    datas = Subjects.objects.all()
    serializer = SubjectsSerializer(datas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSubjectsScoreDatas(request, subject_id):
    scores = SubjectsScore.objects.filter(subjects_id=subject_id).order_by('-score')
    if not scores.exists():
        return Response({"error": "No data found for the given subject_id"}, status=404)

    serializer = SubjectsScoreSerializer(scores, many=True)
    
    ranked_scores = []
    current_rank = 1
    current_score = None

    for i, score in enumerate(serializer.data):
        if current_score != score['score']:
            current_rank = i + 1
            current_score = score['score']
        ranked_scores.append({
            'rank': current_rank,
            'nickname': score['characters']['player']['nickname'],
            'school': score['characters']['player']['school'],
            'score': score['score']
        })

    return Response(ranked_scores)

def ranking(request):
    subjects = Subjects.objects.all()
    first_subject_id = subjects[0].id if subjects else None

    if first_subject_id:
        scores_response = getSubjectsScoreDatas(request, first_subject_id)
        ranked_scores = scores_response.data
    else:
        ranked_scores = []

    return render(request, 'ranking.html', {'subjects': subjects, 'ranked_scores': ranked_scores})

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
    search_query = request.GET.get('search', '')
    notices = Notice.objects.all().order_by('-created_at')
    
    if search_query:
        notices = notices.filter(Q(title__icontains=search_query))
    
    return render(request, 'notice.html', {'notices': notices, 'search_query': search_query})

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

def generate_verification_code():
    return str(random.randint(100000, 999999))

def find_account_id(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        action = request.POST.get('action', '')

        if action == 'resend':
            verification_code = generate_verification_code()
            VerificationCode.objects.update_or_create(email=email, defaults={'code': verification_code})

            send_mail(
                'Your Verification Code',
                f'Your verification code is {verification_code}.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return JsonResponse({'status': 'success', 'message': '인증 코드가 전송되었습니다.'})
        
        elif action == 'check':
            try:
                stored_code = VerificationCode.objects.get(email=email).code
                if stored_code == code:
                    user = Player.objects.get(email=email)
                    return JsonResponse({'status': 'success', 'user_id': user.player_id})
                else:
                    return JsonResponse({'status': 'error', 'message': '잘못된 인증 코드입니다.'})
            except VerificationCode.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': '이메일로 발송된 인증 코드가 없습니다.'})

    return render(request, 'find_account_id.html')

def check_id(request, player_id):
    return render(request, 'check_id.html', {'player_id': player_id})
