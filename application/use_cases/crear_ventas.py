from domain.interfaces.venta_repo import VentaRepository


def crear_venta(data: dict, repo: VentaRepository):

    productos = data.get("productos") or []
    metodo_pago = (data.get("metodoPago") or "").strip()

    if not productos:
        return {
            "ok": False,
            "message": "Debe agregar al menos un producto a la venta"
        }

    if not metodo_pago:
        return {
            "ok": False,
            "message": "Debe seleccionar un método de pago"
        }

    metodos_validos = ["Efectivo", "Yape", "Tarjeta"]

    if metodo_pago not in metodos_validos:
        return {
            "ok": False,
            "message": "Método de pago inválido"
        }

    for item in productos:
        producto_id = item.get("productoId")
        cantidad = item.get("cantidad")

        if not producto_id:
            return {
                "ok": False,
                "message": "Producto inválido"
            }

        try:
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            return {
                "ok": False,
                "message": "Cantidad inválida"
            }

        if cantidad <= 0:
            return {
                "ok": False,
                "message": "La cantidad debe ser mayor a 0"
            }

    return repo.crear(data)