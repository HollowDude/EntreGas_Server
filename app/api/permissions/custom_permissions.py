from rest_framework import permissions
from django.contrib.auth.models import User

from app.models.cliente import Cliente

class CustomAccessPermission(permissions.BasePermission):
    """
    Define acceso según rol en models.Trabajador.puesto o models.Cliente:
    - Administradores (superuser o puesto='administrador'): acceso total.
    - Jefe de servicio: solo puede crear comprobantes (entrega, abastecimiento, devolución) y listar clientes y cilindros.
    - Clientes: solo pueden listar cilindros y editar su propio registro de cliente.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if user.is_superuser or (hasattr(user, 'trabajador') and user.trabajador.puesto == 'administrador'):
            return True

        if hasattr(user, 'trabajador'):
            if user.trabajador.puesto == 'jefe de servicio':
                if view.action == 'create' and view.basename in ['comprobante-entrega', 'comprobante-abastecimiento']:
                    return True
                if view.action == 'list' and view.basename in ['cliente', 'cilindro']:
                    return True
            
            if view.basename == 'reporte-devolucion' and view.action in ['list', 'retrieve']:
                return True
            return False

        if hasattr(user, 'cliente'):
            if view.basename == 'reporte-devolucion' and view.action == 'create':
                return True
            if view.basename == 'cilindro' and view.action == 'list':
                return True
            if view.basename == 'cliente' and view.action in ['retrieve', 'update', 'partial_update']:
                return True
            return False

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or (hasattr(user, 'trabajador') and user.trabajador.puesto == 'administrador'):
            return True

        if hasattr(user, 'trabajador'):
            return True

        if hasattr(user, 'cliente') and isinstance(obj, Cliente):
            return obj.pk == user.cliente.pk

        return False