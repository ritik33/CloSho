from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('update-profile/', views.updateProfile, name='update-profile'),
    path('update-password/', views.updatePassword, name='update-password'),
]
