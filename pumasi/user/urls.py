from django.contrib import admin
from django.urls import path
from .views import UserList, UserDetail, ChildList, ChildDetail, ChildDelete, AddUserData, AddChildData

urlpatterns = [
    path("", UserList),
    path("<str:pk>", UserDetail),
    path("<str:pk>/child", ChildList),
    path("<str:pk>/child/<int:child_pk>", ChildDetail),
    path("<str:pk>/child/<int:child_pk>/delete", ChildDelete),
    path("addUserData", AddUserData),
    path("addChildData", AddChildData),
]