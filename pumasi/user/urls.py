from django.contrib import admin
from django.urls import path
from .views import UserList, UserDetail, ChildList, ChildDetail, AddUserData, AddChildData

urlpatterns = [
    path("", UserList),
    path("<str:pk>", UserDetail),
    path("<str:pk>/child", ChildList),
    path("<str:pk>/child/<int:child_pk>", ChildDetail),
    path("addUserData", AddUserData),
    path("addChildData", AddChildData),
]