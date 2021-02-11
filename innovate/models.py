from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Team(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=20, null=True, blank=True)
    reciept = models.FileField(upload_to='reciepts/', null=True, blank=True)
    
    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return self.name
    
    def clean(self):
        # Don't allow teams to have the same name.
        if Team.objects.filter(name=self.name).count() > 0:
            raise ValidationError({'name': 'That name is already taken! Sorry.'})

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

    def clean(self):
        # Don't allow teams to have the same name.
        if Competitor.objects.filter(name=self.name).count() > 0:
            raise ValidationError({'name': 'Somebody with that name is already registered!'})

        if Competitor.objects.filter(email=self.email).count() > 0:
            raise ValidationError({'email': 'Somebody with that email is already registered!'})
