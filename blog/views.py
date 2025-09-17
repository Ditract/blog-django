from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Post, Category, Comment, Profile
from .forms import PostForm, SearchForm, CommentForm, ProfileForm
from django.urls import reverse
from django.contrib import messages



class HomeView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 6  # Mostrar 6 posts

    def get_queryset(self):
        return Post.objects.all().order_by('-fecha')[:6]  # Últimos 6 posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Bienvenido a Mi Blog'
        if self.request.user.is_authenticated:
            context['bienvenida'] = f'¡Hola, {self.request.user.username}!'
        else:
            context['bienvenida'] = '¡Explora los últimos posts!'
        return context


class ListaPostsView(ListView):
    model = Post
    template_name = 'blog/lista_posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        categoria_id = self.kwargs.get('categoria_id')

        if query:
            queryset = queryset.filter(Q(titulo__icontains=query) | Q(contenido__icontains=query))
        if categoria_id:
            queryset = queryset.filter(categorias__id=categoria_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Category.objects.all()
        context['search_form'] = SearchForm(self.request.GET)
        context['query'] = self.request.GET.get('q')
        context['categoria_id'] = self.kwargs.get('categoria_id')

        if context['query']:
            if context['categoria_id']:
                categoria = Category.objects.get(id=context['categoria_id'])
                context['titulo'] = f'Resultados de "{context["query"]}" en {categoria.nombre}'
            else:
                context['titulo'] = f'Resultados de búsqueda para "{context["query"]}"'
        elif context['categoria_id']:
            categoria = Category.objects.get(id=context['categoria_id'])
            context['titulo'] = f'Posts en {categoria.nombre}'
        else:
            context['titulo'] = 'Todos los Posts'

        return context


class DetallePostView(DetailView):
    model = Post
    template_name = 'blog/detalle_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        referer = self.request.META.get('HTTP_REFERER', '')
        if '/perfil/' in referer:
            context['back_url'] = reverse('profile', kwargs={'username': self.request.user.username})
        else:
            context['back_url'] = reverse('lista_posts')
        return context


class CrearPostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/crear_post.html'
    success_url = reverse_lazy('lista_posts')

    def form_valid(self, form):
        form.instance.autor = self.request.user
        response = super().form_valid(form)
        form.instance.categorias.set(form.cleaned_data['categorias'])
        return response



class EditarPostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/editar_post.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.autor

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '¡El post se ha actualizado correctamente!')
        return response

    def get_success_url(self):
        return reverse('detalle_post', kwargs={'pk': self.object.pk})


class EliminarPostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/eliminar_post.html'
    success_url = reverse_lazy('lista_posts')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.autor


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/detalle_post.html'

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detalle_post', kwargs={'pk': self.kwargs['pk']})


class ProfileView(DetailView):
    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile_user'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile'] = self.object.profile
        except Profile.DoesNotExist:
            context['profile'] = None
        context['posts'] = Post.objects.filter(autor=self.object).order_by('-fecha')
        return context


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'blog/profile_edit.html'
    success_url = reverse_lazy('lista_posts')

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def test_func(self):
        return self.request.user == self.get_object().user


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].error_messages = {
            'password_too_short': 'La contraseña es demasiado corta. Debe contener al menos 8 caracteres.',
            'password_too_common': 'La contraseña es demasiado común.',
            'password_entirely_numeric': 'La contraseña no puede ser completamente numérica.',
        }
        self.fields['password2'].error_messages = {
            'password_mismatch': 'Las contraseñas no coinciden.',
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 4:
            raise ValidationError("El nombre de usuario debe tener al menos 4 caracteres.")
        if ' ' in username:
            raise ValidationError("El nombre de usuario no puede contener espacios.")
        return username


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})