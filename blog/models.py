from django.contrib.auth.models import User
from django.db import models
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill


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
    imagen = models.ImageField(upload_to='post/', blank=True, null=True)

    #imagen optimizada para las cards
    imagen_card = ImageSpecField(
        source='imagen',
        processors=[ResizeToFill(400, 250)],
        format='JPEG',
        options={'quality': 95}
    )

    #imagen optimizada para el detalle del post
    imagen_detalle = ImageSpecField(
        source='imagen',
        processors=[ResizeToFill(800, 300)],
        format='JPEG',
        options={'quality': 100}
    )

    class Meta:
        ordering = ['-fecha']  # ordena por fecha descendente

    def __str__(self):
        return self.titulo
