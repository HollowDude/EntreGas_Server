from django.db import models
from django.contrib.auth.models import User

PUESTOS = [
    ("tecnico", "Tecnico"),
    ("jefe de servicio", "Jefe de Servicio")
]

class Trabajador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    puesto = models.CharField(choices=PUESTOS, max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.puesto}"
