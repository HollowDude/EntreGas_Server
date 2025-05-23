from datetime import date
from django.forms import ValidationError
from rest_framework import viewsets, status
from app.models.comprobante_entrega import Comprobante_Entrega, Cliente
from rest_framework.response import Response
from app.api.serializers.comprobante_entregaSerializer import Comprobante_EntregaSerializer
from rest_framework.permissions import IsAuthenticated
from app.api.permissions.custom_permissions import CustomAccessPermission
from app.api.utils import procesar_entrega, calcular_fecha_proximo_cilindro
from app.api.permissions.authenticationPermissions import CsrfExemptSessionAuthentication


class Comprobante_EntregaViewSet(viewsets.ModelViewSet):
    queryset = Comprobante_Entrega.objects.select_related('cliente__user')
    serializer_class = Comprobante_EntregaSerializer
    permission_classes = [IsAuthenticated, CustomAccessPermission]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            comprobante = serializer.save()

            try:
                procesar_entrega(comprobante)
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            direccion = comprobante.cliente.direccion
            clientes_dir = Cliente.objects.filter(direccion=direccion)

            clientes_dir.update(fecha_UT=comprobante.fecha)


            fecha_norm = calcular_fecha_proximo_cilindro('normal')
            clientes_dir.filter(tipo='normal').update(fecha_PC=fecha_norm)
            fecha_esp = calcular_fecha_proximo_cilindro('especial')
            clientes_dir.filter(tipo='especial').update(fecha_PC=fecha_esp)

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
    
