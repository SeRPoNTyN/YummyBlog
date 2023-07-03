from django import template
from django.db.models import *
from food.models import Category

register = template.Library()


@register.inclusion_tag("inc/categories_home.html")
def get_categories_home():
    categories = Category.objects.order_by("-views")[:3]
    return {"categories": categories}


@register.inclusion_tag("inc/categories_header.html")
def get_categories_header():
    categories = Category.objects.order_by("-views")
    return {"categories": categories}

