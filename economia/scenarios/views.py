from django.shortcuts import render

# Create your views here.
def previous_scenario(request):
    return render(request,'previous_scenario.html')

def scenario_list(request):
    return render(request,'scenario_list.html')

def scenario(request):
    return render(request,'scenario.html')

