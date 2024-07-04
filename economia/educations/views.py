from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from economia.models import *
from .serializers import TFQuizSerializer

# Create your views here.
def level_choice(request):
    return render(request,'level_choice.html')

# OX 퀴즈
class TFQuizAPIView(generics.GenericAPIView):
    serializer_class = TFQuizSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question_id = serializer.validated_data['question_id']
        submitted_answer = serializer.validated_data['submitted_answer']

        try:
            question = Tf.objects.get(id=question_id)
        except Tf.DoesNotExist:
            return Response({"error": "Question does not exist"}, status=status.HTTP_404_NOT_FOUND)

        correct_answer = question.correct_answer

        if submitted_answer.upper() == correct_answer:  # 대소문자 구분 없이 체크
            is_correct = True
        else:
            is_correct = False

        # 결과를 반환
        return Response({
            "question_id": question_id,
            "submitted_answer": submitted_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "explanation": question.explanation if not is_correct else None
        })


class ChooseTFChapterView(APIView):
    def post(self, request, *args, **kwargs):
        chapter = request.data.get('chapter')
        if not chapter:
            return Response({"error": "Chapter number is required."}, status=status.HTTP_400_BAD_REQUEST)

        questions = Tf.objects.filter(chapter=chapter)[:5]  # 챕터별 문제 5개 가져오기

        if not questions:
            return Response({"error": "No questions found for the selected chapter."}, status=status.HTTP_404_NOT_FOUND)

        question_data = [{
            "id": question.id,
            "question_text": question.question_text,
            "correct_answer": question.correct_answer,
            "explanation": question.explanation
        } for question in questions]

        return Response({"questions": question_data}, status=status.HTTP_200_OK)


class TFQuizView(APIView):
    def post(self, request, *args, **kwargs):
        question_id = request.data.get('question_id')
        submitted_answer = request.data.get('submitted_answer')

        try:
            question = Tf.objects.get(id=question_id)
        except Tf.DoesNotExist:
            return Response({"error": "Question not found."}, status=status.HTTP_404_NOT_FOUND)

        correct_answer = question.correct_answer
        is_correct = submitted_answer == correct_answer

        response_data = {
            "question_id": question.id,
            "submitted_answer": submitted_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "explanation": question.explanation if not is_correct else None
        }

        return Response(response_data, status=status.HTTP_200_OK)


def blank(request):
    return render(request,'blank.html')

def multiple(request):
    return render(request,'multiple.html')

def previous_quiz_answer(request):
    return render(request,'previous_quiz_answer.html')

def previous_quiz(request):
    return render(request,'previous_quiz.html')

# 학습하기
@csrf_exempt
def study_view(request):
    if request.method == 'GET' and 'video' in request.GET:
        video_url = "https://music.youtube.com/watch?v=od5qQ84pKIo&list=RDAMVM-vN8G8Vpy6M"
        print("Returning video URL:", video_url)
        return JsonResponse({"video_url": video_url})
    elif request.method == 'GET':
        print("Rendering study.html")
        return render(request, 'study.html')
    print("Invalid request method")
    return JsonResponse({"error": "Invalid request method"}, status=400)

def summary_anime(request):
    return render(request,'summary_anime.html')
