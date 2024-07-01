from django.shortcuts import render

# Create your views here.
def char_create(request):
    return render(request,'char_create.html')

def signup(request):
    return render(request,'signup.html')

def find_accound_pwd(request):
    return render(request,'find_accound_pwd.html')

def find_accound_id(request):
    return render(request,'find_accound_id.html')

def find_accound(request):
    return render(request,'find_accound.html')

def check_id(request):
    return render(request,'check_id.html')

def ranking(request):
    return render(request,'ranking.html')