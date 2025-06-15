from rest_framework import serializers
from app.models.comprobante_entrega import Comprobante_Entrega

class Comprobante_EntregaSerializer(serializers.ModelSerializer):
    cliente = serializers.CharField()

    class Meta:
        model = Comprobante_Entrega
        fields = ['fecha', 'cilindroE', 'cilindroS', 'cliente']

    def create(self, validated_data):
        username = validated_data.pop('cliente')
        from app.models.cliente import Cliente
        cliente = Cliente.objects.filter(user__username=username).first()
        if not cliente:
            raise serializers.ValidationError({'cliente': 'Cliente no encontrado'})
        return Comprobante_Entrega.objects.create(cliente=cliente, **validated_data)
    