from django.urls import path
from afrocamp_app import views

urlpatterns = [
    path('login/', views.login),
    path('jogos/', views.jogos),
    path('jogos/<uuid:id_jogo>/', views.detalhes_jogo, name='id_jogo'),
    path('times/', views.times),
    path('participantes/', views.participantes),
    path('torneio/', views.torneio)
]