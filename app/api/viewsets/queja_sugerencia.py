from django.forms import ValidationError
from rest_framework import viewsets, status
from app.models.queja_sugerencia import Queja_sugerencia
from rest_framework.response import Response
from app.api.serializers.queja_sugerenciaSerializer import Queja_sugerenciaSerializer
from rest_framework.permissions import IsAuthenticated
from app.api.permissions.custom_permissions import CustomAccessPermission
from datetime import date


class QuejaSugerenciaViewSet(viewsets.ModelViewSet):
    queryset = Queja_sugerencia.objects.select_related('cliente__user')
    serializer_class = Queja_sugerenciaSerializer
    permission_classes = [IsAuthenticated, CustomAccessPermission]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response({'error': 'Datos inválidos'}, status=status.HTTP_400_BAD_REQUEST)
        
        cliente = getattr(request.user, 'cliente', None)
        fecha_obj = date.today()
        if cliente is None:
            return Response(
                {'error': 'El cliente especificado no existe'},
                status=404
            )

        try:
            q = Queja_sugerencia(fecha=fecha_obj, cliente=cliente, mensaje=request.data.get('mensaje'))
            q.save()
        except Exception as e:
            return Response(
                {'error' : f'{str(e)}'},
                status=400
            )
        
        return Response(
            {'message':"Queja o sugerencia registrada correctamente"},
            status=201
        )