from django.contrib.auth.models import User
from django.db import models

TIPOS = [
    ("Normal", "Normal"),
    ("Especial", "Especial")
]

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length = 255)
    tipo = models.CharField(choices=TIPOS, max_length=255)
    fecha_UT = models.DateField(null=True, blank=True)
    fecha_PC = models.DateField(null=True, blank=True)