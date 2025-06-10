from rest_framework import serializers
from app.models.comprobante_entrega import Comprobante_Entrega

class Comprobante_EntregaSerializer(serializers.ModelSerializer):
    cliente_username = serializers.CharField(source='cliente.user.username', read_only=True)
    class Meta:
        model = Comprobante_Entrega
        fields = [
            'fecha',
            'cilindroE',
            'cilindroS',
            'cliente',
            'cliente_username'
        ]

