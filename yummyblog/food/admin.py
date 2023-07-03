from django.utils.safestring import mark_safe
from .models import *
from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
# Register your models here.


class CategoryAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Category
        fields = '__all__'


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class TagsAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Tags
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    form = PostAdminForm
    save_as = True
    save_on_top = True
    list_display = ["id", "title", "slug", "get_image", "created_at", "views"]
    list_display_links = ["id", "title"]
    list_filter = ["category", "tags"]
    search_fields = ["title", "content", "tags", "category"]
    readonly_fields = ["views", "author", "created_at", "get_image"]
    fields = ["title", "slug", "content", "author", "category", "tags", "image", "get_image", "views", "created_at"]

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width ='50'>")
        return "-"

    get_image.short_description = "Image"


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    form = CategoryAdminForm
    save_as = True
    save_on_top = True
    list_display = ["id", "title", "slug", "get_image", "views"]
    list_display_links = ["id", "title"]
    search_fields = ["title", "description"]
    readonly_fields = ["get_image", "views"]
    fields = ["title", "slug", "views", "description", "image", "get_image"]

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width ='50'>")
        return "-"

    get_image.short_description = "Image"


class TagsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    form = TagsAdminForm
    save_as = True
    save_on_top = True
    list_display = ["id", "title", "slug"]
    list_display_links = ["id", "title"]
    search_fields = ["title", "description"]
    fields = ["title", "slug", "description"]


admin.site.register(Tags, TagsAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
