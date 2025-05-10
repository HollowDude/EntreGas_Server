from django.contrib.auth.models import User
from django.db import models

TIPOS = [
    ("normal", "Normal"),
    ("especial", "Especial")
]

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length = 255)
    tipo = models.CharField(choices=TIPOS, max_length=255)
    fecha_UT = models.DateField()
    fecha_PC = models.DateField()