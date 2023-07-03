from django import template
from django.db.models import *
from food.models import Post, CommentUnderPost
register = template.Library()


@register.inclusion_tag("inc/recent_posts_home_top.html")
def get_posts_home_top(cnt=4):
    posts = Post.objects.order_by("-created_at")[:4]
    return {"posts": posts, "cnt": cnt}


@register.inclusion_tag("inc/most_viewed_posts_home.html")
def get_most_viewed_posts_home(cnt=4):
    posts = Post.objects.order_by("-views")[:4]
    return {"posts": posts, "cnt": cnt}


@register.inclusion_tag("inc/most_popular_posts_sidebar.html")
def get_most_popular_posts_sidebar(cnt=5):
    posts = list(sorted(Post.objects.order_by("-created_at"), key=lambda x: x.views * 2 + x.likes.count() * 10))[-cnt:][::-1]
    return {"posts": posts, "cnt": cnt}


@register.inclusion_tag("inc/most_popular_post_home.html")
def get_most_popular_post_home(cnt=1):
    post = list(sorted(Post.objects.order_by("-created_at"), key=lambda x: x.views * 2 + x.likes.count() * 10))[-cnt:][::-1]
    return {"post": post, "cnt": cnt}


@register.inclusion_tag("inc/get_related_posts_single.html")
def get_related_posts_single(cnt=4):
    posts = Post.objects.order_by("-created_at")[:4]
    return {"posts": posts, "cnt": cnt}


@register.inclusion_tag("inc/post_comments_cnt.html")
def get_count_of_comments(slug):
    cnt = CommentUnderPost.objects.filter(post__slug=slug).count()
    return {"cnt": cnt}


