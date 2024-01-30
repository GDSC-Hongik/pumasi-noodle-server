from django.contrib import admin
from django.urls import path
from .views import UserPageView, ChildList, ChildDetail, AddData

urlpatterns = [
    path("addData", AddData),
    path("<str:pk>", UserPageView),
    path("<str:pk>/child", ChildList),
    path("<str:pk>/child/<int:child_pk>", ChildDetail),
]