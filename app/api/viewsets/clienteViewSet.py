from django.forms import ValidationError
from rest_framework import viewsets, status
from app.models.cliente import Cliente
from rest_framework.response import Response
from app.api.serializers.clienteSerializer import ClienteSerializer, ClienteFlatSerializer
from rest_framework.permissions import IsAuthenticated
from app.api.permissions.custom_permissions import CustomAccessPermission
from app.api.permissions.authenticationPermissions import CsrfExemptSessionAuthentication
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.select_related('user').all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated, CustomAccessPermission]

    def get_serializer_class(self):
        if self.action in ['list', 'retrive']:
            return ClienteFlatSerializer
        return ClienteSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            print(serializer.validated_data)
            if User.objects.filter(email=serializer.validated_data.get('user').get('email')).exists():
                print("ya existe el user")
                raise Exception('Ya existe un usuario con ese email')


            Cliente = serializer.save()
            

            return Response({"message" : "Cliente creado correctamente"}, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            print(e)
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'error': f'{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, *args, **kwargs):
        try:
            
            instance = self.get_object()
            user = User.objects.get(id = instance.user_id)
            user.delete()
            instance.delete()

            return Response(
                {"message": f"Cliente con id {kwargs['pk']} eliminado"},
                status=status.HTTP_204_NO_CONTENT
            )
        except ValidationError as e:
            return Response({'error': str(e)}, status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error inesperado': f'Intenta again: {e}'}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def update(self, request, *args, **kwargs):
        try:

            instance = self.get_object(request.id)
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


            correo_nuevo = request.data.get("correo")
            username_nuevo = request.data.get("username")
            id_actual = request.data.get("id") or instance.id

            if correo_nuevo:
                correo_conflict = Cliente.objects.filter(user__email=correo_nuevo).exclude(id=id_actual).first()
                if correo_conflict:
                    return Response(
                        {"error": "Correo ya registrado"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            if username_nuevo:
                username_conflict = Cliente.objects.filter(user__username=username_nuevo).exclude(id=id_actual).first()
                if username_conflict:
                    return Response(
                        {"error": "EL nombre de usuario ya está en uso"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'error': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)