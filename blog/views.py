from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Post, Category
from .forms import PostForm, SearchForm, CustomUserCreationForm


class ListaPostsView(ListView):
    model = Post
    template_name = 'blog/lista_posts.html'
    context_object_name = 'page_obj'
    paginate_by = 5  # Paginación

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

        # Título dinámico
        if context['query']:
            if context['categoria_id']:
                categoria = get_object_or_404(Category, id=context['categoria_id'])
                context['titulo'] = f'Resultados de "{context["query"]}" en {categoria.nombre}'
            else:
                context['titulo'] = f'Resultados de búsqueda para "{context["query"]}"'
        elif context['categoria_id']:
            categoria = get_object_or_404(Category, id=context['categoria_id'])
            context['titulo'] = f'Posts en {categoria.nombre}'
        else:
            context['titulo'] = 'Todos los Posts'

        return context


class DetallePostView(DetailView):
    model = Post
    template_name = 'blog/detalle_post.html'
    context_object_name = 'post'


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
    success_url = reverse_lazy('lista_posts')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.autor


class EliminarPostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/eliminar_post.html'
    success_url = reverse_lazy('lista_posts')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.autor


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            # Imprime los errores con sus códigos
            for field in form:
                for error in field.errors:
                    error_data = form.errors[field.name].as_data()
                    for err in error_data:
                        print(f"Field: {field.name}, Error: {err.message}, Code: {err.code}")
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})