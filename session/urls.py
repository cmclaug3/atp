from django.contrib import admin
from django.urls import path, include

from .views import ServeSessionView, BurnSessionView



urlpatterns = [
    path('serve_session/<int:client_id>', ServeSessionView.as_view(), name='serve_session'),
    path('burn_session/<int:client_id>', BurnSessionView.as_view(), name='burn_session'),


    ]