from django.contrib import admin
from .models import Post, PontuacaoQuizz, Cadeira, Professor, Projeto, Picture

# Register your models here.

admin.site.register(Post)
admin.site.register(PontuacaoQuizz)
admin.site.register(Cadeira)
admin.site.register(Professor)
admin.site.register(Projeto)
admin.site.register(Picture)
