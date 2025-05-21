from datetime import date
from django.db import models
from .cliente import Cliente


class Cilindro(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    fehca_llegada = models.DateField(default = date.today)
    defectuoso = models.BooleanField(default = False)
    lleno = models.BooleanField(default = True)
    asign = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)