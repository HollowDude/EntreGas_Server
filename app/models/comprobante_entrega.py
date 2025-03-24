from django.db import models
from .cliente import Cliente
from .cilindro import Cilindro

class Comprobante_Entrega(models.Model):
    fecha = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cilindroE = models.ForeignKey(Cilindro, on_delete=models.CASCADE, related_name='comprobantes_entrada')
    cilindroS = models.ForeignKey(Cilindro, on_delete=models.CASCADE, related_name='comprobantes_salida')


