from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField
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
    imagen = CloudinaryField('image', blank=True, null=True)

    # Imagen optimizada para las cards
    imagen_card = ImageSpecField(
        source='imagen',
        processors=[ResizeToFill(400, 250)],
        format='JPEG',
        options={'quality': 95}
    )

    # Imagen optimizada para el detalle del post
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

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.autor.username} en {self.post.titulo}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    avatar = CloudinaryField('avatar', blank=True, null=True, default='avatars/default.png')

    def __str__(self):
        return f'Perfil de {self.user.username}'