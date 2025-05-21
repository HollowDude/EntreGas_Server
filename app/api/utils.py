from datetime import date
from dateutil.relativedelta import relativedelta
from django.forms import ValidationError

from app.models.cliente import Cliente
from app.models.cilindro import Cilindro


def calcular_fecha_proximo_cilindro(tipo: str) -> date:
    """
    Para clientes normales: hoy + 2 meses.
    Para clientes especiales: hoy + 1 mes.
    """
    if tipo == "normal":
        return date.today() + relativedelta(months=2)
    return date.today() + relativedelta(months=1)


def crear_cilindros_abastecimiento(fecha: date, cantidad: int) -> None:
    """
    Crea 'cantidad' cilindros con valores por defecto:
    - fehca_llegada = fecha
    - defectuoso = False
    - lleno = True
    - asign = None
    """
    cilindros = [
        Cilindro(
            fehca_llegada=fecha,
            defectuoso=False,
            lleno=True,
            asign=None
        )
        for _ in range(cantidad)
    ]
    Cilindro.objects.bulk_create(cilindros)


def procesar_entrega(comprobante) -> None:
    """
    Valida disponibilidad de cilindros:
    - Busca el primer cilindro sin asignar, lleno y no defectuoso.
    - Asigna ese cilindro a comprobante.cilindroE.
    - Toma el cilindro existente (asignado al cliente) como comprobante.cilindroS.
    - Actualiza campos 'asign' y 'lleno' en los cilindros involucrados.
    """
    cliente = comprobante.cliente
    cilindro_nuevo = (
        Cilindro.objects.filter(asign__isnull=True, lleno=True, defectuoso=False).first()
    )
    if not cilindro_nuevo:
        raise ValidationError("No hay cilindros disponibles para asignar.")

    cilindro_antiguo = (Cilindro.objects.filter(asign=cliente).first()
    )

    comprobante.cilindroE = cilindro_nuevo
    comprobante.cilindroS = cilindro_antiguo
    comprobante.save(update_fields=['cilindroE', 'cilindroS'])

    cilindro_nuevo.asign = cliente
    cilindro_nuevo.save(update_fields=['asign'])

    if cilindro_antiguo:
        cilindro_antiguo.asign = None
        cilindro_antiguo.lleno = False
        cilindro_antiguo.save(update_fields=['asign', 'lleno'])