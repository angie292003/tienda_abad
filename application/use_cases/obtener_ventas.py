from domain.interfaces.venta_repo import VentaRepository


def obtener_ventas(repo: VentaRepository):
    return repo.obtener_todas()