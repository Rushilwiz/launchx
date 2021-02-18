from django.shortcuts import render, redirect

from .forms import CompetitorFormset, CompetitorForm, TeamForm
from .models import Competitor

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from config.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives, send_mail

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
