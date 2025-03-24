from rest_framework import serializers
from app.models.reporte_devolucion import Reporte_Devolucion

class Reporte_DevolucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte_Devolucion
        fields = '__all__'
