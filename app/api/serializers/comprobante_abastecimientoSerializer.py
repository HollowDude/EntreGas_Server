from rest_framework import serializers
from app.models.comprobante_abastecimiento import Comprobante_Abastecimiento

class Comprobante_AbastecimientoSerializer(serializers.ModelSerializer):

    trabajador_recibio = serializers.CharField(source='trabajador_recibio.user.username', read_only=True)
    class Meta:
        model = Comprobante_Abastecimiento
        fields = [
            'fecha',
            'cant_cilindros',
            'proveedor',
            'trabajador_recibio'
        ]
