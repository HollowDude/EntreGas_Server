from datetime import date
from rest_framework import serializers
from django.contrib.auth.models import User
from app.models.cliente import Cliente

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

    def validate_email(self, value):
        if not value.endswith("@uci.cu"):
            raise serializers.ValidationError("El correo debe pertenecer al dominio @uci.cu.")
        
        user_id = self.instance.id if self.instance else None
        if User.objects.filter(email=value).exclude(id=user_id).exists():
            raise serializers.ValidationError("Este correo ya está en uso por otro trabajador.")
        
        return value

class ClienteSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Cliente
        fields = ['user', 'id', 'direccion', 'tipo', 'fecha_UT', 'fecha_PC']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            cliente = Cliente.objects.create(user=user, **validated_data)
            return cliente

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def validate_fecha_UT(self, value):
        if value >= date.today():
            raise serializers.ValidationError("La fecha de ultima T no puede ser superior a hoy")
        return value