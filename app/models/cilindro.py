from datetime import date
from django.db import models
from .cliente import Cliente


class Cilindro(models.Model):
    fehca_llegada = models.DateField(default = date.today)
    defectuoso = models.BooleanField(default = False)
    lleno = models.BooleanField(default = True)
    asign = models.ForeignKey(Cliente, on_delete = models.CASCADE)