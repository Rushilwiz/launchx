from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

class Team(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=20, null=True, blank=True)
    reciept = models.FileField(upload_to='reciepts/', null=True, blank=True)
    
    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return f'Team {self.number}: {self.name}'
    
    @property
    def feedback_recieved(self):
        return Score.objects.filter(team=self).count()

    @property
    def score_average(self):
        scores = Score.objects.filter(team=self)
        if scores.count() == 0:
            return 0
        average = 0
        for score in scores:
            average += score.get_total_score
        return round(average / scores.count(), 2)

    # def clean(self):
    #     # Don't allow teams to have the same name.
    #     if Team.objects.filter(name=self.name).count() > 0:
    #         raise ValidationError({'name': 'That name is already taken! Sorry.'})

class Competitor(models.Model):
    name = models.CharField(max_length=20, blank=True, default='')
    email = models.EmailField(max_length=254)
    school = models.CharField(max_length=20, blank=True, default='')
    county = models.CharField(max_length=20, blank=True, default='')
    is_leader = models.BooleanField(default=False)
    
    team = models.ForeignKey(Team, related_name="competitors", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Competitor"
        verbose_name_plural = "Competitors"
    
    def __str__(self):
        return self.name

    # def clean(self):
    #         # Don't allow teams to have the same name.
    #         if Competitor.objects.filter(name=self.name).count() > 0:
    #             raise ValidationError({'name': 'Somebody with that name is already registered!'})

    #         if Competitor.objects.filter(email=self.email).count() > 0:
    #             raise ValidationError({'email': 'Somebody with that email is already registered!'})

class Judge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isEven = models.BooleanField()

    class Meta:
        verbose_name = "Judge"
        verbose_name_plural = "Judges"

    def __str__(self):
        return f'Judge {self.user.last_name}'
    
    @property
    def name(self):
        return self.user.get_full_name()

    @property
    def scores_left(self):
        all_teams = len([team.number for team in Team.objects.all() if ((team.number % 2 == 0 and self.isEven) or (team.number % 2 != 0 and not self.isEven))])
        completed_teams = Score.objects.filter(judge=self).count()
        return f'{completed_teams}/{all_teams}'
    
    @property
    def color(self):
        return 'Blue' if self.isEven else 'Red'

class Score(models.Model):
    judge = models.ForeignKey(Judge, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    # product scores
    innovation = IntegerRangeField(min_value=0, max_value=30)
    need = IntegerRangeField(min_value=0, max_value=35)
    finances = IntegerRangeField(min_value=0, max_value=25)
    creativity = IntegerRangeField(min_value=0, max_value=10)

    # delivery scores
    qna = IntegerRangeField(min_value=0, max_value=25)
    speaking = IntegerRangeField(min_value=0, max_value=10)
    persuasiveness = IntegerRangeField(min_value=0, max_value=10)
    professionalism = IntegerRangeField(min_value=0, max_value=5)
    fields = [innovation, need, finances, creativity, qna, speaking, persuasiveness, professionalism]

    feedback = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback"
    
    def __str__(self):
        return f'Team {self.team.number}\'s Feedback from {self.judge.user.get_full_name()}'
    
    @property
    def get_total_score(self):
        fields = [self.innovation, self.need, self.finances, self.creativity, self.qna, self.speaking, self.persuasiveness, self.professionalism]
        return sum(fields)