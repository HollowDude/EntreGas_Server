from django.forms import ValidationError
from rest_framework import viewsets, status
from app.models.reporte_devolucion import Reporte_Devolucion
from rest_framework.response import Response
from app.api.serializers.reporte_devolucionSerializer import Reporte_DevolucionSerializer
from rest_framework.permissions import IsAuthenticated
from app.api.permissions.custom_permissions import CustomAccessPermission

class Reporte_DevolucionViewSet(viewsets.ModelViewSet):
    queryset = Reporte_Devolucion.objects.select_related('cliente__user')
    serializer_class = Reporte_DevolucionSerializer
    permission_classes = [IsAuthenticated, CustomAccessPermission]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            cliente = request.user.cliente

            cilindro = get_object_or_404(Cilindro, asign=cliente)

            reporte = serializer.save(
                cliente=cliente,
                cilindro=cilindro,
                fecha=date.today()
            )

            return Response(
                self.get_serializer(reporte).data,
                status=status.HTTP_201_CREATED
            )

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {'error': f'Error inesperado: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )