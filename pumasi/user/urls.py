from django.contrib import admin
from django.urls import path
from .views import UserList, UserDetail, ChildList, ChildDetail, AddUserData, AddChildData, AddUserDataPost

urlpatterns = [
    path("", UserList), # 전체 유저 리스트
    path("addUserData", AddUserData), # 유저 테스트 데이터 생성(하드코딩)
    path("addUserData/<str:pk>", AddUserDataPost), # 유저 테스트 데이터 생성(POST 요청) -> 실제 사용하는 기능은 아니고 개발 편의를 위해 유저 테스트 데이터 생성할 수 있도록 한 기능임
    path("addChildData", AddChildData), # 아이 테스트 데이터 생성(하드코딩)
    path("<str:pk>", UserDetail),
    path("<str:pk>/child", ChildList),
    path("<str:pk>/child/<int:child_pk>", ChildDetail),
    # path("<str:pk>/care", UserCareList) <- 개발중
    # path("<str:pk>/care/detail", ) <- 개발중
]