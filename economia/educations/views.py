from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from economia.models import *
from .serializers import *


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
def level_choice(request):
    return render(request,'level_choice.html')

def tfquiz(request):
    return render(request,'tfquiz.html')


def multiple(request):
    return render(request,'multiple.html')

def previous_quiz_answer(request):
    return render(request,'previous_quiz_answer.html')

def blank(request):
    return render(request,'blank.html')

def study(request):
    return render(request,'study.html')

def summary_anime(request):
    return render(request,'summary_anime.html')

def wrong_explanation(request):
    return render(request,'wrong_explanation.html')

def chapter_summary(request):
    return render(request,'chapter_summary.html')
