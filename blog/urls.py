from django.shortcuts import redirect
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.lista_posts, name='lista_posts'),
    path('<int:pk>/', views.detalle_post, name='detalle_post'),
    path('nuevo/', views.crear_post, name='crear_post'),
    path('editar/<int:pk>/', views.editar_post, name='editar_post'),
    path('eliminar/<int:pk>/', views.eliminar_post, name='eliminar_post'),
    path('register/', views.register, name='register'),
]