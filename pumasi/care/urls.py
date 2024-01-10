from django.contrib import admin
from django.urls import path, include
from .views import care_list, care_detail, my_care

urlpatterns = [
    path('', my_care),
    path('list', care_list),
    path('<int:pk>', care_detail),
]
