from django.shortcuts import render
from .models import *

def login(request):
    return render(request, 'pages/login.html')

def jogos(request):
    jogos = Jogo.objects.all().order_by('tempo_fim')
    context = {
        'jogos': jogos
    }
    return render(request, 'pages/jogos.html', context)

def detalhes_jogo(request, id_jogo):
    jogo = Jogo.objects.get(id=id_jogo)
    ocorrencias = Ocorrencia.objects.filter(jogo=jogo).order_by('-tempo_jogo')
    
    ocorrencias_detalhes = []
    for o in ocorrencias:
        envolvidos = []
        ocorrencia_participantes = o.ocorrenciaparticipante_set.all()
        for op in ocorrencia_participantes:
            envolvidos.append({
                "participante": op.participante,
                "envolvimento": op.get_envolvimento_display()
            })
            
        ocorrencias_detalhes.append({
            "tipo_ocorrencia": o.get_tipo_ocorrencia_display(),
            "tempo_jogo": o.tempo_jogo,
            "envolvidos": envolvidos
        })


    context = {
        'jogo': jogo,
        'ocorrencias': ocorrencias_detalhes
    }
    print(ocorrencias_detalhes)
    return render(request, 'pages/jogo_detalhes.html', context)

def times(request):
    return render(request, 'pages/times.html')

def participantes(request):
    return render(request, 'pages/participantes.html')

def torneio(request):
    return render(request, 'pages/torneio.html')