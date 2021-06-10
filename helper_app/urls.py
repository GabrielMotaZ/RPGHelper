from django.urls import path
from . import views

urlpatterns = [
    path('sala/', views.room, name='room'),
    path('login/', views.login, name='login'),
    path('entrar/', views.validate, name='validate'),
    path('selecao/', views.select, name='select'),
    path('registrar/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('test/', views.test, name='test'),
    path('editarSkill/', views.editSkill, name='editSkill'),
    path('criarSkill/', views.createSkill, name='createSkill'),
    path('criarPersonagem/', views.createChar, name='createChar'),
    path('deletarSkill/', views.deleteSkill, name='deleteSkill'),
]