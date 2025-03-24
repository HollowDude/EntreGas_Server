from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.api.viewsets.trabajadorViewSet import TrabajadorViewSet
from app.api.viewsets.clienteViewSet import ClienteViewSet
from app.api.viewsets.authentication import AuthViewSet
from app.api.viewsets.cilindroViewSet import CilindroViewSet
from app.api.viewsets.comprobante_abastecimientoViewSet import Comprobante_AbastecimientoViewSet
from app.api.viewsets.comprobante_entregaViewSet import Comprobante_EntregaViewSet
from app.api.viewsets.reporte_devolucionViewSet import Reporte_DevolucionViewSet


router = DefaultRouter()

#Modelos
router.register('trabajador', TrabajadorViewSet)
router.register('cliente', ClienteViewSet)
router.register('cilindro', CilindroViewSet)
router.register('comprobante_abastecimiento', Comprobante_AbastecimientoViewSet)
router.register('comprobante_entrega', Comprobante_EntregaViewSet)
router.register('reporte_devolucion', Reporte_DevolucionViewSet)


#El auth
router.register(r'auth', AuthViewSet, basename='auth')



urlpatterns = [
    path('', include(router.urls))
]