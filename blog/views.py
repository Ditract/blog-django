from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Post, Category
from .forms import PostForm


def lista_posts(request, categoria_id=None):
    posts = Post.objects.all()
    categorias = Category.objects.all()

    if categoria_id:
        categoria = get_object_or_404(Category, id=categoria_id)
        posts = posts.filter(categorias=categoria)
        titulo = f'Posts en {categoria.nombre}'
    else:
        titulo = 'Todos los Posts'

    return render(request, 'blog/lista_posts.html', {
        'posts': posts,
        'categorias': categorias,
        'titulo': titulo,
    })


def detalle_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    return render(request, 'blog/detalle_post.html', {'post': post})


@login_required
def crear_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.save()
            form.save_m2m()  # Guarda la relación ManyToMany después de save()
            return redirect('lista_posts')
    else:
        form = PostForm()
    return render(request, 'blog/crear_post.html', {'form': form})


@login_required
def editar_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.autor != request.user:
        return HttpResponse('No autorizado', status=403)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('lista_posts')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/editar_post.html', {'form': form})


@login_required
def eliminar_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.autor != request.user:
        return HttpResponse('No autorizado', status=403)
    if request.method == 'POST':
        post.delete()
        return redirect('lista_posts')
    return render(request, 'blog/eliminar_post.html', {'post': post})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})