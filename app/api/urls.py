from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.api.viewsets.trabajadorViewSet import TrabajadorViewSet
from app.api.viewsets.clienteViewSet import ClienteViewSet


router = DefaultRouter()

router.register('trabajador', TrabajadorViewSet)
router.register('cliente', ClienteViewSet)

urlpatterns = [
    path('', include(router.urls))
]