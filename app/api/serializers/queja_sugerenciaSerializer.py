from rest_framework import serializers
from app.models.queja_sugerencia import Queja_sugerencia


class Queja_sugerenciaSerializer(serializers.ModelSerializer):
    cliente = serializers.CharField(source='cliente.user.username', required=False)

    class Meta:
        model = Queja_sugerencia
        fields = ['fecha', 'cliente', 'mensaje']
