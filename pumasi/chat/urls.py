from django.contrib import admin
from django.urls import path, include
from .views import chat_list, chat_detail, chat_settings, chat_message, create_chat_room

urlpatterns = [
    path('', create_chat_room),
    path('list', chat_list),
    path('<str:room_id>', chat_detail),
    path('<str:room_id>/settings', chat_settings),
    path('<str:room_id>/message', chat_message),
]
