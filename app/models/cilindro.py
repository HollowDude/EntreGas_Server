from datetime import date
from django.db import models
from .cliente import Cliente


class Cilindro(models.Model):
    num = models.CharField("Numero de serie", blank=True, null=True, max_length=255)
    fehca_llegada = models.DateField(default = date.today)
    defectuoso = models.BooleanField(default = False)
    lleno = models.BooleanField(default = True)
    asign = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)