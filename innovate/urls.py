from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='innovate-home'),
    path('signup/', views.signup, name='competitor-signup'),
    path('signup/confirm/', views.confirm, name='competitor-signup-confirm'),
    path('judges/', views.portal, name='judges-portal'),
    path('judges/feedback/', views.feedback, name='judges-feedback')
]