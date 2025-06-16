from rest_framework import serializers
from app.models.comprobante_entrega import Comprobante_Entrega

class Comprobante_EntregaSerializer(serializers.ModelSerializer):

    cliente = serializers.CharField(source='cliente.user.username')

    class Meta:
        model = Comprobante_Entrega
        fields = ['fecha', 'cilindroE', 'cilindroS', 'cliente']