import datetime
import matplotlib
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .forms import PostForm
from .models import Post, PontuacaoQuizz
from matplotlib import pyplot as plt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


matplotlib.use('Agg')


def home_view(request):
    hoje = datetime.date.today()
    nasc = datetime.date(1998, 7, 7)
    anos = (hoje - nasc).days // 365

    context = {
        'anos': anos
    }
    return render(request, 'portfolio/home.html', context)


def apresentacao_view(request):
    return render(request, 'portfolio/apresentacao.html')


def blog_view(request):
    context = {'posts': Post.objects.all()}
    return render(request, 'portfolio/blog.html', context)


def licenciatura_view(request):
    return render(request, 'portfolio/licenciatura.html')


def competencias_view(request):
    return render(request, 'portfolio/competencias.html')


def projetos_view(request):
    return render(request, 'portfolio/projetos.html')


def formacao_view(request):
    return render(request, 'portfolio/formacao.html')


def login_view(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('portfolio:home'))
        else:
            return render(request, 'portfolio/login.html', {
                'message': 'Credenciais inválidas.'
            })

    return render(request, 'portfolio/login.html')


def logout_view(request):
    logout(request)

    return render(request, 'portfolio/login.html', {
                'message': 'Obrigado pela visita!'
            })


def novoPost_view(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('portfolio:blog'))

    context = {
        'form': form
    }

    return render(request, 'portfolio/novoPost.html', context)


def editarPost_view(request, post_id):
    post = Post.objects.get(pk=post_id)
    form = PostForm(request.POST or None, instance=post)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('portfolio:blog'))

    context = {'form': form, 'post_id': post_id}
    return render(request, 'portfolio/editarPost.html', context)


def apagarPost_view(request, post_id):
    Post.objects.get(pk=post_id).delete()
    return HttpResponseRedirect(reverse('portfolio:blog'))


def pontuacao_quizz(request):
    score = 0
    if request.POST['p1'] == 'javascript':
        score += 1

    if request.POST['p2'] == 'Elementos_Semanticos':
        score += 1

    if request.POST['p3'] == 'TopRightBotLeft':
        score += 1

    if request.POST['p4'] == 'def_Function':
        score += 1

    if request.POST['p5'] == 'conf_url_view_html':
        score += 1

    return score


def quizz_view(request):
    if request.method == 'POST':
        n = request.POST['nome']
        p = pontuacao_quizz(request)
        r = PontuacaoQuizz(nome=n, pontuacao=p)
        r.save()

    desenha_grafico_resultados(request)
    return render(request, 'portfolio/quizz.html')


def desenha_grafico_resultados(request):
    pontuacoes = PontuacaoQuizz.objects.all()
    pontuacao_sorted = sorted(pontuacoes, key=lambda objeto: objeto.pontuacao, reverse=False)
    lista_nomes = []
    lista_pontuacao = []

    for person in pontuacao_sorted:
        lista_nomes.append(person.nome)
        lista_pontuacao.append(person.pontuacao)

    plt.barh(lista_nomes, lista_pontuacao)
    plt.savefig('portfolio/static/portfolio/images/graf.png', bbox_inches='tight')
