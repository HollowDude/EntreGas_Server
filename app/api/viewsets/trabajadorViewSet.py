from django.forms import ValidationError
from rest_framework import viewsets, status
from app.models.trabajador import Trabajador
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from app.api.serializers.trabajadorSerializer import TrabajadorSerializer, TrabajadorFlatSerializer
from app.api.permissions.custom_permissions import CustomAccessPermission
from app.api.permissions.authenticationPermissions import CsrfExemptSessionAuthentication

from django.contrib.auth.models import User

class TrabajadorViewSet(viewsets.ModelViewSet):
    queryset = Trabajador.objects.select_related('user').all()
    serializer_class = TrabajadorSerializer
    permission_classes = [IsAuthenticated, CustomAccessPermission]

    def get_serializer_class(self):
        if self.action in ['list', 'retrive']:
            return TrabajadorFlatSerializer
        return TrabajadorSerializer

    def create(self, request, *args, **kwargs):
        try:
            user_data = request.data.get('user', {})
            email = user_data.get('email')
            username = user_data.get('username')

            if email and User.objects.filter(email__iexact=email).exists():
                return Response(
                    {'error': 'Ya existe un usuario con ese correo.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if username and User.objects.filter(username__iexact=username).exists():
                return Response(
                    {'error': 'Ya existe un usuario con ese nombre de usuario.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            trabajador = serializer.save()
            trabajador.user.is_staff = True
            trabajador.user.save()

            return Response({"message" : "Se ha creado el trabajador satisfactoriamente"}, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Un error inesperado ha ocurrido: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, *args, **kwargs):
        try:
            
            instance = self.get_object()
            user = User.objects.get(id = instance.user_id)
            user.delete()
            instance.delete()

            return Response(
                {"message": f"Trabajador con id {kwargs['pk']} eliminado"},
                status=status.HTTP_204_NO_CONTENT
            )
        except ValidationError as e:
            return Response({'error': str(e)}, status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error inesperado': f'Intenta again: {e}'}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def update(self, request, *args, **kwargs):
        try:

            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)

            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except ValidationError as e:
            return Response({'error': str(e)}, status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error inesperado': f'Intenta again: {e}'}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            user_data = request.data.get("user", {})
            email_nuevo = request.data.get("correo")
            username_nuevo = request.data.get("username")
            user_actual_id = instance.user.id

            if email_nuevo:
                correo_conflict = Trabajador.objects.filter(user__email=email_nuevo).exclude(id=request.data.get('id')).first()
                if correo_conflict:
                    return Response(
                        {"error": "Ya existe un usuario con ese correo."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            if username_nuevo:
                username_conflict = Trabajador.objects.filter(user__username=username_nuevo).exclude(id=request.data.get('id')).first()
                if username_conflict:
                    return Response(
                        {"error": "Ya existe un usuario con ese nombre de usuario."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Error inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
