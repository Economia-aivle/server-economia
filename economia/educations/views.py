from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from economia.models import *
from .serializers import *
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


def multiple(request, characters, subject, chapter, num):
    # characters, subject, chapter에 해당하는 데이터를 필터링합니다.
    multiple_response = requests.get(f'http://127.0.0.1:8000/educations/multipledatas/{characters}')
    multiple_data = multiple_response.json()
    
    multiple_list = [item for item in multiple_data if item['characters'] == characters and item['subjects'] == subject and item['chapter'] == chapter]
    
    questions = []
    max_num = min(5, len(multiple_list))
    for i in range(max_num):
        multiple_list[i]['num'] = i + 1
        questions.append(multiple_list[i])
    
    question = questions[num - 1] if num <= max_num else None
    
    if num == 6:
        return redirect('educations:level_choice', characters=characters, subject=subject, chapter=chapter)
    # # POST 요청 처리
    if request.method == 'POST':
        user_answer = request.POST.get('answer')
        correct_answer = question['correct_answer']
        
        if user_answer == correct_answer:
            # 정답인 경우
            correct_count = request.session.get('correct_count', 0) + 1
            request.session['correct_count'] = correct_count
            print(correct_count)
            if correct_count == 5:
                # 모든 문제를 맞춘 경우 Stage 모델의 chapter_sub를 3으로 업데이트
                try:
                    stage_data = Stage.objects.get(characters_id=characters, subject=subject, chapter=chapter)
                    stage_data.chapter_sub = 3
                    stage_data.save()
                except Stage.DoesNotExist:
                    pass
                
                # 세션 초기화
                request.session['correct_count'] = 0

                # JSON 응답 전송
                return JsonResponse({'status': 'complete', 'message': '모든 문제를 맞췄습니다!'})
            else:
                # 아직 모든 문제를 맞추지 않은 경우
                return JsonResponse({'status': 'correct', 'message': '정답입니다.'})
        else:
            # 오답인 경우
            return JsonResponse({'status': 'wrong', 'message': '오답입니다.'})
   
    # GET 요청 처리
    return render(request, 'multiple.html', {'question': question, 'num': num, 'characters': characters, 'subject': subject, 'chapter': chapter})



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
