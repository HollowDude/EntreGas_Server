from django.forms import ValidationError
from rest_framework import viewsets, status
from app.models.reporte_devolucion import Reporte_Devolucion
from rest_framework.response import Response
from app.api.serializers.reporte_devolucionSerializer import Reporte_DevolucionSerializer
from rest_framework.permissions import IsAuthenticated
from app.api.permissions.custom_permissions import CustomAccessPermission
from app.api.permissions.authenticationPermissions import CsrfExemptSessionAuthentication
from app.models.cliente import Cliente
from app.models.cilindro import Cilindro
from django.shortcuts import get_object_or_404
from datetime import datetime, date


class Reporte_DevolucionViewSet(viewsets.ModelViewSet):
    queryset = Reporte_Devolucion.objects.select_related('cliente__user')
    serializer_class = Reporte_DevolucionSerializer
    permission_classes = [IsAuthenticated, CustomAccessPermission]

    """     def create(self, request, *args, **kwargs):
            try:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                validated_data = serializer.validated_data

                cliente = getattr(request.user, 'cliente', None)
                if cliente is None:
                    cliente_id = validated_data.get('cliente').get('user').get('username')
                    print("Prueba: ", validated_data.get('cliente') )
                    if not cliente_id:
                        raise ValidationError("Se requiere un cliente para el reporte")
                    cliente = get_object_or_404(Cliente, user__username=cliente_id)

                cilindro = get_object_or_404(Cilindro, asign=cliente)

                reporte = serializer.save(
                    cliente=cliente,
                    cilindro=cilindro,
                    defecto=validated_data.get('defecto'),
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
                ) """
        

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response({'error': 'Datos inválidos'}, status=status.HTTP_400_BAD_REQUEST)
        
        cliente = getattr(request.user, 'cliente', None)
        fecha_obj = date.today()
        if cliente is None:
            try:
                print("Prueba: Desde panel de administrador")
                cliente = Cliente.objects.get(user__username=request.data.get('cliente'))
                fecha_obj = datetime.strptime(request.data.get("fecha"), '%Y-%m-%d').date()
            except Cliente.DoesNotExist:
                return Response(
                    {'error': 'El cliente especificado no existe'},
                    status=404
                )

        try:
            cilindro= Cilindro.objects.get(asign=cliente)
        except Exception as e:
            return Response(
                {'error':'El cliente actual no tiene cilindros asignados'},
                status=404
            )        

        try:
            rd = Reporte_Devolucion(fecha=fecha_obj, cliente=cliente, cilindro=cilindro, defecto=request.data.get('defecto'))
            rd.save()
        except Exception as e:
            return Response(
                {'error' : f'{str(e)}'},
                status=400
            )
        
        return Response(
            {'message':"Reporte de devolucion creado"},
            status=201
        )