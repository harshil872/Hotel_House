from django.shortcuts import render
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index.html'),
    path('contact/',views.contact, name="contact"),
]