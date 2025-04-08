from datetime import datetime
from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from .choices import CategoriaChoices

class Usuario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4())
    class TipoUsuario(models.TextChoices):
        VISTORIADOR = 'vis', _('Vistoriador')
        ADMINISTRADOR = 'adm', _('Administrador')
    tipo_usuario = models.CharField(choices=TipoUsuario, max_length=3)
    email = models.CharField(max_length=100)
    senha = models.CharField()
    nome_completo = models.CharField(max_length=100)


class Funcao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4())
    descricao_funcao = models.CharField(max_length=100)
    
class Genero(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    descricao_genero = models.CharField(max_length=50)

class Participante(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4())
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    telefone = models.CharField(max_length=11, default='', blank=True)
    email = models.CharField(max_length=100)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    funcao = models.ForeignKey(Funcao, on_delete=models.SET_NULL, null=True)
    
class Bairro(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4())
    class NomeZona(models.TextChoices):
        NORTE = "NORTE", "Zona Norte"
        SUL = "SUL", "Zona Sul"
        LESTE = "LESTE", "Zona Leste"
        OESTE = "OESTE", "Zona Oeste"
        CENTRO = "CENTRO", "Zona Central"
    zona = models.CharField(choices=NomeZona, max_length=6)
    nome = models.CharField(max_length=100)
    
class Clube(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4())
    nome = models.CharField(max_length=100)
    models.ForeignKey(Bairro, on_delete=models.SET_NULL, null=True, blank=True)

class Esporte(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4())
    nome = models.CharField(max_length=100)
    
class Responsavel_Time(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4())
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=11)
    email = models.CharField(max_length=100)
    
class Time(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4())
    clube = models.ForeignKey(Clube, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    # Montar um dicionário de responsável para inicializar um time
    responsavel = models.ForeignKey(Responsavel_Time, on_delete=models.SET_NULL, null=True, blank=True)
    esporte = models.ForeignKey(Esporte, on_delete=models.CASCADE)
    categoria = models.CharField(CategoriaChoices, max_length=9)

class Fase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4())
    descricao = models.CharField(max_length=100)

class Jogo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4())
    tempo_inicio = models.DateTimeField(default=datetime.now)
    tempo_fim = models.DateTimeField(null=True, blank=True)
    pontuacao_time1 = models.IntegerField(default=0)
    pontuacao_time2 = models.IntegerField(default=0)
    time_1 = models.ForeignKey(Time, on_delete=models.CASCADE, related_name='jogos_como_time_1')
    time_2 = models.ForeignKey(Time, on_delete=models.CASCADE, related_name='jogos_como_time_2')
    vencedor = models.ForeignKey(Time, on_delete=models.CASCADE, related_name='vitorias', null=True, blank=True)
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE)

class Torneio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4())
    categoria = models.CharField(max_length=9, choices=CategoriaChoices)
    esporte = models.ForeignKey(Esporte, on_delete=models.CASCADE)
    vencedor = models.ForeignKey(Time, on_delete=models.SET_NULL, null=True, blank=True)

    
class Ocorrencia(models.Model):    
    class TipoOcorrencia(models.TextChoices):
        GOL = 'gol', _('Gol')
        AMARELO_FALTA = 'am_ft', _('Cartão Amarelo: falta')
        AMARELO_MISC = 'am_misc', _('Cartão Amarelo: outros motivos')
        VERMELHO_FALTA = 'verm_ft', _('Cartão Vermelho: falta')
        VERMELHO_MISC = 'verm_misc', _('Cartão Vermelho: outros motivos')
        FALTA = 'ft', _('Falta')
        
    id = models.UUIDField(primary_key=True, default=uuid4())
    tipo_ocorrencia = models.CharField(choices=TipoOcorrencia)
    tempo_jogo = models.TimeField(auto_now=False, auto_now_add=False)
    envolvidos = models.ManyToManyField(Participante, through="OcorrenciaParticipante")
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE)
    
class OcorrenciaParticipante(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4())
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE)
    class Envolvimento(models.TextChoices):
        CAUSADOR = 'cs', _('Causador')
        VITIMA = 'vi', _('Vítima')
        ENVOLVIDO = 'ev', ('Envolvido')
    envolvimento = models.CharField(max_length=2, choices=Envolvimento)
    ocorrencia = models.ForeignKey(Ocorrencia, on_delete=models.CASCADE)