from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from economia.models import *
from .serializers import *

# Create your views here.
def char_create(request):
    return render(request,'char_create.html')

def char_delete(request):
    return render(request,'char_delete.html')

def signup(request):
    return render(request,'signup.html')

def find_account_pwd(request):
    return render(request,'find_account_pwd.html')

def find_account_id(request):
    return render(request,'find_account_id.html')

def find_account(request):
    return render(request,'find_account.html')

def check_id(request):
    return render(request,'check_id.html')

@api_view(['GET'])
def getSubjectsDatas(request):
    datas = Subjects.objects.all()
    serializer = SubjectsSerializer(datas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSubjectsScoreDatas(request, subject_id):
    scores = SubjectsScore.objects.filter(subjects_id=subject_id).order_by('-score')
    if not scores.exists():
        return Response({"error": "No data found for the given subject_id"}, status=404)

    serializer = SubjectsScoreSerializer(scores, many=True)
    

    ranked_scores = []
    current_rank = 1
    current_score = None

    for i, score in enumerate(serializer.data):
        if current_score != score['score']:
            current_rank = i + 1
            current_score = score['score']
        ranked_scores.append({
            'rank': current_rank,
            'nickname': score['characters']['player']['nickname'],
            'school': score['characters']['player']['school'],
            'score': score['score']
        })

    return Response(ranked_scores)

def ranking(request):
    subjects = Subjects.objects.all()
    first_subject_id = subjects[0].id if subjects else None

    if first_subject_id:
        scores_response = getSubjectsScoreDatas(request, first_subject_id)
        ranked_scores = scores_response.data
    else:
        ranked_scores = []

    return render(request, 'ranking.html', {'subjects': subjects, 'ranked_scores': ranked_scores})