from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from django.contrib import messages
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .form import PlayerForm
from .models import *
from .serializers import UserLoginSerializer, ProductSerializer, CharacterSerializer
from datetime import datetime, timedelta, timezone
import jwt
from django.db.models import F, Window
from django.db.models.functions import Rank
from rest_framework.response import Response
from django.middleware.csrf import get_token

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

def index(request):
    return render(request, 'index.html')

def chapter(request):
    return render(request, 'chapter.html')

def mypage(request):
    return render(request, 'mypage.html')

def onboarding(request):
    return render(request, 'onboarding.html')

def update_info(request):
    return render(request, 'update_info.html')

class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data
            response = Response(token, status=status.HTTP_200_OK)
            response.set_cookie('access_token', token['access'], httponly=True, samesite='Lax')
            response.set_cookie('refresh_token', token['refresh'], httponly=True, samesite='Lax')
            response.set_cookie('csrftoken', get_token(request), samesite='Lax')
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        try:
            access_token = request.data.get('access_token')
            refresh_token = request.data.get('refresh_token')

            if not access_token or not refresh_token:
                return Response({"detail": "Missing access_token or refresh_token in request body"}, status=status.HTTP_400_BAD_REQUEST)

            access_token_obj = AccessToken(access_token)
            access_token_obj.set_exp(from_time=datetime.now())

            refresh_token_obj = RefreshToken(refresh_token)
            refresh_token_obj.set_exp(from_time=datetime.now())

            return Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)

        except TokenError as e:
            return Response({"detail": f"TokenError: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

def refresh_access_token(refresh_token):
    try:
        payload = jwt.decode(refresh_token, "economia", algorithms=['HS256'])
        user_id = payload['user_id']
        access_token_payload = {
            'user_id': user_id,
            'exp': datetime.now(timezone.utc) + timedelta(minutes=30)
        }
        access_token = jwt.encode(access_token_payload, "economia", algorithm='HS256')
        return access_token, refresh_token
    except jwt.ExpiredSignatureError:
        return {'error': 'refresh_token_expired'}
    except jwt.InvalidTokenError:
        return {'error': 'invalid_refresh_token'}

def home(request, subject_id):
    access_token = request.GET.get('token_access')
    refresh_token = request.GET.get('token_refresh')
    
    def level(exp):
        total = int(exp)
        present = 100
        lev = 0

        while (total - present) >= 0:
            total -= present
            lev += 1
            present += 100
        
        return total, present, lev
    
    def get_ranking(subject_id, character_id):
        scores = list(
            SubjectsScore.objects.filter(subjects=subject_id).annotate(
                rank=Window(
                    expression=Rank(),
                    order_by=F('score').desc()
                )
            )
        )
        target_index = None
        for index, obj in enumerate(scores):
            if obj.characters.id == character_id:
                target_index = index
                break
        
        return target_index

    if not access_token:
        return HttpResponse('Token is missing', status=400)
    retry_count = 0
    while retry_count < 2:
        try:
            decoded = jwt.decode(access_token, 'economia', algorithms=['HS256'])
            decoded['subjects_id'] = subject_id - 1
            decoded['access_token'] = access_token
            decoded['refresh_token'] = refresh_token
            data = Player.objects.get(player_id=decoded['player_id'])
            serializer = ProductSerializer(data)
            data_character = Characters.objects.get(player_id=serializer.data['id'])
            serializer_character = CharacterSerializer(data_character)
            character_id = serializer_character.data['id']
            decoded['exp'] = serializer_character.data['exp']
            data_subject = Subjects.objects.all().values_list('subjects', flat=True)
            decoded['subjects'] = data_subject
            decoded['total'], decoded['present'], decoded['level'] = level(serializer_character.data['exp'])
            decoded['percent'] = int(100 * decoded['total'] / decoded['present'])

            decoded['scenario_list'] = Scenario.objects.filter(subjects=subject_id).annotate(
                rank=Window(
                    expression=Rank(),
                    order_by=F('start_time').desc()
                )
            )[:3]
            scenario_ids = Scenario.objects.filter(subjects=subject_id).values_list('id', flat=True)
            decoded['comment_list'] = Comments.objects.filter(scenario_id__in=scenario_ids).annotate(
                rank=Window(
                    expression=Rank(),
                    order_by=F('time').desc()
                )
            )[:3]

            decoded['multiple_list'] = Multiple.objects.filter(characters=character_id, subjects=subject_id)
            decoded['tf_list'] = Tf.objects.filter(characters=character_id, subjects=subject_id)
            decoded['blank_list'] = Blank.objects.filter(characters=character_id, subjects=subject_id)
            mul = Multiple.objects.filter(characters=character_id, subjects=subject_id).annotate(
                rank=Window(
                    expression=Rank(),
                    order_by=F('chapter').desc()
                )
            ).first()
            tf = Tf.objects.filter(characters=character_id, subjects=subject_id).annotate(
                rank=Window(
                    expression=Rank(),
                    order_by=F('chapter').desc()
                )
            ).first()
            blank = Blank.objects.filter(characters=character_id, subjects=subject_id).annotate(
                rank=Window(
                    expression=Rank(),
                    order_by=F('chapter').desc()
                )
            ).first()
            decoded['chapter_tf'] = tf.chapter
            decoded['chapter_blank'] = blank.chapter
            decoded['chapter_mul'] = mul.chapter

            if tf.chapter != blank.chapter:
                decoded['chapter'] = tf.chapter
                decoded['kind'] = "빈칸 채우기"
            else:
                if blank.chapter != mul.chapter:
                    decoded['chapter'] = blank.chapter
                    decoded['kind'] = "객관식"
                else:
                    decoded['chapter'] = blank.chapter + 1
                    decoded['kind'] = "OX"

            decoded['score'] = SubjectsScore.objects.filter(characters=character_id, subjects=subject_id).first().score
            decoded['rank'] = get_ranking(subject_id, character_id)
            decoded['notice_list'] = NoticeBoard.objects.all()[:3]

            return render(request, 'home.html', {'user': decoded})
        except jwt.ExpiredSignatureError:
            access_token, refresh_token = refresh_access_token(refresh_token)
            retry_count += 1
            return HttpResponse('Token has expired', status=401)
        except jwt.InvalidTokenError:
            retry_count += 1
            return HttpResponse('Invalid token', status=401)

def delete_account(request):
    try:
        player = Player.objects.get(email=request.user.email)
        Characters.objects.filter(player=player).delete()
        ChildComments.objects.filter(player=player).delete()
        Comments.objects.filter(characters__player=player).delete()
        NoticeBoard.objects.filter(admin=player).delete()
        player.delete()

        messages.success(request, "회원 탈퇴가 완료되었습니다.")
        return redirect('onboarding')
    except Player.DoesNotExist:
        messages.error(request, "사용자를 찾을 수 없습니다.")
        return redirect('mypage')

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
        user_id = request.POST.get('user_id1')
        password = request.POST.get('password1')

        if not Player.objects.filter(player_id=user_id).exists():
            return JsonResponse({'error': '존재하지 않는 아이디입니다.'}, status=400)
        data = Player.objects.get(player_id=user_id)
        serializer = ProductSerializer(data)
        if serializer.data['password'] != password:
            return JsonResponse({'error': '비밀번호를 다시 확인해주세요'}, status=400)
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

def ranking(request):
    return render(request, 'ranking.html')

def success(request):
    return render(request, 'success.html')

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )

            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)

            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
