from django.shortcuts import render

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from django.contrib.auth.decorators import login_required

# Create your views here.
def login(request):
    return render(request, 'users/login.html')

@login_required
def logout(request):
    auth_logout(request)
    return render(request, 'users/logout.html')