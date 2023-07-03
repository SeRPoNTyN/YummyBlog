from django.urls import path
from .views import *


urlpatterns = [
    path("archive/categories/<str:slug>", PostsByCategory.as_view(), name="category"),
    path("post/<str:slug>", GetPost.as_view(), name="single"),
    path("post-like/<str:slug>", like_or_dislike, name="post_like"),
    path("comment-like/<int:pk>", like_comment, name="comment_like"),
    path("comment-dislike/<int:pk>", dislike_comment, name="comment_dislike"),
    path("view/<str:slug>", views_category, name="views_category"),
    path("archive/categories/", GetCategories.as_view(), name="choice_category"),
    path("archive/", Archive.as_view(), name="archive"),
    path("add-comment/<str:slug>", add_comment, name="add_comment"),
    path("", Home.as_view(), name="home"),
]
