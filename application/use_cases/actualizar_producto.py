from domain.entities.productos import Producto
from domain.interfaces.productos_repo import ProductoRepository


def normalizar_estado(valor):

    if isinstance(valor, bool):
        return valor

    if isinstance(valor, str):
        return valor.lower() == "true"

    return True


def actualizar_producto(producto_id: str, data: dict, repo: ProductoRepository):

    nombre = (data.get("nombre") or "").strip()
    categoria = (data.get("categoria") or "").strip()
    marca = (data.get("marca") or "").strip()
    unidad_medida = (data.get("unidadMedida") or "").strip()
    proveedor_id = (data.get("proveedorId") or "").strip()

    estado = normalizar_estado(data.get("estado", True))

    try:
        precio_compra = float(data.get("precioCompra"))
        precio_venta = float(data.get("precioVenta"))
        stock = int(data.get("stock"))
        stock_minimo = int(data.get("stockMinimo"))
    except (TypeError, ValueError):
        return {
            "ok": False,
            "message": "Precio, stock o stock mínimo inválido"
        }

    if not producto_id:
        return {
            "ok": False,
            "message": "ID del producto inválido"
        }

    if not nombre:
        return {
            "ok": False,
            "message": "El nombre es obligatorio"
        }

    if not categoria:
        return {
            "ok": False,
            "message": "La categoría es obligatoria"
        }

    if not marca:
        return {
            "ok": False,
            "message": "La marca es obligatoria"
        }

    if not unidad_medida:
        return {
            "ok": False,
            "message": "La unidad de medida es obligatoria"
        }

    if not proveedor_id:
        return {
            "ok": False,
            "message": "El proveedor es obligatorio"
        }

    if precio_compra <= 0:
        return {
            "ok": False,
            "message": "El precio de compra debe ser mayor a 0"
        }

    if precio_venta <= 0:
        return {
            "ok": False,
            "message": "El precio de venta debe ser mayor a 0"
        }

    if precio_venta < precio_compra:
        return {
            "ok": False,
            "message": "El precio de venta no puede ser menor al precio de compra"
        }

    if stock < 0:
        return {
            "ok": False,
            "message": "El stock no puede ser negativo"
        }

    if stock_minimo < 0:
        return {
            "ok": False,
            "message": "El stock mínimo no puede ser negativo"
        }

    # Regla automática:
    # Si el stock queda en 0, el producto pasa a inactivo.
    if stock == 0:
        estado = False

    producto = Producto(
        nombre=nombre,
        categoria=categoria,
        marca=marca,
        precio_compra=precio_compra,
        precio_venta=precio_venta,
        stock=stock,
        stock_minimo=stock_minimo,
        unidad_medida=unidad_medida,
        estado=estado,
        proveedor_id=proveedor_id,
        id=producto_id
    )

    producto_actualizado = repo.actualizar_por_id(producto_id, producto)

    if not producto_actualizado:
        return {
            "ok": False,
            "message": "No se pudo actualizar el producto"
        }

    return {
        "ok": True,
        "message": "Producto actualizado correctamente",
        "producto": producto_actualizado.to_dict()
    }