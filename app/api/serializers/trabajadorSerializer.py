from rest_framework import serializers
from django.contrib.auth.models import User
from app.models.trabajador import Trabajador

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password','first_name', 'last_name', 'email']
        extra_kwargs = {
        'password': {'write_only': True}
    }


    def validate_email(self, value):
        if not value.endswith("@uci.cu"):
            raise serializers.ValidationError("El correo debe pertenecer al dominio @uci.cu.")
        
        user_id = self.instance.id if self.instance else None
        if User.objects.filter(email=value).exclude(id=user_id).exists():
            raise serializers.ValidationError("Este correo ya está en uso por otro trabajador.")
        
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class TrabajadorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Trabajador
        fields = ['id', 'user', 'puesto']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()
        trabajador = Trabajador.objects.create(user=user, **validated_data)
        return trabajador
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            password = user_data.pop('password', None)
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            if password:
                user.set_password(password)
            user.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
