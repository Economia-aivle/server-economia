from django.shortcuts import render, redirect
from .form import PlayerForm
from .models import *
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import UserLoginSerializer
from django.http import HttpResponse
import jwt
from django.db.models import F, Window
from django.db.models.functions import Rank
from datetime import datetime, timedelta, timezone
from django.contrib import messages
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError

access_token = ""

def index(request):
    return render(request,'index.html')
def chapter(request):
    return render(request,'chapter.html')

def mypage(request):
    return render(request,'mypage.html')
def onboarding(request):
    return render(request,'onboarding.html')
def update_info(request):
    return render(request,'update_info.html')

#로그인 함수
class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data
            return Response(token, status=status.HTTP_200_OK)
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

#refresh token의 유효성 검사
def refresh_access_token(refresh_token):
    try:
        # Refresh Token 검증
        payload = jwt.decode(refresh_token, "economia", algorithms=['HS256'])
        user_id = payload['user_id']  # 예시에서는 payload에 사용자 ID가 포함되어 있다고 가정

        # 새로운 Access Token 생성
        access_token_payload = {
            'user_id': user_id,
            'exp': datetime.now(timezone.utc) + timedelta(minutes=30)  # Access Token의 유효 기간 설정 (예시: 30분)
        }
        access_token = jwt.encode(access_token_payload, "economia", algorithm='HS256')

        return access_token, refresh_token
    except jwt.ExpiredSignatureError:
        # Refresh Token이 만료된 경우 처리
        return {'error': 'refresh_token_expired'}
    except jwt.InvalidTokenError:
        # Refresh Token이 유효하지 않은 경우 처리
        return {'error': 'invalid_refresh_token'}


#홈화면
def home(request, subject_id):
    access_token = request.GET.get('token_access')
    refresh_token = request.GET.get('token_refresh')

    #레벨 계산
    def level(exp):
        total=int(exp)
        present=100
        lev = 0

        while(total-present) >= 0:
            total-=present
            lev+=1
            present+=100
        
        return total, present, lev
    
    #등수 계산
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
            # 여기서는 비밀 키를 사용하여 토큰을 디코드합니다. 비밀 키는 실제 비밀 키로 교체해야 합니다.
            decoded = jwt.decode(access_token, 'economia', algorithms=['HS256'])
            decoded['subjects_id'] = subject_id-1
            decoded['access_token'] = access_token
            decoded['refresh_token'] = refresh_token
            data = Player.objects.get(player_id=decoded['player_id'])
            serializer = ProductSerializer(data)
            data_character = Characters.objects.get(player_id=serializer.data['id'])
            serializer_character = CharacterSerializer(data_character)
            character_id = serializer_character.data['id']
            decoded['exp'] = serializer_character.data['exp']
            data_subject = Subjects.objects.all().values_list('subjects', flat=True)
            # serializer_subject = SubjectSerializer(data_subject)
            decoded['subjects'] = data_subject
            decoded['total'], decoded['present'],decoded['level'] = level(serializer_character.data['exp'])
            decoded['percent'] = int(100 * decoded['total'] / decoded['present'])

            #시나리오 정보 가져오기


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

            #기본 문제 정보 가져오기
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
                decoded['chapter']=tf.chapter
                decoded['kind'] = "빈칸 채우기"
            else:
                if blank.chapter != mul.chapter:
                    decoded['chapter']=blank.chapter
                    decoded['kind'] = "객관식"
                else:
                    decoded['chapter']=blank.chapter+1
                    decoded['kind'] = "OX"
                
                

            #과목에 맞는 스코어 가져오기
            decoded['score'] = SubjectsScore.objects.filter(characters=character_id, subjects=subject_id).first().score

            #등수 가져오기
            decoded['rank'] = get_ranking(subject_id, character_id)
            decoded['notice_list'] = NoticeBoard.objects.all()[:3]
                
            # Characters.objects.get(player_id=decodedplayer_id)
            # 디코드된 정보를 활용하여 원하는 작업을 수행합니다.
            return render(request, 'home.html', {'user': decoded})
        except jwt.ExpiredSignatureError:
            access_token, refresh_token = refresh_access_token(refresh_token)
            retry_count+=1
            return HttpResponse('Token has expired', status=401)
        except jwt.InvalidTokenError:
            retry_count+=1
            return HttpResponse('Invalid token', status=401)


def delete_account(request):
    print(request)
    try:
        # 현재 로그인한 사용자 가져오기
        player = Player.objects.get(email=request.user.email)

        # 관련된 데이터 삭제
        Characters.objects.filter(player=player).delete()
        ChildComments.objects.filter(player=player).delete()
        Comments.objects.filter(characters__player=player).delete()
        NoticeBoard.objects.filter(admin=player).delete()

        # 사용자 삭제
        player.delete()

        messages.success(request, "회원 탈퇴가 완료되었습니다.")
        return redirect('onboarding')
    except Player.DoesNotExist:
        messages.error(request, "사용자를 찾을 수 없습니다.")
        return redirect('mypage')


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
        if serializer.data['password'] != password:
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

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # jwt 토큰 접근
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
            
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)