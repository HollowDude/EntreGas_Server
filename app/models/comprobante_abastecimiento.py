from django.db import models
from .trabajador import Trabajador

class Comprobante_Abastecimiento(models.Model):
    fecha = models.DateField()
    cant_cilindros = models.IntegerField()
    proveedor = models.CharField(max_length = 50)
    trabajador_recivio = models.ForeignKey(Trabajador, on_delete=models.CASCADE)


