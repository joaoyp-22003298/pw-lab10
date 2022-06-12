from django.db import models


# Create your models here.
class Picture(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pictures/', blank=True)


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


class Professor(models.Model):
    nome = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.nome}"


class Cadeira(models.Model):
    nome = models.CharField(max_length=55)
    descricao = models.TextField(max_length=300)
    ects = models.FloatField(default=5.0)
    ranking = models.IntegerField(default=4)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome}, {self.professor}"


class Projeto(models.Model):
    titulo = models.CharField(max_length=45)
    descricao = models.TextField(max_length=600)
    imagem = models.ImageField(upload_to='pictures/')

    def __str__(self):
        return self.titulo
