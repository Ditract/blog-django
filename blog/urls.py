from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListaPostsView.as_view(), name='lista_posts'),
    path('categoria/<int:categoria_id>/', views.ListaPostsView.as_view(), name='posts_por_categoria'),
    path('<int:pk>/', views.DetallePostView.as_view(), name='detalle_post'),
    path('nuevo/', views.CrearPostView.as_view(), name='crear_post'),
    path('editar/<int:pk>/', views.EditarPostView.as_view(), name='editar_post'),
    path('eliminar/<int:pk>/', views.EliminarPostView.as_view(), name='eliminar_post'),
    path('comment/<int:pk>/', views.CommentCreateView.as_view(), name='comment_create'),
    path('register/', views.register, name='register'),
]