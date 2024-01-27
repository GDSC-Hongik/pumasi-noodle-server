from django.contrib import admin
from django.urls import path
from .views import UserPageView, ChildList, ChildDetail

urlpatterns = [
    path("<str:pk>", UserPageView),
    path("<str:pk>/child", ChildList),
    path("<str:pk>/child/<int:child_pk>", ChildDetail),
]