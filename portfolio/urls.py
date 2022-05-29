from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.home_view),
    path('Home', views.home_view, name='home'),
    path('Blog', views.blog_view, name='blog'),
    path('quizz', views.quizz_view, name='quizz'),
    path('novoPost', views.novoPost_view, name='novoPost'),
    path('editarPost/<int:post_id>', views.editarPost_view, name='editarPost'),
    path('apagarPost/<int:post_id>', views.apagarPost_view, name='apagarPost'),
    path('Apresentacao', views.apresentacao_view, name='apresentacao'),
    path('licenciatura', views.licenciatura_view, name='licenciatura'),
    path('projetos', views.projetos_view, name='projetos'),
    path('competencias', views.competencias_view, name='competencias'),
    path('formacao', views.formacao_view, name='formacao'),
    path('login', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

