from django.contrib import admin

from blog.models import Post, Category

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'fecha']
    list_filter = ['categorias', 'autor', 'fecha']
    filter_horizontal = ['categorias']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['nombre']