from django.db import models
from .cliente import Cliente
from .cilindro import Cilindro

class Reporte_Devolucion(models.Model):
    fecha = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cilindro = models.ForeignKey(Cilindro, on_delete=models.CASCADE)
    defecto = models.TextField(max_length = 255)
