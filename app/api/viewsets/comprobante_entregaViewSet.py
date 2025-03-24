from django.forms import ValidationError
from rest_framework import viewsets, status
from app.models.comprobante_entrega import Comprobante_Entrega
from rest_framework.response import Response
from app.api.serializers.comprobante_entregaSerializer import Comprobante_EntregaSerializer
from rest_framework.permissions import IsAuthenticated
from app.api.permissions.trabajadorPermissions import IsJefeOrReadOnly

class Comprobante_EntregaViewSet(viewsets.ModelViewSet):
    queryset = Comprobante_Entrega.objects.all()
    serializer_class = Comprobante_EntregaSerializer
    permission_classes = [IsAuthenticated, IsJefeOrReadOnly]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            Comprobante_Entrega = serializer.save()
            

            return Response(self.get_serializer(Comprobante_Entrega).data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Un error inesperado a ocurrido {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, *args, **kwargs):
        try:
            
            instance = self.get_object()
            instance.delete()

            return Response(
                {"message": f"Comprobante Entrega con id {kwargs['pk']} eliminado"},
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
    
