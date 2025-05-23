from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from ...models.trabajador import Trabajador
from ...models.cliente import Cliente


class AuthViewSet(viewsets.ViewSet):
    """
    Habla claro: con JWT no hay que llorar por CSRF ni sesiones eternas.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        correo = request.data.get('correo')
        password = request.data.get('password')

        if not correo or not password:
            return Response(
                {'detail': 'Email y contraseña son obligatorios.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email__iexact=correo)
        except User.DoesNotExist:
            return Response({'detail': 'Credenciales inválidas (email)'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({'detail': 'Credenciales inválidas (password)'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generar tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        payload = {
            'access': access_token,
            'refresh': refresh_token,
            'user': user.username,
        }

        # Añadir info de perfil
        try:
            trab = Trabajador.objects.get(user=user)
            payload.update({
                'tipo_usuario': 'trabajador',
                'puesto': trab.puesto
            })
        except Trabajador.DoesNotExist:
            try:
                cli = Cliente.objects.get(user=user)
                payload.update({
                    'tipo_usuario': 'cliente',
                    'tipo_cliente': cli.tipo
                })
            except Cliente.DoesNotExist:
                payload['tipo_usuario'] = 'desconocido'

        return Response(payload, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def refresh(self, request):
        """
        Recibe {"refresh": "<token>"} y devuelve nuevo access.
        """
        token = request.data.get('refresh')
        if not token:
            return Response({'detail': 'Token de refresh es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            refresh = RefreshToken(token)
            new_access = str(refresh.access_token)
            return Response({'access': new_access}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': 'Token inválido o expirado.'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """
        Lista negra el refresh token para expulsarlo del coro de la vida.
        """
        token = request.data.get('refresh')
        if not token:
            return Response({'detail': 'Refresh token requerido para logout.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token_obj = RefreshToken(token)
            # Blacklist all outstanding tokens of this user, si lo deseas:
            for t in OutstandingToken.objects.filter(user=token_obj.user):
                BlacklistedToken.objects.get_or_create(token=t)
            return Response({'detail': 'Desconectado correctamente.'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'detail': 'Token inválido o expirado.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def check(self, request):
        """
        Con JWT no hay sesión, pero puedes validar el access:
        Debes incluirlo en Authorization: Bearer <access>.
        """
        user = request.user
        if not user or not user.is_authenticated:
            return Response({'authenticated': False}, status=status.HTTP_200_OK)

        # Determinar rol
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
