from django.contrib import admin
from django.urls import path
from .views import UserPageView, ChildList, ChildDetail, AddData, user_list

urlpatterns = [
    path("addData", AddData),
    path("", user_list),
    path("<str:pk>", UserPageView),
    path("<str:pk>/child", ChildList),
    path("<str:pk>/child/<int:child_pk>", ChildDetail),
]