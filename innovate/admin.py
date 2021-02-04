from django.contrib import admin

from .models import Team, Competitor
from django.contrib.auth.models import User, Group

# Register your models here.
class LaunchXAdminSite(admin.AdminSite):
    site_header = "LaunchX Admin"
    site_title = "LaunchX Admin Portal"
    index_title = "Welcome to LaunchX Admin Page"

admin_site = LaunchXAdminSite(name='launchx-admin')

admin_site.register(User)
admin_site.register(Group)

admin_site.register(Competitor)
admin_site.register(Team)