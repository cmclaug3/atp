"""atp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from accounts.views import (RegisterAuthorizedUserView, SetNewUserPasswordView, home, CreateClientView,\
    SingleClientView, SetPinView, SetClientPinView, ClientView, TrainerView, SingleTrainerView, AllWeeksView, SingleWeekView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('session/', include('session.urls')),
    path('', home, name='home'),
    path('register_user', RegisterAuthorizedUserView.as_view(), name='register_user'),
    path('set_new_user_password/<int:new_user_id>', SetNewUserPasswordView.as_view(), name='set_new_user_password'),
    path('set_pin', SetPinView.as_view(), name='set_pin'),
    path('set_client_pin/<int:client_id>', SetClientPinView.as_view(), name='set_client_pin'),
    path('create_client', CreateClientView.as_view(), name='create_client'),
    path('clients', ClientView.as_view(), name='clients'),
    path('single_client/<int:client_id>', SingleClientView.as_view(), name='single_client'),
    path('trainers', TrainerView.as_view(), name='trainers'),
    path('single_trainer/<int:trainer_id>', SingleTrainerView.as_view(), name='single_trainer'),
    path('all_weeks', AllWeeksView.as_view(), name='all_weeks'),
    path('single_week/<int:week_num>', SingleWeekView.as_view(), name='single_week'),
]

