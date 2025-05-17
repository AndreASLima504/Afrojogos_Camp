from django.shortcuts import render
from .models import *

def login(request):
    return render(request, 'pages/login.html')

def jogos(request):
    jogos = Jogo.objects.all().order_by('-tempo_fim')
    context = {
        'jogos': jogos
    }
    return render(request, 'pages/jogos.html', context)

def times(request):
    return render(request, 'pages/times.html')

def participantes(request):
    return render(request, 'pages/participantes.html')

def torneio(request):
    return render(request, 'pages/torneio.html')