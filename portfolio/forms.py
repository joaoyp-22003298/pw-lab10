from django.forms import ModelForm
from django import forms
from .models import Post, Cadeira, Projeto


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


class CadeiraForm(ModelForm):
    class Meta:
        model = Cadeira
        fields = '__all__'


class ProjetoForm(ModelForm):
    class Meta:
        model = Projeto
        fields = '__all__'
