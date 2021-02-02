from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('calendar/', views.calendar, name='calendar'),
    path('officers/', views.officers, name='officers')
]