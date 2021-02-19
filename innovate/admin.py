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

admin_site.register(Judge)
admin_site.register(Score)

admin_site.register(Competitor)

class CompetitorInline(admin.TabularInline):
    model = Competitor

class TeamAdmin(admin.ModelAdmin):
    inlines = [
        CompetitorInline,
    ]
    

admin_site.register(Team, TeamAdmin)