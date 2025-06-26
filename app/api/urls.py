from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.api.viewsets.trabajadorViewSet import TrabajadorViewSet
from app.api.viewsets.clienteViewSet import ClienteViewSet
from app.api.viewsets.authentication import AuthViewSet
from app.api.viewsets.cilindroViewSet import CilindroViewSet
from app.api.viewsets.comprobante_abastecimientoViewSet import Comprobante_AbastecimientoViewSet
from app.api.viewsets.comprobante_entregaViewSet import Comprobante_EntregaViewSet
from app.api.viewsets.reporte_devolucionViewSet import Reporte_DevolucionViewSet
from app.api.viewsets.recovermailViewSet import PasswordResetViewSet
from app.api.viewsets.queja_sugerencia import QuejaSugerenciaViewSet


router = DefaultRouter()

#Modelos
router.register('trabajador', TrabajadorViewSet)
router.register('cliente', ClienteViewSet)
router.register('cilindro', CilindroViewSet)
router.register('comprobante_abastecimiento', Comprobante_AbastecimientoViewSet)
router.register('comprobante_entrega', Comprobante_EntregaViewSet)
router.register('reporte_devolucion', Reporte_DevolucionViewSet)
router.register('queja_sugerencia', QuejaSugerenciaViewSet)


#El auth
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'password-reset', PasswordResetViewSet, basename='password-reset')



urlpatterns = [
    path('password-reset/validate-token/<str:token>/', 
         PasswordResetViewSet.as_view({'get': 'validate_token'}), 
         name='validate-token'),
] + router.urls