from django.shortcuts import render

# Create your views here.
def level_choice(request):
    return render(request,'level_choice.html')

def tfquiz(request):
    return render(request,'tfquiz.html')

def blank(request):
    return render(request,'blank.html')

def multiple(request):
    return render(request,'multiple.html')

def previous_quiz_answer(request):
    return render(request,'previous_quiz_answer.html')

def previous_quiz(request):
    return render(request,'previous_quiz.html')

def study(request):
    return render(request,'study.html')

def summary_anime(request):
    return render(request,'summary_anime.html')
