from rest_framework import serializers
from app.models.comprobante_abastecimiento import Comprobante_Abastecimiento

class Comprobante_AbastecimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comprobante_Abastecimiento
        fields = '__all__'
