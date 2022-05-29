from django.db import models


# Create your models here.

class Post(models.Model):
    autor = models.CharField(max_length=25)
    data = models.DateField(auto_now_add=True)
    titulo = models.CharField(max_length=30)
    descricao = models.TextField()

    def __str__(self):
        return f"{self.titulo}, {self.autor} - {self.data}"


class PontuacaoQuizz(models.Model):
    nome = models.CharField(max_length=25)
    pontuacao = models.IntegerField(default=0)

    def __str__(self):
        return self.nome
