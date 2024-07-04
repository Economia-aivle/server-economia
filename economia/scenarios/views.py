from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
import requests
from economia.models import *
from .serializers import *
from datetime import datetime, timedelta
import pytz
from .forms import ScenarioForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


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

    # 테스트 용이므로 player_id 1로 고정
    child_comment = ChildComments(parent_id=parent_id, player_id=1, texts=text)
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
    scenario_response = requests.get('http://127.0.0.1:8000/scenarios/scenario_datas')
    scenario_data = scenario_response.json()

    
    for item in scenario_data:
        start_time = datetime.strptime(item['start_time'], '%Y-%m-%dT%H:%M:%S%z')
        start_time_utc = start_time.astimezone(pytz.utc)  # UTC로 변환
        
        if start_time_utc + timedelta(days=7) < timezone.now():
            item['is_overdue'] = True
        else:
            item['is_overdue'] = False
    
    return render(request, 'scenario_list.html', {'scenarios': scenario_data})

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

def previous_scenario(request,id):
    response = requests.get(f'http://127.0.0.1:8000/scenarios/scenario/{id}')
    scenario_data = response.json()
    
    response = requests.get(f'http://127.0.0.1:8000/scenarios/comment_datas/{id}')
    comment_data = response.json()
    
    childcomment_data = []

    # Fetch child comment data for each comment
    for comment in comment_data:
        response = requests.get(f'http://127.0.0.1:8000/scenarios/childcomment_datas/{comment["id"]}')
        childcomment_data.extend(response.json())
    
    context = {
        'scenario': scenario_data,
        'comment': comment_data,
        'childcomment': childcomment_data,
    }
    
    return render(request,'previous_scenario.html', context)

@csrf_exempt
def like_comment(request): #comment 좋아요
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment = Comments.objects.get(id=comment_id)
        comment.like_cnt += 1
        comment.save()
        return JsonResponse({'success': True, 'like_cnt': comment.like_cnt})
    return JsonResponse({'success': False})

def submit_answer(request): #시나리오 답 제출
    if request.method == 'POST':
        scenario_id = request.POST.get('scenario_id')
        scenario_answer = request.POST.get('scenario_answer')

        # Assume characters_id is fixed as 1 for testing purposes
        characters_id = 1

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