from datetime import date
from xmlrpc import client
from django.forms import ValidationError
from rest_framework import viewsets, status
from app.models.comprobante_entrega import Comprobante_Entrega
from app.models.cilindro import Cilindro
from app.models.cliente import Cliente
from rest_framework.response import Response
from app.api.serializers.comprobante_entregaSerializer import Comprobante_EntregaSerializer
from rest_framework.permissions import IsAuthenticated
from app.api.permissions.custom_permissions import CustomAccessPermission
from app.api.utils import procesar_entrega, calcular_fecha_proximo_cilindro, verificar_disponibilidad
from app.api.permissions.authenticationPermissions import CsrfExemptSessionAuthentication
from rest_framework.decorators import action 
from datetime import datetime, date
from rest_framework.permissions import AllowAny

from django.db import transaction


class Comprobante_EntregaViewSet(viewsets.ModelViewSet):
    queryset = Comprobante_Entrega.objects.select_related('cliente__user')
    serializer_class = Comprobante_EntregaSerializer
    permission_classes = [IsAuthenticated, CustomAccessPermission]


    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def solicitar(self, request, *args, **kwargs):
        if verificar_disponibilidad():
            return Response(
                {
                    'message' : "Hay cilindros disponibles, vaya cuando quiera"
                },
                status=status.HTTP_200_OK
            )
        return Response(
                {
                    'message' : "No hay cilindros disponibles actualmente"
                },
                status=status.HTTP_200_OK
            )


    """ def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
           
            print(request.data.get("fecha"))
            fecha_obj = datetime.strptime(request.data.get("fecha"), '%Y-%m-%d').date()
            if fecha_obj > date.today():
                raise Exception ("La fecha debe ser de hoy o antes")

            comprobante = serializer.save()

            try:
                procesar_entrega(comprobante)
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            direccion = comprobante.cliente.direccion
            clientes_dir = Cliente.objects.filter(direccion=direccion)

            clientes_dir.update(fecha_UT=comprobante.fecha)


            fecha_norm = calcular_fecha_proximo_cilindro('Normal', comprobante.fecha)
            fecha_esp = calcular_fecha_proximo_cilindro('Especial', comprobante.fecha)

            print(fecha_esp, fecha_norm)

            clientes_dir.filter(tipo='Normal').update(fecha_PC=fecha_norm)
            clientes_dir.filter(tipo='Especial').update(fecha_PC=fecha_esp)

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
     """
    
    
    def create(self, request, *args, **kwargs):
            
            try:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
            except ValidationError:
                return Response({'error': 'Datos inválidos'}, status=status.HTTP_400_BAD_REQUEST)

            client = Cliente.objects.get(user__username=request.data.get('cliente'))
            if not client:
                return Response(
                    {'error':'El cliente especificado no existe'},
                    status=404
                )

            cilindroE = Cilindro.objects.filter(asign__isnull=True, defectuoso=False).first()
            if not cilindroE:
                return Response(
                    {'message':'No hay cilindros disponibles para asignar'},
                    status=200
                )
            
            try:
                cilindroS = Cilindro.objects.get(asign=client)
            except Cilindro.DoesNotExist:
                cilindroS = None 


            entrega = Comprobante_Entrega(fecha=request.data.get('fecha'), cliente=client, cilindroE=cilindroE, cilindroS=cilindroS)

            try:
                with transaction.atomic():
                    entrega.save()
                    fecha_obj = datetime.strptime(request.data.get("fecha"), '%Y-%m-%d').date()
                    nextDate = calcular_fecha_proximo_cilindro(client.tipo, fecha_obj)
                    Cliente.objects.filter(direccion=client.direccion).update(fecha_UT=fecha_obj, fecha_PC=nextDate)
                    cilindroE.asign = client
                    cilindroE.save()
                    if cilindroS:
                        cilindroS.lleno = False
                        cilindroS.asign = None
                        cilindroS.save()
            except Exception as e:
                return Response(
                    {'error': f'{str(e)}'},
                    status=500
                )
            
            return Response(
                {'message':"Entrega exitosa"},
                status=200
            )



