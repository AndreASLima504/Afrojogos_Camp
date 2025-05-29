from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Funcao)
admin.site.register(Jogo)
admin.site.register(Time)

@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'funcao', 'time', 'telefone']
    

admin.site.register(Bairro)
admin.site.register(Clube)
admin.site.register(Esporte)
admin.site.register(Responsavel_Time)
admin.site.register(Fase)
admin.site.register(Torneio)
admin.site.register(Ocorrencia)
admin.site.register(OcorrenciaParticipante)
