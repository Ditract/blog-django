from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm

def lista_posts(request):
    posts = Post.objects.all()
    return render(request, 'blog/lista_posts.html', {'posts': posts})

def detalle_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    return render(request, 'blog/detalle_post.html', {'post': post})

def crear_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_posts')
    else:
        form = PostForm()
    return render(request, 'blog/crear_post.html', {'form': form})

def editar_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('lista_posts')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/editar_post.html', {'form': form})

def eliminar_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('lista_posts')
    return render(request, 'blog/eliminar_post.html', {'post': post})