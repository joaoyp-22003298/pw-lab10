from django.forms import ModelForm
from django import forms
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

        # ferramentas
        widgets = {
            'autor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Autor do Post'}),

            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título do Post'}),
        }
