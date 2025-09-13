from django.contrib import admin

from blog.models import Post, Category, Comment


# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'fecha']
    list_filter = ['categorias', 'autor', 'fecha']
    filter_horizontal = ['categorias']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['nombre']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'autor', 'fecha']
    list_filter = ['post', 'autor', 'fecha']