from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
import requests
from economia.models import *
from .serializers import *
from datetime import datetime, timedelta
import pytz
import jwt
from .forms import ScenarioForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from economia.serializers import ProductSerializer, CharacterSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
# Create your views here.

class ProtectedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'This is a protected view'}
        return Response(content)


@api_view(['GET'])
def getScenarioDatas(request):
    datas = Scenario.objects.all()
    serializer = ScenarioSerializer(datas, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
def getScenarioData(request, id):
    datas = Scenario.objects.filter(id=id)
    serializer = ScenarioSerializer(datas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getCommentData(request, scenario):
    datas = Comments.objects.filter(scenario=scenario)
    serializer = CommentsSerializer(datas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getChildCommentData(request, comments_id):
    datas = ChildComments.objects.filter(parent=comments_id)
    serializer = ChildCommentsSerializer(datas, many=True)
    return Response(serializer.data)

@api_view(['POST']) #대댓글 입력 폼
def submit_childcomment(request):
    parent_id = request.POST.get('parent_id')
    text = request.POST.get('childcomment_text')
    player_id = get_player(request, 'player')
    image = request.FILES.get('image')
    
    if image:
        valid_extensions = ['jpg', 'jpeg', 'gif', 'png', 'webp']
        extension = image.name.split('.')[-1].lower()
        if extension not in valid_extensions:
            return JsonResponse({'error': '지원되지 않는 파일 형식입니다.'}, status=405)
    child_comment = ChildComments(parent_id=parent_id, player_id=player_id, texts=text, imgfile=image)
    child_comment.save()
    scenario_id = request.POST.get('scenario_id')
    return redirect('scenarios:previous_scenario', id=scenario_id)

@api_view(['POST']) # 댓글 지우기
def delete_comment(request, id):
    comment = get_object_or_404(Comments, id=id)
    comment.delete()
    return redirect('scenarios:previous_scenario', id=request.POST.get('scenario_id'))

@api_view(['POST']) # 대댓글 지우기
def delete_childcomment(request, id):
    childcomment = get_object_or_404(ChildComments, id=id)
    childcomment.delete()
    return redirect('scenarios:previous_scenario', id=request.POST.get('scenario_id'))

def scenario_list(request):
    staff = get_staff(request)
    print(staff)
    scenario_response = requests.get('http://127.0.0.1:8000/scenarios/scenario_datas')
    scenario_data = scenario_response.json()
    
    query = request.GET.get('search', '')
    
    if query:
        scenario_data = [item for item in scenario_data if query.lower() in item['title'].lower()]

    for item in scenario_data:
        start_time = datetime.strptime(item['start_time'], '%Y-%m-%dT%H:%M:%S%z')
        start_time_utc = start_time.astimezone(pytz.utc)
        
        if start_time_utc + timedelta(days=7) < timezone.now():
            item['is_overdue'] = True
        else:
            item['is_overdue'] = False

        item['start_time_utc'] = start_time_utc

    scenario_data.sort(key=lambda x: x['start_time_utc'], reverse=True)

    paginator = Paginator(scenario_data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'is_staff': staff,
    }

    return render(request, 'scenario_list.html', context)

def scenario(request, id):
    response = requests.get(f'http://127.0.0.1:8000/scenarios/scenario/{id}')
    data = response.json()
    return render(request, 'scenario.html', {'scenario': data})

def create_scenario(request): #시나리오 생성
    if request.method == 'POST':
        form = ScenarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('scenarios:scenario_list')  # Assuming you have a view to list scenarios
    else:
        form = ScenarioForm()
    return render(request, 'create_scenario.html', {'form': form})



def previous_scenario(request, id):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')

    # 디버깅 로그 추가
    print("Access Token:", access_token)
    print("Refresh Token:", refresh_token)
    
    if not access_token:
        return JsonResponse({"error": "토큰이 없습니다."}, status=400)
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    characters_id = get_player(request, 'characters')
    player_id = get_player(request, 'player')
    # Scenario 데이터 가져오기
    scenario_response = requests.get(f'http://127.0.0.1:8000/scenarios/scenario/{id}', headers=headers)
    scenario_data = scenario_response.json()
    
    # 각 항목의 start_time을 UTC로 변환하고 is_overdue 필드를 추가
    for item in scenario_data:
        start_time = datetime.strptime(item['start_time'], '%Y-%m-%dT%H:%M:%S%z')
        start_time_utc = start_time.astimezone(pytz.utc)  # UTC로 변환
        
        if start_time_utc + timedelta(days=7) < timezone.now():
            item['is_overdue'] = True
        else:
            item['is_overdue'] = False

        # UTC로 변환된 start_time을 item에 추가 (정렬용)
        item['start_time_utc'] = start_time_utc

    # start_time_utc 기준으로 내림차순 정렬
    scenario_data.sort(key=lambda x: x['start_time_utc'], reverse=True)
    
    # Comment 데이터 가져오기
    comment_response = requests.get(f'http://127.0.0.1:8000/scenarios/comment_datas/{id}')
    comment_data = comment_response.json()
    
    comments = Comments.objects.filter(scenario_id=id).select_related('characters__player')
    
     # 각 Comment에 대해 좋아요 여부 확인 및 Player 닉네임 가져오기
    comment_data_updated = []
    for comment in comments:
        is_liked_by_user = CommentsLikes.objects.filter(comment_id=comment.id, player_id=player_id).exists()
        comment_data_updated.append({
            'id': comment.id,
            'scenario_id': comment.scenario_id,
            'characters_id': comment.characters_id,
            'percents': comment.percents,
            'texts': comment.texts,
            'like_cnt': comment.like_cnt,
            'is_liked_by_user': is_liked_by_user,
            'player_nickname': comment.characters.player.nickname  # Player 닉네임 추가
        })
    
    childcomment_data = []
    
    comments = Comments.objects.filter(scenario_id=id)
    # 특정 캐릭터가 작성한 댓글이 있는지 확인
    has_character_comment = comments.filter(characters_id=characters_id).exists()
    
    # 각 Comment에 대해 좋아요 여부 확인 및 Child Comment 데이터 가져오기
    # for comment in comment_data:
    #     # 좋아요 여부 확인
    #     is_liked_by_user = CommentsLikes.objects.filter(comment_id=comment['id'], player_id=player_id).exists()
    #     comment['is_liked_by_user'] = is_liked_by_user
        
    # Child Comment 데이터 가져오기
    child_comments = ChildComments.objects.select_related('player').filter(parent__in=[comment['id'] for comment in comment_data]).order_by('id')
    
    for child in child_comments:
        childcomment_data.append({
            'id': child.id,
            'parent_id': child.parent_id,
            'player_id': child.player_id,
            'texts': child.texts,
            'player_nickname': child.player.nickname,
            'img' : child.imgfile
        })
    
    context = {
        'scenario': scenario_data,
        'comment': comment_data_updated,
        'childcomment': childcomment_data,
        'characters_id' : characters_id,
        'player_id' : player_id,
        'has_character_comment': has_character_comment,
    }
    
    return render(request, 'previous_scenario.html', context)

@require_POST
@csrf_exempt
def like_comment(request, comment_id):
    if request.method == 'POST':
        player_id = get_player(request, 'player') # 임시로 사용자 ID를 1로 설정
        
        comment = get_object_or_404(Comments, id=comment_id)
        player = get_object_or_404(Player, id=player_id)
        
        try:
            # 사용자가 해당 댓글에 좋아요를 했는지 확인
            is_liked_by_user = CommentsLikes.objects.filter(comment=comment, player=player).exists()
            
            if is_liked_by_user:
                # 이미 좋아요를 눌렀으면 좋아요 취소
                CommentsLikes.objects.filter(comment=comment, player=player).delete()
                comment.like_cnt = comment.like_cnt - 1 if comment.like_cnt else 0
                action = 'unliked'
            else:
                # 좋아요를 처음 누른 경우
                CommentsLikes.objects.create(comment=comment, player=player)
                comment.like_cnt = comment.like_cnt + 1 if comment.like_cnt else 1
                action = 'liked'
            
            comment.save()
            return JsonResponse({'success': True, 'like_cnt': comment.like_cnt, 'action': action})
        
        except CommentsLikes.DoesNotExist:
            return JsonResponse({'error': 'Failed to process like/unlike action.'}, status=500)
    
    return JsonResponse({'error': 'Method not allowed.'}, status=405)

def submit_answer(request): #시나리오 답 제출
    if request.method == 'POST':
        scenario_id = request.POST.get('scenario_id')
        scenario_answer = request.POST.get('scenario_answer')
        characters_id = get_player(request, 'characters')
        # Assume characters_id is fixed as 1 for testing purposes

        # Create a new Comment object
        new_comment = Comments(
            scenario_id=scenario_id,
            characters_id=characters_id,
            percents=0,  # Adjust the percents field as needed
            texts=scenario_answer,
            like_cnt=0
        )
        new_comment.save()

        return redirect('scenarios:previous_scenario', id=scenario_id)

    return redirect('scenarios:scenario_list')

def get_player(request, id):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')

    # 디버깅 로그 추가
    print("Access Token:", access_token)
    print("Refresh Token:", refresh_token)
    
    if not access_token:
        return JsonResponse({"error": "토큰이 없습니다."}, status=400)
    
    decoded = jwt.decode(access_token, 'economia', algorithms=['HS256'])
    decoded['access_token'] = access_token
    player = Player.objects.get(player_id=decoded['player_id'])
    player_id = player.id
    character = get_object_or_404(Characters, player_id=player_id)
    characters_id = character.id
    print(characters_id)
    print(player_id)
    if id == 'player':
        return player_id
    elif id == 'characters':
        return characters_id
    else:
        return player_id
    
def get_staff(request):
    id = get_player(request, 'player')
    player = Player.objects.get(id=id)
    staff = player.is_staff
    return staff