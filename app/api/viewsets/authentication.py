from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from app.api.permissions.authenticationPermissions import CsrfExemptSessionAuthentication
from ...models.trabajador import Trabajador
from ...models.cliente import Cliente


class AuthViewSet(viewsets.ViewSet):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        correo = request.data.get('correo')
        password = request.data.get('password')
        remember = request.data.get('recordar', False)

        user_qs = User.objects.filter(email=correo)
        if not user_qs.exists():
            return Response({'detail': 'Credenciales inválidas (correo)'},
                            status=status.HTTP_401_UNAUTHORIZED)
        user_obj = user_qs.first()

        user = authenticate(request, username=user_obj.username, password=password)
        if user is None:
            return Response({'detail': 'Credenciales inválidas (password)'},
                            status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        if not remember:
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(30 * 24 * 60 * 60)

        payload = {
            'detail': 'Autenticado correctamente',
            'user': user.username
        }

        try:
            trabajador = Trabajador.objects.get(user=user)
            payload.update({
                'tipo_usuario': 'trabajador',
                'puesto': trabajador.puesto
            })
            return Response(payload, status=status.HTTP_200_OK)
        except Trabajador.DoesNotExist:
            pass

        try:
            cliente = Cliente.objects.get(user=user)
            payload.update({
                'tipo_usuario': 'cliente',
                'tipo_cliente': cliente.tipo
            })
            return Response(payload, status=status.HTTP_200_OK)
        except Cliente.DoesNotExist:
            pass

        return Response(payload, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        logout(request)
        return Response({'detail': 'Desconectado correctamente'},
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def check(self, request):
        if not request.user.is_authenticated:
            return Response({'authenticated': False},
                            status=status.HTTP_200_OK)

        user = request.user
        if user.is_superuser:
            tipo = 'administrador'
        else:
            try:
                Trabajador.objects.get(user=user)
                tipo = 'trabajador'
            except Trabajador.DoesNotExist:
                try:
                    Cliente.objects.get(user=user)
                    tipo = 'cliente'
                except Cliente.DoesNotExist:
                    tipo = None

        return Response({
            'authenticated': True,
            'user': user.username,
            'tipo_user': tipo
        }, status=status.HTTP_200_OK)
