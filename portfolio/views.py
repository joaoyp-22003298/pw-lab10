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

from .forms import PostForm, ProjetoForm, CadeiraForm
from .models import Post, PontuacaoQuizz, Projeto, Cadeira

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


def blog_view(request):
    context = {'posts': Post.objects.all()}
    return render(request, 'portfolio/blog.html', context)


def licenciatura_view(request):
    context = {'cadeiras': Cadeira.objects.all()}
    return render(request, 'portfolio/licenciatura.html', context)


def competencias_view(request):
    return render(request, 'portfolio/competencias.html')


def projetos_view(request):
    context = {'projetos': Projeto.objects.all()}
    return render(request, 'portfolio/projetos.html', context)


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
    plt.xlabel("Pontuações: ")
    plt.ylabel("Nomes: ")
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

    form = CadeiraForm(request.POST, request.FILES or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('portfolio:licenciatura'))

    context = {'form': form}

    return render(request, 'portfolio/novaCadeira.html', context)


def novoProjeto_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('portfolio:login'))

    form = ProjetoForm(request.POST, request.FILES or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('portfolio:projetos'))

    context = {'form': form}

    return render(request, 'portfolio/novoProjeto.html', context)


def editarCadeira_view(request, cadeira_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('portfolio:login'))

    cadeira = Cadeira.objects.get(id=cadeira_id)
    form = CadeiraForm(request.POST or request.FILES or None, instance=cadeira)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('portfolio:licenciatura'))

    context = {'form': form, 'cadeira_id': cadeira_id}
    return render(request, 'portfolio/editarCadeira.html', context)


def apagarCadeira_view(request, cadeira_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('portfolio:login'))

    cadeira = Cadeira.objects.get(id=cadeira_id)
    cadeira.delete()
    return HttpResponseRedirect(reverse('portfolio:licenciatura'))


def editarProjeto_view(request, projeto_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('portfolio:login'))

    projeto = Projeto.objects.get(id=projeto_id)
    form = ProjetoForm(request.POST or request.FILES or None, instance=projeto)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('portfolio:projetos'))

    context = {'form': form, 'projeto_id': projeto_id}
    return render(request, 'portfolio/editarProjeto.html', context)


def apagarProjeto_view(request, projeto_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('portfolio:login'))

    projeto = Projeto.objects.get(id=projeto_id)
    projeto.delete()
    return HttpResponseRedirect(reverse('portfolio:projetos'))


def labs_view(request):
    return render(request, 'portfolio/labs.html')
