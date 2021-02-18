from django import forms
from django.forms import modelformset_factory

from .models import Competitor, Team

class CompetitorForm(forms.ModelForm):
    name = forms.CharField(label='Full Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John Doe'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@email.com'}))
    school = forms.CharField(label='School', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'TJHSST'}))
    county = forms.CharField(label='County', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fairfax'}))
    
    class Meta:
        model = Competitor
        fields = ['name', 'email', 'school', 'county']

    def __init__(self, *args, **kwargs):
        super(CompetitorForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''


CompetitorFormset = modelformset_factory(
    Competitor,
    form=CompetitorForm,
    min_num=2, max_num=4)

class TeamForm(forms.ModelForm):
    name = forms.CharField(required=False, label="Team Name",  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'BusinessX'}))
    reciept = forms.FileField(required=False)

    class Meta:
        model = Team
        fields = ['name', 'reciept']

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''

    def save(self, commit=True):
        m = super(TeamForm, self).save(commit=False)
        m.number = Team.objects.all().count() + 1
        if commit:
            m.save()
        return m