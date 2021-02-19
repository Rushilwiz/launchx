from django.shortcuts import render, redirect

from .forms import CompetitorFormset, CompetitorForm, TeamForm, ScoreForm
from .models import Competitor, Team, Judge, Score

from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives, send_mail

from config.settings import EMAIL_HOST_USER

# Create your views here.
def home(request):
    return render(request, 'innovate/index.html')

def signup(request):
    formset = CompetitorFormset(queryset=Competitor.objects.none())
    team_form = TeamForm()
    
    if request.method == 'POST':
        formset = CompetitorFormset(request.POST)
        team_form = TeamForm(request.POST, request.FILES)
        if formset.is_valid() and team_form.is_valid():
            team = team_form.save()
            is_leader = True
            members = []
            for form in formset:
                name = form.cleaned_data.get('name')
                email = form.cleaned_data.get('email')
                school = form.cleaned_data.get('school')
                county = form.cleaned_data.get('school')
                if name and email and school and county:
                    m = Competitor(name=name, email=email, school=school, county=county, is_leader=is_leader, team=team)
                    is_leader = False
                    members.append(m)
            send_confirmation(request, team, members)
            for m in members:
                m.save()
            return redirect('landing')

    return render(request, 'innovate/signup.html', {'formset': formset, 'team_form': team_form})


def send_confirmation(request, team, members):
    subject = "🥳 InnovateTJ Signup Confirmation"
    recepients = []
    for member in members:
        recepients.append(member.email)

    context = {
        'team': team,
        'members': members
    }

    html_message = render_to_string('innovate/email_template.html', context=context)
    plain_message = strip_tags(html_message)
    sender = [EMAIL_HOST_USER] 
    email = EmailMultiAlternatives(
        subject, 
        plain_message, 
        EMAIL_HOST_USER, 
        recepients,
        reply_to=sender
    )
    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)

def confirm(request):
    return render(request, 'innovate/confirm.html')

@login_required
def portal(request):
    judge = Judge.objects.get(user=request.user)
    team_numbers = [team.number for team in Team.objects.all() if ((team.number % 2 == 0 and judge.isEven) or (team.number % 2 != 0 and not judge.isEven))]
    teams, completed_teams = [], []
    for number in team_numbers:
        if Score.objects.filter(team=Team.objects.get(number=number), judge=judge).count() == 0:
            teams.append(Team.objects.get(number=number))
        else:
            completed_teams.append((Team.objects.get(number=number), Score.objects.get(team=Team.objects.get(number=number), judge=judge)))
    
    context = {
        'teams': teams,
        'completed_teams': completed_teams,
        'completed_teams_count': len(completed_teams),
        'teams_count': len(team_numbers)
    }

    return render(request, 'innovate/portal.html', context=context)

@login_required
def feedback(request):
    form = ScoreForm()
    judge = Judge.objects.get(user=request.user)
    if type(judge) != Judge:
        print('no team or judge')
        return redirect('judges-portal')
    
    if request.method == 'POST':
        form = ScoreForm(request.POST)
        if form.is_valid():
            team = Team.objects.get(number=request.POST['team_number'])
            if ((team.number % 2 != 0 and judge.isEven) or (team.number % 2 == 0 and not judge.isEven)):
                print('judge not approved')
                return redirect('judges-portal')
            score = form.save(commit=False)
            score.judge = judge
            score.team = team
            score.feedback = form.cleaned_data['feedback']
            score.save()
            return redirect('judges-portal')
    elif request.GET.get('team'):
        team = Team.objects.get(number=request.GET['team'])
        if team == None:
            print('no team or judge')
        elif ((team.number % 2 != 0 and judge.isEven) or (team.number % 2 == 0 and not judge.isEven)):
            print('judge not approved')
        elif Score.objects.filter(team=team, judge=judge).count() != 0:
            print('feedback already exists')
        else:
            context = {
                'team': team,
                'judge': judge,
                'form': form,
            }
            return render(request, 'innovate/feedback.html', context=context)
    return redirect('judges-portal')

