from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField

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
    avatar = CloudinaryField('avatar', blank=True, null=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return "https://res.cloudinary.com/dt8cem7zx/image/upload/v1758148462/default_lb86o0.png"