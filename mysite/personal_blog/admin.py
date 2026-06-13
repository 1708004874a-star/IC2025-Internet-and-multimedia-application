from django.contrib import admin
from .models import Post, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'publication_date', 'category', 'is_published']
    list_filter = ['is_published', 'category', 'tags', 'publication_date']
    search_fields = ['title', 'content']
    date_hierarchy = 'publication_date'
    filter_horizontal = ['tags']
