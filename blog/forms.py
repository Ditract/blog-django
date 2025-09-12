from django import forms
from blog.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo','contenido', 'categorias']
        widgets = {
            'categorias': forms.CheckboxSelectMultiple(),
        }

class SearchForm(forms.Form):
    q = forms.CharField(max_length=100, required=False, label='Buscar...')