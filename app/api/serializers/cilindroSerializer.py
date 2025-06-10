from rest_framework import serializers
from app.models.cilindro import Cilindro

class CilindroSerializer(serializers.ModelSerializer):
    id   = serializers.CharField()
    fecha_de_llegada = serializers.DateField()
    defectuoso = serializers.BooleanField()
    lleno = serializers.BooleanField()
    asignacion = serializers.CharField( source="asign.user.username" , read_only=True)

    class Meta:
        model = Cilindro
        fields = [
            'id',
            'fecha_de_llegada',
            'defectuoso',
            'lleno',
            'asignacion',
        ]
    
    def get_asignacion(self, obj):
        if obj.asign and obj.asign.user:
            return obj.asign.user.email
        return None

