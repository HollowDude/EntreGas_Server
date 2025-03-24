from rest_framework import serializers
from app.models.comprobante_entrega import Comprobante_Entrega

class Comprobante_EntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comprobante_Entrega
        fields = '__all__'
