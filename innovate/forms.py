from django import forms
from django.forms import modelformset_factory

from .models import Competitor, Team, Score

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
    name = forms.CharField(required=True, label="Team Name",  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'BusinessX'}))
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

class ScoreForm(forms.ModelForm):
    innovation = forms.IntegerField(min_value=0, max_value=30, widget=forms.NumberInput(attrs={'placeholder': '30'}))
    need = forms.IntegerField(min_value=0, max_value=35, widget=forms.NumberInput(attrs={'placeholder': '35'}))
    finances = forms.IntegerField(min_value=0, max_value=25, widget=forms.NumberInput(attrs={'placeholder': '25'}))
    creativity = forms.IntegerField(min_value=0, max_value=10, widget=forms.NumberInput(attrs={'placeholder': '10'}))

    qna = forms.IntegerField(min_value=0, max_value=25, widget=forms.NumberInput(attrs={'placeholder': '25'}))
    speaking = forms.IntegerField(min_value=0, max_value=10, widget=forms.NumberInput(attrs={'placeholder': '10'}))
    persuasiveness = forms.IntegerField(min_value=0, max_value=10, widget=forms.NumberInput(attrs={'placeholder': '10'}))
    professionalism = forms.IntegerField(min_value=0, max_value=5, widget=forms.NumberInput(attrs={'placeholder': '5'}))

    feedback = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': 'Enter feedback here (optional)', 'class': 'form-control'}))

    class Meta:
        model = Score
        fields = ['innovation', 'need', 'finances', 'creativity', 'qna', 'speaking', 'persuasiveness', 'professionalism']