from django.forms import ValidationError
from rest_framework import viewsets, status
from app.models.cilindro import Cilindro
from rest_framework.response import Response
from app.api.serializers.cilindroSerializer import CilindroSerializer
from rest_framework.permissions import IsAuthenticated
from app.api.permissions.custom_permissions import CustomAccessPermission
from app.api.permissions.authenticationPermissions import CsrfExemptSessionAuthentication
from rest_framework.decorators import action
from django.db.models import Q


class CilindroViewSet(viewsets.ModelViewSet):
    queryset = Cilindro.objects.select_related('asign__user')
    authentication_classes = [CsrfExemptSessionAuthentication]
    serializer_class = CilindroSerializer
    permission_classes = [IsAuthenticated, CustomAccessPermission]


    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            print(serializer.validated_data)

            Cilindro = serializer.save()
            

            return Response(self.get_serializer(Cilindro).data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Un error inesperado a ocurrido {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, *args, **kwargs):
        try:
            
            instance = self.get_object()
            instance.delete()

            return Response(
                {"message": f"Cilindro con id {kwargs['pk']} eliminado"},
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

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Error inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
