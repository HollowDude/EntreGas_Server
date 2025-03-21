from rest_framework import serializers
from app.models.cilindro import Cilindro

class CilindroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cilindro
        fields = '__all__'
