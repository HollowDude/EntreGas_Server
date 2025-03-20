from rest_framework import permissions

class IsJefeOrReadOnly(permissions.BasePermission):


    def has_permission(self, request, view):
        if request.user and request.user.is_superuser:
            return True
        
        if request.user and hasattr(request.user, 'trabajador'):
            return request.user.trabajador.puesto == "jefe de servicio" and request.method in permissions.SAFE_METHODS
        
        return False
