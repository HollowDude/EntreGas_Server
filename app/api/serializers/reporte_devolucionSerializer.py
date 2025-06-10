from rest_framework import serializers
from app.models.reporte_devolucion import Reporte_Devolucion


class Reporte_DevolucionSerializer(serializers.ModelSerializer):
    cliente = serializers.CharField(source='cliente.id', required=False)

    class Meta:
        model = Reporte_Devolucion
        fields = ['fecha', 'cilindro', 'cliente', 'defecto']
        extra_kwargs = {
            'fecha': {'required': False},
            'cilindro': {'required': False},
            'defecto': {'required': False}
        }
