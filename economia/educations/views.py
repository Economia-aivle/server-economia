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
import jwt
from django.contrib.sessions.models import Session


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
    
    characters = get_player(request, 'characters')
    
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

def success(request):
    return render(request, 'success.html')


def previous_quiz_answer(request, characters):
    response = requests.get(f'http://127.0.0.1:8000/educations/multipledatas/{characters}')
    data = response.json()
    return render(request, 'previous_quiz_answer.html', {'multiple': data})

# Create your views here.
def level_choice(request, characters, subjects_id, chapter):
    chapter = int(chapter)
    response = requests.get(f'http://127.0.0.1:8000/educations/getSubjectDatas/{subjects_id}/')
    data = response.json()
    
    # characters 정보 가져오기
    characters = get_player(request, 'characters')
    
    # subjects_id와 일치하는 chapter 찾기
    chapter_item = next((item for item in data if item['id'] == subjects_id), None)
    
    if chapter_item:
        chapter_content = chapter_item['chapters']
        chapter_list = chapter_content.split(', ')
        # chapter 값은 1-based index이므로 -1 해줌
        part = chapter_list[chapter - 1] if chapter - 1 < len(chapter_list) else None
    else:
        part = None
    try:
        stage_data = Stage.objects.get(characters_id=characters, subjects_id=subjects_id, chapter=chapter)
        chapter_sub = stage_data.chapter_sub
    except Stage.DoesNotExist:
        # Stage가 없을 경우 새로운 Stage 객체를 생성합니다.
        stage_data = Stage.objects.create(characters_id=characters, chapter=chapter, chapter_sub=1, subjects_id=subjects_id)
        chapter_sub = stage_data.chapter_sub
    
    context = {
        'characters': characters,
        'subjects_id': subjects_id,
        'chapter': chapter,
        'chapter_sub': chapter_sub,
        'part': part,
    }
    
    return render(request, 'level_choice.html', context)


@csrf_exempt
def tf_quiz_view(request):
    if request.method == 'GET':
        used_question_ids = request.GET.getlist('used_question_ids[]')
        chapter = request.GET.get('chapter')
        subjects_id = request.GET.get('subjects_id')  # 수정된 부분
        # characters = request.GET.get('characters')
        
        if not chapter or not subjects_id:
            return JsonResponse({"error": "Chapter and subjects are required."}, status=status.HTTP_400_BAD_REQUEST)

        questions = Tf.objects.filter(chapter=chapter, subjects_id=subjects_id).exclude(id__in=used_question_ids)
        if not questions:
            return JsonResponse({"error": "No questions available."}, status=status.HTTP_404_NOT_FOUND)
        question = random.choice(questions)

        context = {
            "question_id": question.id,
            "question_text": question.question_text,
            "correct_answer": question.correct_answer,
            "explanation": question.explanation,
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
        
        return JsonResponse(response_data, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def update_stage(request):
    if request.method == 'POST':
        characters = request.POST.get('characters')
        subjects_id = request.POST.get('subjects_id')
        chapter = request.POST.get('chapter')

        if not characters or not subjects_id or not chapter:
            return JsonResponse({"error": "Characters, subjects, and chapter are required."}, status=400)

        try:
            stage = Stage.objects.get(characters_id=characters, subjects_id=subjects_id, chapter=chapter)
            if stage.chapter_sub == 1:
                stage.chapter_sub = 2
                stage.save()
                return JsonResponse({'status': 'success', 'message': 'Stage updated successfully!'})
        except Stage.DoesNotExist:
            return JsonResponse({"error": "Stage not found."}, status=404)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

def tf_quiz_page(request, subjects_id, chapter):
    characters = get_player(request, 'characters')
    character = Characters.objects.get(id=characters)
    character_img = character.kind_url
    sounds = ['sounds/back_sound1.mp3', 'sounds/back_sound2.mp3', 'sounds/back_sound3.mp3']
    random_sound = random.choice(sounds)
    print(character_img)
    context = {
            'characters': characters,
              'subjects_id': subjects_id,
              'chapter': chapter,
              'character_img':character_img,
              'random_sound': random_sound,
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
    



def multiple(request, characters, subjects_id, chapter, num):
    # characters, subject, chapter에 해당하는 데이터를 필터링합니다.
    characters = get_player(request, 'characters')
    character = Characters.objects.get(id=characters)
    character_img = character.kind_url
    print(character_img)
    multiple_response = requests.get(f'http://127.0.0.1:8000/educations/multipledatas/{characters}')
    multiple_data = multiple_response.json()
    sounds = ['sounds/back_sound1.mp3', 'sounds/back_sound2.mp3', 'sounds/back_sound3.mp3']
    random_sound = random.choice(sounds)

    multiple_list = [item for item in multiple_data if item['characters'] == characters and item['subjects'] == subjects_id and item['chapter'] == chapter]

    questions = []
    max_num = min(5, len(multiple_list))
    for i in range(max_num):
        item = multiple_list[-(i + 1)]
        item['num'] = max_num - i
        questions.append(item)

    question = questions[num - 1] if num <= max_num else None
    if num == 6:
        return redirect('educations:level_choice', characters=characters, subjects_id=subjects_id, chapter=chapter)
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
                    stage_data = Stage.objects.get(characters_id=characters, subjects_id=subjects_id, chapter=chapter)
                    character_score = Characters.objects.get(characters_id=characters)
                    stage_data.chapter_sub = 3
                    character_score.score +=200
                    character_score.save()
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
        elif user_answer != correct_answer:
            wrong_count = request.session.get('wrong_count', 0) + 1
            request.session['wrong_count'] = wrong_count
            # 오답인 경우
            return JsonResponse({'status': 'wrong', 'message': '오답입니다.'})
    correct_count = request.session.get('correct_count', 0)
    wrong_count = request.session.get('wrong_count', 0)
    hp_percentage = max(0, 100 - (correct_count * 20))  # 체력 퍼센트 계산
    print(wrong_count)
    context ={'question': question,
              'num': num,
              'characters': characters,
              'subjects_id': subjects_id,
              'chapter': chapter,
              'correct_count': correct_count,
              'hp_percentage': hp_percentage,
              'wrong_count' : wrong_count,
              'character_img' : character_img,
              'random_sound' :random_sound,
              }
    
    
    # GET 요청 처리
    return render(request, 'multiple.html', context )



def blank(request, characters, subjects_id, chapter, num):
    blank_response = requests.get(f'http://127.0.0.1:8000/educations/blankdatas/{characters}')
    blank_data = blank_response.json()
    characters = get_player(request, 'characters')
    character = Characters.objects.get(id=characters)
    character_img = character.kind_url
    print(character_img)
    sounds = ['sounds/back_sound1.mp3', 'sounds/back_sound2.mp3', 'sounds/back_sound3.mp3']
    random_sound = random.choice(sounds)
    # characters, subject, chapter에 해당하는 데이터를 필터링합니다.
    blank_list = [item for item in blank_data if item['characters'] == characters and item['subjects'] == subjects_id and item['chapter'] == chapter]
    
    # 최대 5개의 질문을 가져옵니다.
    questions = []
    max_num = min(5, len(blank_list))
    for i in range(max_num):
        blank_list[i]['num'] = i + 1
        questions.append(blank_list[i])
    
    # 현재 num에 해당하는 질문을 가져옵니다.
    question = questions[num - 1] if num <= max_num else None
    if num == 6:
        return redirect('educations:level_choice', characters=characters, subjects_id=subjects_id, chapter=chapter)
    
    if request.method == 'POST':
        user_answer = request.POST.get('answer')
        correct_answer = question['correct_answer']
        if user_answer == correct_answer:
            # 정답인 경우
            blank_correct_count = request.session.get('blank_correct_count', 0) + 1
            request.session['blank_correct_count'] = blank_correct_count
            request.session.modified = True  # 세션 데이터가 변경되었음을 명시
            print(f"Correct count updated: {blank_correct_count}")
            if blank_correct_count == 5:
                # 모든 문제를 맞춘 경우 Stage 모델의 chapter_sub를 3으로 업데이트
                try:
                    stage_data = Stage.objects.get(characters_id=characters, subjects_id=subjects_id, chapter=chapter)
                    character_score = Characters.objects.get(characters_id=characters)
                    character_score.score +=300
                    stage_data.chapter_sub = 3
                    character_score.save()
                    stage_data.save()
                except Stage.DoesNotExist:
                    pass
                
                # 세션 초기화
                request.session['blank_correct_count'] = 0
                request.session.modified = True  # 세션 데이터가 변경되었음을 명시

                # JSON 응답 전송
                return JsonResponse({'status': 'complete', 'message': '모든 문제를 맞췄습니다!'})
            else:
                # 아직 모든 문제를 맞추지 않은 경우
                return JsonResponse({'status': 'correct', 'message': '정답입니다.'})
        elif user_answer != correct_answer:
            blank_wrong_count = request.session.get('blank_wrong_count', 0) + 1
            request.session['blank_wrong_count'] = blank_wrong_count
            request.session.modified = True  # 세션 데이터가 변경되었음을 명시
            print(f"Wrong count updated: {blank_wrong_count}")
            # 오답인 경우
            return JsonResponse({'status': 'wrong', 'message': '오답입니다.'})
    
    blank_correct_count = request.session.get('blank_correct_count', 0)
    blank_wrong_count = request.session.get('blank_wrong_count', 0)
    hp_percentage = max(0, 100 - (blank_correct_count * 20))  # 체력 퍼센트 계산
    context = {
        'question': question,
        'num': num,
        'characters': characters,
        'subjects_id': subjects_id,
        'chapter': chapter,
        'correct_count': blank_correct_count,
        'hp_percentage': hp_percentage,
        'wrong_count': blank_wrong_count,
        'character_img': character_img,
        'random_sound': random_sound,
    }

    return render(request, 'blank.html', context)

    
def study(request):
    return render(request,'study.html')

def summary_anime(request):
    return render(request,'summary_anime.html')

def wrong_explanation(request):
    return render(request,'wrong_explanation.html')

def chapter_summary(request):
    return render(request,'chapter_summary.html')

def chapter(request, subjects):
    response = requests.get(f'http://127.0.0.1:8000/educations/getSubjectDatas/{subjects}/')
    data = response.json()
    characters = get_player(request, 'characters')
    for chapter in data:
        chapter_content = chapter['chapters']
        chapter['chapters_list'] = chapter_content.split(', ')
    context = {
        'chapter': data,
        'characters':characters,
        
    }
    print(data)
    return render(request,'chapter.html', context)

@csrf_exempt
def study_view(request):
    if request.method == 'GET':
        print("Rendering study.html")
        return render(request, 'study.html')
    print("Invalid request method")
    return JsonResponse({"error": "Invalid request method"}, status=400)


def summary_anime(request):
    return render(request, 'summary_anime.html')

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
    