from django.shortcuts import render

def login(request):
    return render(request, 'pages/login.html')

def jogos(request):
    return render(request, 'pages/jogos.html')

def times(request):
    return render(request, 'pages/times.html')

def participantes(request):
    return render(request, 'pages/participantes.html')

def torneio(request):
    return render(request, 'pages/torneio.html')