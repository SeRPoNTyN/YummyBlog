from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.


class Tags(models.Model):
    title = models.CharField(max_length=50, verbose_name="Имя")
    description = models.TextField(max_length=200, verbose_name="Описание")
    slug = models.CharField(max_length=100, verbose_name="Ссылка", unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["title"]

    def get_absolute_url(self):
        return reverse("posts_by_tags", kwargs={"slug": self.slug})


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="Имя категории")
    description = models.TextField(max_length=200, verbose_name="Описание")
    image = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, verbose_name="Фото")
    slug = models.CharField(max_length=100, verbose_name="Ссылка", unique=True)
    views = models.IntegerField(default=0, verbose_name="Кол-во просмотров")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["title"]

    def get_absolute_url(self):
        return reverse("category", kwargs={"slug": self.slug})

    def get_absolute_url_views(self):
        return reverse("views_category", kwargs={"slug": self.slug})


class Post(models.Model):
    title = models.CharField(max_length=50, verbose_name="Имя поста")
    content = models.TextField(verbose_name="Содержание")
    image = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, verbose_name="Фото")
    slug = models.CharField(max_length=100, verbose_name="Ссылка", unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категории", null=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Автор", null=True, related_name="Автор")
    likes = models.ManyToManyField(User, verbose_name="Лайки", related_name="Лайки")
    created_at = models.DateField(auto_now_add=True, verbose_name="Время создания")
    views = models.IntegerField(default=0, verbose_name="Кол-во просмотров")
    tags = models.ManyToManyField(Tags, verbose_name="Теги")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["title"]

    def get_absolute_url(self):
        return reverse("single", kwargs={"slug": self.slug})

    def get_likes_count(self):
        return self.likes.count()


class CommentUnderPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Автор комментария")
    content = models.TextField(verbose_name="Содержимое комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания комментария")
    post = models.ForeignKey(Post, on_delete=models.PROTECT, verbose_name="Пост", null=True)
    likes = models.ManyToManyField(User, verbose_name="Лайки", related_name="Лайки комментария+")
    dislikes = models.ManyToManyField(User, verbose_name="Дизлайки", related_name="Дизлайки комментария+")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def add_comment(self):
        return reverse("add_comment", kwargs={"slug": self.slug})

    def get_likes_count(self):
        return self.likes.count() - self.dislikes.count()

