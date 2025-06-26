from django.db import models
from .cliente import Cliente
from .cilindro import Cilindro

class Queja_sugerencia(models.Model):
    fecha = models.DateField(null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    mensaje = models.TextField(max_length = 255)
