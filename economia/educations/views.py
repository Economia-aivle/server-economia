from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from economia.models import *
from .serializers import *
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


@api_view(['GET'])
def getBlankDatas(request, characters):
    datas = Blank.objects.filter(characters=characters)
    serializer = BlankSerializer(datas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getMultipleDatas(request, characters):
    datas = Multiple.objects.filter(characters=characters)
    serializer = MultipleSerializer(datas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTfDatas(request, characters):
    datas = Tf.objects.filter(characters=characters)
    serializer = TfSerializer(datas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSubjectDatas(request, subjects):
    datas = Subjects.objects.filter(subjects=subjects)
    serializer = SubjectSerializer(datas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getStageDatas(request, characters):
    datas = Stage.objects.filter(characters=characters)
    serializer = StageSerializer(datas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_next_blank(request, characters, subject, chapter, num):
    next_num = num + 1  # 다음 문제 번호 계산
    blank = get_object_or_404(Blank, characters=characters, subject=subject, chapter=chapter, num=next_num)
    serializer = BlankSerializer(blank)
    return JsonResponse(serializer.data)

def previous_quiz(request, characters):
    
    # player = request.player
    # characters = Characters.objects.get(player=player) #로그인한 player의 characters 속성을 가져옵니다.
    
    blank_response = requests.get(f'http://127.0.0.1:8000/educations/blankdatas/{characters}')
    blank_data = blank_response.json()

    # 두 번째 API 요청
    multiple_response = requests.get(f'http://127.0.0.1:8000/educations/multipledatas/{characters}')
    multiple_data = multiple_response.json()
    
    tf_response = requests.get(f'http://127.0.0.1:8000/educations/tfdatas/{characters}')
    tf_data = tf_response.json()

    # 템플릿에 데이터를 전달
    context = {
        'blank': blank_data,
        'multiple': multiple_data,
        'tf' : tf_data
    }
    return render(request, 'previous_quiz.html', context)


def previous_quiz_answer(request, characters):
    response = requests.get(f'http://127.0.0.1:8000/educations/multipledatas/{characters}')
    data = response.json()
    return render(request, 'previous_quiz_answer.html', {'multiple': data})

# Create your views here.
def level_choice(request, characters, subject, chapter):
    characters = 1
    try:
        stage_data = Stage.objects.get(characters_id=characters, subject=subject, chapter=chapter)
        chapter_sub = stage_data.chapter_sub
        print(type(chapter_sub))
    except Stage.DoesNotExist:
        chapter_sub = None
        print(chapter_sub)
    
    context = {
        'characters': characters,
        'subject': subject,
        'chapter': chapter,
        'chapter_sub': chapter_sub,
    }
    
    return render(request,'level_choice.html', context)

def tfquiz(request):
    return render(request,'tfquiz.html')


def multiple(request):
    return render(request,'multiple.html')

def previous_quiz_answer(request):
    return render(request,'previous_quiz_answer.html')

from django.shortcuts import render
import requests

def blank(request, characters, subject, chapter, num):
    blank_response = requests.get(f'http://127.0.0.1:8000/educations/blankdatas/{characters}')
    blank_data = blank_response.json()
    
    # characters, subject, chapter에 해당하는 데이터를 필터링합니다.
    blank_list = [item for item in blank_data if item['characters'] == characters and item['subjects'] == subject and item['chapter'] == chapter]

    # 최대 5개의 질문을 가져옵니다.
    questions = []
    max_num = min(5, len(blank_list))
    for i in range(max_num):
        blank_list[i]['num'] = i + 1
        questions.append(blank_list[i])
    
    # 현재 num에 해당하는 질문을 가져옵니다.
    question = questions[num - 1] if num <= max_num else None

    return render(request, 'blank.html', {'question': question, 'num': num, 'characters': characters, 'subject': subject, 'chapter': chapter})

    
def study(request):
    return render(request,'study.html')

def summary_anime(request):
    return render(request,'summary_anime.html')

def wrong_explanation(request):
    return render(request,'wrong_explanation.html')

def chapter_summary(request):
    return render(request,'chapter_summary.html')

def chapter(request, subjects):
    subjects='금융'
    response = requests.get(f'http://127.0.0.1:8000/educations/getSubjectDatas/{subjects}/')
    data = response.json()
    
    return render(request,'chapter.html', {'chapter': data})
