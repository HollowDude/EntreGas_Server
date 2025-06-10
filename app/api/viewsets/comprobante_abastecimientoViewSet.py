from django.forms import ValidationError
from rest_framework import viewsets, status
from app.models.comprobante_abastecimiento import Comprobante_Abastecimiento
from rest_framework.response import Response
from app.api.serializers.comprobante_abastecimientoSerializer import Comprobante_AbastecimientoSerializer
from rest_framework.permissions import IsAuthenticated
from app.api.permissions.custom_permissions import CustomAccessPermission
from app.api.permissions.authenticationPermissions import CsrfExemptSessionAuthentication

class Comprobante_AbastecimientoViewSet(viewsets.ModelViewSet):
    queryset = Comprobante_Abastecimiento.objects.select_related('trabajador_recibio__user')
    serializer_class = Comprobante_AbastecimientoSerializer
    permission_classes = [IsAuthenticated, CustomAccessPermission]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            comprobante = serializer.save()

            return Response(
                self.get_serializer(comprobante).data,
                status=status.HTTP_201_CREATED
            )

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {'error': f'Un error inesperado ha ocurrido: {e}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )