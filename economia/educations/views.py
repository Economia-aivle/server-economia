from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from economia.models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
import random


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


@csrf_exempt
def tf_quiz_view(request):
    if request.method == 'GET':
        used_question_ids = request.GET.getlist('used_question_ids[]')
        chapter = request.GET.get('chapter')
        subjects = request.GET.get('subjects')  # 수정된 부분
        characters = request.GET.get('characters')

        if not chapter or not subjects:
            return JsonResponse({"error": "Chapter and subjects are required."}, status=status.HTTP_400_BAD_REQUEST)

        questions = Tf.objects.filter(chapter=chapter, subjects=subjects).exclude(id__in=used_question_ids)
        if not questions:
            return JsonResponse({"error": "No questions available."}, status=status.HTTP_404_NOT_FOUND)
        question = random.choice(questions)

        context = {
            "question_id": question.id,
            "question_text": question.question_text,
            "correct_answer": question.correct_answer,
            "explanation": question.explanation
        }
        return JsonResponse(context, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        question_id = request.POST.get('question_id')
        submitted_answer = request.POST.get('submitted_answer')

        if not question_id:
            return JsonResponse({"error": "Question ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            question = Tf.objects.get(id=question_id)
        except Tf.DoesNotExist:
            return JsonResponse({"error": "Question not found."}, status=status.HTTP_404_NOT_FOUND)

        correct_answer = question.correct_answer
        is_correct = submitted_answer.upper() == correct_answer.upper()
        
        response_data = {
            "question_id": question.id,
            "submitted_answer": submitted_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "explanation": question.explanation if not is_correct else None
        }
        if is_correct:
            correct_count = request.session.get('correct_count', 0) + 1
            request.session['correct_count'] = correct_count
            print(correct_count)

            if correct_count == 5:
                # 모든 문제를 맞췄을 때 Stage 모델 업데이트
                try:
                    stage = Stage.objects.get(characters_id=characters, subject=subjects, chapter=chapter)
                    stage.chapter_sub = 2
                    stage.save()
                except Stage.DoesNotExist:
                    pass  # Stage가 없는 경우 pass

                # 세션 초기화
                request.session['correct_count'] = 0

                return JsonResponse({'status': 'complete', 'message': '모든 문제를 맞췄습니다!'})

            return JsonResponse(response_data, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)

def tf_quiz_page(request, characters, subject, chapter):
    context = {
            'characters': characters,
              'subject': subject,
              'chapter': chapter,
    } 
    return render(request, 'tfquiz.html', context)

def choose_tf_chapter_view(request):
    if request.method == 'POST':
        chapter = request.POST.get('chapter')
        if not chapter:
            return JsonResponse({"error": "Chapter number is required."}, status=status.HTTP_400_BAD_REQUEST)

        questions = Tf.objects.filter(chapter=chapter)[:5]  # 챕터별 문제 5개 가져오기

        if not questions:
            return JsonResponse({"error": "No questions found for the selected chapter."},
                                status=status.HTTP_404_NOT_FOUND)

        question_data = [{
            "id": question.id,
            "question_text": question.question_text,
            "correct_answer": question.correct_answer,
            "explanation": question.explanation
        } for question in questions]

        return JsonResponse({"questions": question_data}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
    



def multiple(request, characters, subject, chapter, num):
    # characters, subject, chapter에 해당하는 데이터를 필터링합니다.
    multiple_response = requests.get(f'http://127.0.0.1:8000/educations/multipledatas/{characters}')
    multiple_data = multiple_response.json()
    
    multiple_list = [item for item in multiple_data if item['characters'] == characters and item['subjects'] == subject and item['chapter'] == chapter]
    
    questions = []
    max_num = min(8, len(multiple_list))
    for i in range(max_num):
        multiple_list[i]['num'] = i + 1
        questions.append(multiple_list[i])
    
    question = questions[num - 1] if num <= max_num else None
    
    if num == 9:
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
    correct_count = request.session.get('correct_count', 0)
    hp_percentage = max(0, 100 - (correct_count * 20))  # 체력 퍼센트 계산
    
    context ={'question': question,
              'num': num,
              'characters': characters,
              'subject': subject,
              'chapter': chapter,
              'correct_count': correct_count,
              'hp_percentage': hp_percentage,
              }
    
    
    # GET 요청 처리
    return render(request, 'multiple.html', context )



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
@csrf_exempt
def study_view(request):
    if request.method == 'GET':
        print("Rendering study.html")
        return render(request, 'study.html')
    print("Invalid request method")
    return JsonResponse({"error": "Invalid request method"}, status=400)


def summary_anime(request):
    return render(request, 'summary_anime.html')
