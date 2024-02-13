from django.urls import path
from .views import post_detail, post_list, post_create, post_like, comment_create

urlpatterns = [
    path('list', post_list),
    path('post', post_create),
    path('post/<str:post_id>', post_detail),
    path('post/<str:post_id>/like', post_like),
    path('post/<str:post_id>/comment', comment_create),
]
