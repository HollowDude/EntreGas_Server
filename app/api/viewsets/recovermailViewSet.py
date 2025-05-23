from datetime import timedelta
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework.permissions import AllowAny
from app.api.permissions.authenticationPermissions import CsrfExemptSessionAuthentication
from app.api.serializers.recovermailSerializer import PasswordResetRequestSerializer, PasswordResetConfirmSerializer

User = get_user_model()

class PasswordResetViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    http_method_names = ['post', 'get']

    @action(detail=False, methods=['post'])
    def request_reset(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'detail': 'No existe un usuario con este correo electrónico.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        refresh = RefreshToken.for_user(user)
        refresh.set_exp(lifetime=timedelta(hours=5))
        
        token = str(refresh.access_token)
        
        link = f"http://localhost:5173/new-password/{token}"

        send_mail(user.get_username, email, link)
        
        return Response(
            {'detail': 'Se ha enviado un enlace de recuperación a tu correo uci.',
             'token': token},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def validate_token(self, request, token=None):
        if not token:
            return Response(
                {'detail': 'Token no proporcionado.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            UntypedToken(token)
            
            
            return Response(
                {'detail': 'Token válido.'},
                status=status.HTTP_200_OK
            )
            
        except (TokenError):
            return Response(
                {'detail': 'Token inválido o expirado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def reset_password(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        
        try:
            decoded_token = UntypedToken(token)
            user_id = decoded_token['user_id']
        
            
            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()
            
            
            return Response(
                {'detail': 'Contraseña actualizada correctamente.'},
                status=status.HTTP_200_OK
            )
            
        except (TokenError, User.DoesNotExist):
            return Response(
                {'detail': 'Token inválido o expirado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

def send_mail(usuario, email, link):
    try:
        subject = 'Recuperación de contraseña'
        message = f'Hola {usuario},\n\nPara restablecer tu contraseña, haz click en el siguiente enlace:\n\n{link}\n\nEl enlace expirará en 5 horas.'
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
    except ():
        raise