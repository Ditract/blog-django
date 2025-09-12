from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Category(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Post(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    categorias = models.ManyToManyField(Category, related_name='posts', blank=True)

    class Meta:
        ordering = ['-fecha']  # 👈 siempre ordena por fecha descendente

    def __str__(self):
        return self.titulo
