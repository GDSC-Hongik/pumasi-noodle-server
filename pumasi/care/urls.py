from django.contrib import admin
from django.urls import path, include
from .views import care_list, care_detail

urlpatterns = [
    path('', care_detail),
    path('list', care_list),
]
