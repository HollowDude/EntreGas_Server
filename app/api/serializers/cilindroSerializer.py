from rest_framework import serializers
from app.models.cilindro import Cilindro

class CilindroSerializer(serializers.ModelSerializer):
    id   = serializers.CharField(read_only=True)
    fecha_de_llegada = serializers.SerializerMethodField()
    defectuoso = serializers.SerializerMethodField()
    lleno = serializers.SerializerMethodField()
    asignacion = serializers.CharField(read_only=True)

    class Meta:
        model = Cilindro
        fields = [
            'id',
            'fecha_llegada',
            'defectuoso',
            'lleno',
            'asignacion',
        ]

    def get_fecha_de_llegada(self, obj):
        return obj.fehca_llegada.strftime("%d/%m/%Y")  # si escribiste "fehca", ojo ahí también

    def get_defectuoso(self, obj):
        return "True" if obj.defectuoso else "False"

    def get_lleno(self, obj):
        return "True" if obj.lleno else "False"

