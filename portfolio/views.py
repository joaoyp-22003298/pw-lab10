import base64
import datetime
import io
import urllib

import matplotlib
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from matplotlib import pyplot as plt

from .forms import PostForm
from .models import Post, PontuacaoQuizz

matplotlib.use('Agg')


# if not request.user.is_authenticated:
#   return HttpResponseRedirect(reverse('portfolio:login'))

def home_view(request):
    hoje = datetime.date.today()
    nasc = datetime.date(1998, 7, 7)
    anos = (hoje - nasc).days // 365

    context = {
        'anos': anos
    }
    return render(request, 'portfolio/home.html', context)


def apresentacao_view(request):
    hoje = datetime.date.today()
    nasc = datetime.date(1998, 7, 7)
    anos = (hoje - nasc).days // 365

    context = {
        'anos': anos
    }
    return render(request, 'portfolio/apresentacao.html', context)


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


def desenha_grafico_resultados(request):
    pontuacoes = PontuacaoQuizz.objects.all().order_by('pontuacao')
    lista_nomes = []
    lista_pontuacao = []

    for person in pontuacoes:
        lista_nomes.append(person.nome)
        lista_pontuacao.append(person.pontuacao)

    plt.barh(lista_nomes, lista_pontuacao)
    plt.ylabel("Pontuação")
    plt.savefig('portfolio/static/portfolio/images/graf.png', bbox_inches='tight')

    plt.autoscale()

    fig = plt.gcf()
    plt.close()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')

    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return uri


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

    context = {
        'data': desenha_grafico_resultados(request),
    }

    return render(request, 'portfolio/quizz.html', context)


def novaCadeira_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('portfolio:login'))

    return render(request, 'portfolio/novaCadeira.html')


def novoProjeto_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('portfolio:login'))

    return render(request, 'portfolio/novoProjeto.html')


def editarCadeira_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('portfolio:login'))

    return render(request, 'portfolio/editarCadeira.html')


def editarProjeto_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('portfolio:login'))

    return render(request, 'portfolio/editarProjeto.html')
