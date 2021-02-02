from django.shortcuts import render

# Create your views here.
def landing(request):
    return render(request, 'launchx/landing.html')

def calendar(request):
    return render(request, 'launchx/calendar.html')

def officers(request):
    return render(request, 'launchx/officers.html')