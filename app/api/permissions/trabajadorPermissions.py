from rest_framework import permissions

class IsJefeOrReadOnly(permissions.BasePermission):


    def has_permission(self, request, view):
        # Acceso de lectura para cualquier usuario autenticado
        #Esto va  avariar claro
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Escritura solo para superusuarios o jefes de servicio
        if request.user.is_superuser:
            return True
        
        if hasattr(request.user, 'trabajador'):
            return request.user.trabajador.puesto == "Jefe de Servicio"
        
        return False