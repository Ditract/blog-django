from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from blog.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'contenido', 'categorias', 'imagen']
        widgets = {
            'categorias': forms.CheckboxSelectMultiple(),
            'imagen': forms.FileInput(),
        }

class SearchForm(forms.Form):
    q = forms.CharField(max_length=100, required=False, label='Buscar...')

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].error_messages.update({
            'password_too_similar': _('La contraseña es demasiado similar al nombre de usuario.'),
            'password_too_common': _('Esta contraseña es demasiado común.'),
            'password_entirely_numeric': _('Esta contraseña no puede ser completamente numérica.'),
        })
        self.fields['password2'].error_messages.update({
            'password_mismatch': _('Las contraseñas no coinciden.'),
            'password_too_similar': _('La contraseña es demasiado similar al nombre de usuario.'),
            'password_too_common': _('Esta contraseña es demasiado común.'),
            'password_entirely_numeric': _('Esta contraseña no puede ser completamente numérica.'),
        })


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def clean_contenido(self):
        contenido = self.cleaned_data['contenido']
        if len(contenido) < 5:
            raise ValidationError("El comentario debe tener al menos 5 caracteres.")
        return contenido