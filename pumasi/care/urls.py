from django.contrib import admin
from django.urls import path, include
from .views import care_list, care_detail, my_care

urlpatterns = [
    path('', my_care),
    path('list', care_list),
    path('<str:pk>', care_detail), # Firestore 문서의 ID를 자동 생성 문자열을 이용함.
]
