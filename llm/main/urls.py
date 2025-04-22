from django.contrib import admin
from django.urls import path, include
from .views import chat_view, calculator_view, redirect_to_main, chat_api

urlpatterns = [
    path('', redirect_to_main),
    path('main', chat_view),
    path('calculator', calculator_view),
    path('chat/', chat_api, name='chat_api'),
]
