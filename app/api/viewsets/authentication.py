from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from ...models.trabajador import Trabajador
from ...models.cliente import Cliente



class AuthViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        recordar = request.data.get('recordar', False)
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)

            if recordar:
                request.session.set_expiry(30*24*60*60) #30 dias
            else:
                request.session.set_expiry(None)

            try:
                trabajador = Trabajador.objects.get(user=user)
                return Response({
                    'message': 'Inicio de sesión exitoso',
                    'tipo_usuario': 'trabajador',
                    'puesto': trabajador.puesto,
                    'username': user.username
                }, status=status.HTTP_200_OK)
            except Trabajador.DoesNotExist:
                pass

            try:
                cliente = Cliente.objects.get(user=user)
                return Response({
                    'message': 'Inicio de sesión exitoso',
                    'tipo_usuario': 'cliente',
                    'tipo_cliente': cliente.tipo,
                    'username': user.username
                }, status=status.HTTP_200_OK)
            except Cliente.DoesNotExist:
                pass

            return Response({'message': 'Inicio de sesión exitoso'}, status=status.HTTP_200_OK)
        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        logout(request)
        return Response({'message': 'Sesión cerrada'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def check_auth(self, request):
        return Response({'username': request.user.username})