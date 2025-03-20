from rest_framework import serializers
from django.contrib.auth.models import User
from app.models.trabajador import Trabajador

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

class TrabajadorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Trabajador
        fields = ['id', 'user', 'puesto']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        trabajador = Trabajador.objects.create(user=user, **validated_data)
        return trabajador
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
