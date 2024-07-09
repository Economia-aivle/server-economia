from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from economia.models import *
import random

# Create your views here.
def level_choice(request):
    return render(request, 'level_choice.html')

@csrf_exempt
def tf_quiz_view(request, question_id=None):
    if request.method == 'GET':
        if question_id:
            try:
                question = Tf.objects.get(id=question_id)
            except Tf.DoesNotExist:
                return JsonResponse({"error": "Question not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            questions = list(Tf.objects.all())
            if not questions:
                return JsonResponse({"error": "No questions available."}, status=status.HTTP_404_NOT_FOUND)
            question = random.choice(questions)

        return JsonResponse({
            "question_id": question.id,
            "question_text": question.question_text,
            "correct_answer": question.correct_answer,
            "explanation": question.explanation
        })

    elif request.method == 'POST':
        question_id = request.POST.get('question_id')
        submitted_answer = request.POST.get('submitted_answer')

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

def tf_quiz_page(request):
    return render(request, 'tfquiz.html')
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


def blank(request):
    return render(request, 'blank.html')


def multiple(request):
    return render(request, 'multiple.html')


def previous_quiz_answer(request):
    return render(request, 'previous_quiz_answer.html')


def previous_quiz(request):
    return render(request, 'previous_quiz.html')


@csrf_exempt
def study_view(request):
    if request.method == 'GET':
        print("Rendering study.html")
        return render(request, 'study.html')
    print("Invalid request method")
    return JsonResponse({"error": "Invalid request method"}, status=400)


def summary_anime(request):
    return render(request, 'summary_anime.html')