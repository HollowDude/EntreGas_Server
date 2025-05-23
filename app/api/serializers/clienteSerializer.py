from datetime import date
from wsgiref import validate
from rest_framework import serializers
from django.contrib.auth.models import User
from app.models.cliente import Cliente

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email']

    def validate_email(self, value):
        if not value.endswith("@uci.cu"):
            raise serializers.ValidationError("El correo debe pertenecer al dominio @uci.cu.")
        
        user_id = self.instance.id if self.instance else None
        if User.objects.filter(email=value).exclude(id=user_id).exists():
            raise serializers.ValidationError("Este correo ya está en uso por otro cliente.")
        
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pp('password', None)
        user = User(**validated_data)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class ClienteSerializer(serializers.ModelSerializer):
    username   = serializers.CharField(source='user.username')
    contraseña   = serializers.CharField(write_only=True, source='user.password')
    nombre = serializers.CharField(source='user.first_name', required=False)
    correo      = serializers.EmailField(source='user.email')

    class Meta:
        model = Cliente
        fields = [
            'id',
            # campos de User, todos en el primer nivel
            'username', 'contraseña', 'nombre', 'correo',
            # campos propios de Cliente
            'direccion', 'tipo', 'fecha_UT'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()
        cliente = Cliente.objects.create(user=user, **validated_data)
        return cliente

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

    def validate_fecha_UT(self, value):
        if value >= date.today():
            raise serializers.ValidationError("La fecha de ultima T no puede ser superior a hoy")
        return value

class ClienteFlatSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    tipo = serializers.CharField(source='get_tipo_display')
    direccion = serializers.CharField()
    fecha_UT = serializers.DateField()
    fecha_PC = serializers.DateField()
    username   = serializers.CharField(source='user.username')
    nombre = serializers.CharField(source='user.first_name')
    correo      = serializers.EmailField(source='user.email')

    class Meta:
        model = Cliente
        fields = [
            'id',
            'tipo',
            'direccion',
            'fecha_UT',
            'fecha_PC',
            'username',
            'nombre',
            'correo',
        ]