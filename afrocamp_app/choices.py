from django.db import models
from django.utils.translation import gettext_lazy as _

class CategoriaChoices(models.TextChoices):
    SUB_11_MASC = 'sub_11_mc', _('Sub 11 Masculino')
    SUB_20_MASC = 'sub_20_mc', _('Sub 20 Masculino')
    ADULTO_MASC = 'adulto_mc', _('Adulto Masculino')
    SENIOR_MASC = 'senior_mc', _('Sênior Masculino')
    SUB_11_FEM = 'sub_11_fm', _('Sub 11 Feminino')
    SUB_20_FEM = 'sub_20_fm', _('Sub 20 Feminino')
    ADULTO_FEM = 'adulto_fm', _('Adulto Feminino')
    SENIOR_FEM = 'senior_fm', _('Sênior Feminino')