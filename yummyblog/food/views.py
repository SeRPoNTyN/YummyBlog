from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404
from .forms import *
# Create your views here.


class Home(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.order_by("-created_at")[4:]


class Archive(ListView):
    paginate_by = 1
    model = Post
    template_name = "blog/archive.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.order_by("-created_at")


class GetCategories(ListView):
    paginate_by = 1
    model = Category
    template_name = "blog/choice_category.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.order_by("title")


class PostsByCategory(ListView):
    paginate_by = 1
    model = Post
    template_name = "blog/categories.html"
    context_object_name = "posts"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = str(Category.objects.get(slug=self.kwargs["slug"]))
        return context

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs["slug"]).order_by("-created_at")


def views_category(request, slug):
    category = Category.objects.get(slug=slug)
    category.views = F("views") + 1
    category.save()
    category.refresh_from_db()
    return redirect(category.get_absolute_url())


class GetPost(DetailView):
    model = Post

    template_name = "blog/single.html"
    context_object_name = "post"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F("views") + 1
        self.object.save()
        self.object.refresh_from_db()

        form = CommentForm()

        likes_connected = get_object_or_404(Post, slug=self.kwargs['slug'])
        liked = False

        comments = sorted(CommentUnderPost.objects.filter(post__slug=self.kwargs["slug"]), key=lambda x: x.get_likes_count())[::-1]
        comments_count = len(comments)

        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['number_of_likes'] = likes_connected.get_likes_count()
        context['post_is_liked'] = liked
        context['form'] = form
        context['comments'] = comments
        context['comments_count'] = comments_count

        return context

    def get_queryset(self):
        return Post.objects.filter(slug=self.kwargs["slug"])


def like_or_dislike(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('single', args=[str(slug)]))


def add_comment(request, slug):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = Post.objects.get(slug=slug)
            form.save()
            return redirect(Post.objects.get(slug=slug).get_absolute_url())
    else:
        form = CommentForm()
    return render(request, 'blog/single.html', {'form': form})


def like_comment(request, pk):
    comment = get_object_or_404(CommentUnderPost, pk=pk)
    post = Post.objects.get(pk=comment.post.pk)

    if comment.dislikes.filter(id=request.user.id).exists():
        comment.dislikes.remove(request.user)
        comment.likes.add(request.user)
    elif comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return redirect(post.get_absolute_url())


def dislike_comment(request, pk):
    comment = get_object_or_404(CommentUnderPost, pk=pk)
    post = Post.objects.get(pk=comment.post.pk)
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
        comment.dislikes.add(request.user)
    elif comment.dislikes.filter(id=request.user.id).exists():
        comment.dislikes.remove(request.user)
    else:
        comment.dislikes.add(request.user)
    return redirect(post.get_absolute_url())
