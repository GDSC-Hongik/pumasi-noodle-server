from django.contrib import admin
from django.urls import path, include
from .views import care_list, care_detail, my_care, update_status, request_care

urlpatterns = [
    path('', my_care),
    path('list', care_list),
    path('<str:pk>', care_detail),          # Firestore 문서의 ID로 이메일 이용
    path('<str:pk>/status', update_status), # Firestore 문서의 ID로 이메일 이용
    path('<str:pk>/request', request_care), # Firestore 문서의 ID로 이메일 이용
]
