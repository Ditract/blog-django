from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Post(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.titulo