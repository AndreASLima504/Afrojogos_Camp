from django.urls import path
from afrocamp_app import views

urlpatterns = [
    path('login/', views.login),
    path('jogos/', views.jogos),
    path('times/', views.times),
    path('participantes/', views.participantes),
    path('torneio/', views.torneio)
]