from django.urls import path
from .views import post_detail, post_list, post_create

urlpatterns = [
    path('list', post_list),
    path('post', post_create),
    path('post/<str:post_id>', post_detail),
]
