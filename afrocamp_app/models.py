from datetime import datetime
from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from .choices import CategoriaChoices

class Usuario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    class TipoUsuario(models.TextChoices):
        VISTORIADOR = 'vis', _('Vistoriador')
        ADMINISTRADOR = 'adm', _('Administrador')
    tipo_usuario = models.CharField(choices=TipoUsuario, max_length=3, default='vis')
    email = models.CharField(max_length=100)
    senha = models.CharField()
    nome_completo = models.CharField(max_length=100)


class Funcao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    def __str__(self):
        return self.descricao_funcao
    descricao_funcao = models.CharField(max_length=100)
    
class Bairro(models.Model):
    def __str__(self):
        return self.nome
    
    id = models.UUIDField(primary_key=True, default=uuid4)
    class NomeZona(models.TextChoices):
        NORTE = "NORTE", "Zona Norte"
        SUL = "SUL", "Zona Sul"
        LESTE = "LESTE", "Zona Leste"
        OESTE = "OESTE", "Zona Oeste"
        CENTRO = "CENTRO", "Zona Central"
    zona = models.CharField(choices=NomeZona, max_length=6)
    nome = models.CharField(max_length=100)
    
class Clube(models.Model):
    def __str__(self):
        return self.nome
    
    id = models.UUIDField(primary_key=True, default=uuid4)
    nome = models.CharField(max_length=100)
    models.ForeignKey(Bairro, on_delete=models.SET_NULL, null=True, blank=True)

class Esporte(models.Model):
    def __str__(self):
        return self.nome
    
    id = models.UUIDField(primary_key=True, default=uuid4)
    nome = models.CharField(max_length=100)
    
class Responsavel_Time(models.Model):
    def __str__(self):
        return self.nome
    
    id = models.UUIDField(primary_key=True, default=uuid4)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=11)
    email = models.CharField(max_length=100)
    
class Time(models.Model):
    def __str__(self):
        return self.nome
    
    id = models.UUIDField(primary_key=True, default=uuid4)
    clube = models.ForeignKey(Clube, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    responsavel = models.ForeignKey(Responsavel_Time, on_delete=models.SET_NULL, null=True, blank=True)
    esporte = models.ForeignKey(Esporte, on_delete=models.CASCADE)
    categoria = models.CharField(choices=CategoriaChoices, max_length=9)
    
    
class Participante(models.Model):
    def __str__(self):
        return self.nome
    
    id = models.UUIDField(primary_key=True, default=uuid4)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    telefone = models.CharField(max_length=11, default='', blank=True)
    email = models.CharField(max_length=100)
    
    class Genero(models.TextChoices):
        MASCULINO = "MASCULINO", "Masculino"
        FEMININO = "FEMININO", "Feminino"
        OUTRO = "OUTRO", "Outro"
    genero = models.CharField(choices=Genero, max_length=10)
    time = models.ForeignKey(Time, on_delete=models.SET_NULL, null=True)
    funcao = models.ForeignKey(Funcao, on_delete=models.SET_NULL, null=True)

class Fase(models.Model):
    def __str__(self):
        return self.descricao
    
    id = models.UUIDField(primary_key=True, default=uuid4)
    descricao = models.CharField(max_length=100)

class Jogo(models.Model):
    def __str__(self):
        return f"{self.time_1} X {self.time_2} | {self.tempo_inicio}"
    
    
    id = models.UUIDField(primary_key=True, default=uuid4)
    tempo_inicio = models.DateTimeField(default=datetime.now)
    tempo_fim = models.DateTimeField(null=True, blank=True)
    pontuacao_time1 = models.IntegerField(default=0)
    pontuacao_time2 = models.IntegerField(default=0)
    time_1 = models.ForeignKey(Time, on_delete=models.CASCADE, related_name='jogos_como_time_1')
    time_2 = models.ForeignKey(Time, on_delete=models.CASCADE, related_name='jogos_como_time_2')
    vencedor = models.ForeignKey(Time, on_delete=models.CASCADE, related_name='vitorias', null=True, blank=True)
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE)

class Torneio(models.Model):
    def __str__(self):
        return f"{self.esporte} - {self.get_categoria_display()}"
    
    id = models.UUIDField(primary_key=True, default=uuid4)
    categoria = models.CharField(max_length=9, choices=CategoriaChoices)
    esporte = models.ForeignKey(Esporte, on_delete=models.CASCADE)
    vencedor = models.ForeignKey(Time, on_delete=models.SET_NULL, null=True, blank=True, default=None)

    
class Ocorrencia(models.Model):
    def __str__(self):
        return f"{self.get_tipo_ocorrencia_display()} no {self.jogo}"
    class TipoOcorrencia(models.TextChoices):
        GOL = 'gol', _('Gol')
        AMARELO_FALTA = 'am_ft', _('Cartão Amarelo: falta')
        AMARELO_MISC = 'am_misc', _('Cartão Amarelo: outros motivos')
        VERMELHO_FALTA = 'verm_ft', _('Cartão Vermelho: falta')
        VERMELHO_MISC = 'verm_misc', _('Cartão Vermelho: outros motivos')
        FALTA = 'ft', _('Falta')
        
    id = models.UUIDField(primary_key=True, default=uuid4)
    tipo_ocorrencia = models.CharField(choices=TipoOcorrencia)
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE)
    tempo_jogo = models.DurationField()
    envolvidos = models.ManyToManyField(Participante, through="OcorrenciaParticipante")
    def save(self, *args, **kwargs):
        if not self.tempo_jogo and self.jogo and self.jogo.tempo_inicio:
            self.tempo_jogo = datetime.now() - self.jogo.tempo_inicio
        super().save(*args, **kwargs)
    
class OcorrenciaParticipante(models.Model):
    def __str__(self):
        return f"{self.participante} {self.get_envolvimento_display()} de {self.ocorrencia}"
    id = models.UUIDField(primary_key=True, default=uuid4)
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE)
    class Envolvimento(models.TextChoices):
        CAUSADOR = 'cs', _('Causador')
        VITIMA = 'vi', _('Vítima')
        ENVOLVIDO = 'ev', ('Envolvido')
    envolvimento = models.CharField(max_length=2, choices=Envolvimento)
    ocorrencia = models.ForeignKey(Ocorrencia, on_delete=models.CASCADE)