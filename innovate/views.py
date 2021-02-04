from django.shortcuts import render, redirect

from .forms import CompetitorFormset, CompetitorForm, TeamForm
from .models import Competitor

# Create your views here.
def home(request):
    return render(request, 'innovate/index.html')

def signup(request):
    if request.method == 'POST':
        formset = CompetitorFormset(request.POST)
        team_form = TeamForm(request.POST, request.FILES)
        if formset.is_valid() and team_form.is_valid():
            team = team_form.save()
            is_leader = True
            for form in formset:
                name = form.cleaned_data.get('name')
                email = form.cleaned_data.get('email')
                if name and email:
                    m = Competitor(name=name, email=email, is_leader=is_leader, team=team)
                    m.save()
                    is_leader = False
            return redirect('landing')

    formset = CompetitorFormset()
    team_form = TeamForm()
    return render(request, 'innovate/signup.html', {'formset': formset, 'team_form': team_form})

def confirm(request):
    return render(request, 'innovate/confirm.html')