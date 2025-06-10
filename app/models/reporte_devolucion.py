from django.db import models
from .cliente import Cliente
from .cilindro import Cilindro

class Reporte_Devolucion(models.Model):
    fecha = models.DateField(null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    cilindro = models.ForeignKey(Cilindro, on_delete=models.CASCADE, null=True, blank=True)
    defecto = models.TextField(max_length = 255)
