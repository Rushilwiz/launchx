from django.contrib import admin

from .models import Team, Competitor, Judge, Score
from django.contrib.auth.models import User, Group

# Register your models here.
class LaunchXAdminSite(admin.AdminSite):
    site_header = "LaunchX Admin"
    site_title = "LaunchX Admin Portal"
    index_title = "Welcome to LaunchX Admin Page"

admin_site = LaunchXAdminSite(name='launchx-admin')

admin_site.register(User)
admin_site.register(Group)

class JudgeAdmin(admin.ModelAdmin):
    list_display = ("name", "scores_left", "color")

admin_site.register(Judge, JudgeAdmin)

class ScoreAdmin(admin.ModelAdmin):
    list_display = ("__str__", "get_total_score")
admin_site.register(Score, ScoreAdmin)

class CompetitorAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'team')

admin_site.register(Competitor, CompetitorAdmin)

class CompetitorInline(admin.TabularInline):
    model = Competitor
    

class TeamAdmin(admin.ModelAdmin):
    inlines = [
        CompetitorInline,
    ]

    list_display = ('number', 'name', 'feedback_recieved', 'score_average')
    ordering = ('number',)

admin_site.register(Team, TeamAdmin)