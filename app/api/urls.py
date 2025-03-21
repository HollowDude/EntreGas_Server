from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.api.viewsets.trabajadorViewSet import TrabajadorViewSet
from app.api.viewsets.clienteViewSet import ClienteViewSet
from app.api.viewsets.authentication import AuthViewSet
from app.api.viewsets.cilindroViewSet import CilindroViewSet


router = DefaultRouter()
#Modelos
router.register('trabajador', TrabajadorViewSet)
router.register('cliente', ClienteViewSet)
router.register('cilindro', CilindroViewSet)


#El auth
router.register(r'auth', AuthViewSet, basename='auth')



urlpatterns = [
    path('', include(router.urls))
]