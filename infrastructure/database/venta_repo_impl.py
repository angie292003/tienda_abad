from datetime import datetime
from typing import List

from bson import ObjectId

from domain.interfaces.venta_repo import VentaRepository
from infrastructure.database.mongo_connection import db


class VentaRepoImpl(VentaRepository):

    def __init__(self):
        self.ventas_collection = db["ventas"]
        self.productos_collection = db["producto"]

    def obtener_todas(self) -> List[dict]:

        documentos = self.ventas_collection.find().sort("fecha", -1)

        ventas = []

        for doc in documentos:
            productos = []

            for item in doc.get("productos", []):
                productos.append({
                    "productoId": str(item.get("productoId")),
                    "nombre": item.get("nombre", ""),
                    "categoria": item.get("categoria", ""),
                    "marca": item.get("marca", ""),
                    "cantidad": item.get("cantidad", 0),
                    "precioUnitario": item.get("precioUnitario", 0),
                    "subtotal": item.get("subtotal", 0)
                })

            fecha = doc.get("fecha")

            if isinstance(fecha, datetime):
                fecha = fecha.strftime("%d/%m/%Y %H:%M:%S")

            ventas.append({
                "id": str(doc.get("_id")),
                "productos": productos,
                "metodoPago": doc.get("metodoPago", ""),
                "total": doc.get("total", 0),
                "usuario": doc.get("usuario", ""),
                "rol": doc.get("rol", ""),
                "estado": doc.get("estado", "Registrada"),
                "fecha": fecha
            })

        return ventas

    def crear(self, data: dict) -> dict:

        productos_request = data.get("productos") or []
        metodo_pago = data.get("metodoPago")
        usuario = data.get("usuario")
        rol = data.get("rol")

        productos_venta = []
        total = 0

        for item in productos_request:

            producto_id = item.get("productoId")
            cantidad = int(item.get("cantidad"))

            try:
                object_id = ObjectId(producto_id)
            except Exception:
                return {
                    "ok": False,
                    "message": "ID de producto inválido"
                }

            producto_doc = self.productos_collection.find_one({
                "_id": object_id
            })

            if not producto_doc:
                return {
                    "ok": False,
                    "message": "Producto no encontrado"
                }

            stock_actual = int(producto_doc.get("stock", 0))

            if stock_actual < cantidad:
                return {
                    "ok": False,
                    "message": f"Stock insuficiente para {producto_doc.get('nombre', '')}"
                }

            precio_unitario = float(producto_doc.get("precioVenta", 0))
            subtotal = precio_unitario * cantidad

            productos_venta.append({
                "productoId": object_id,
                "nombre": producto_doc.get("nombre", ""),
                "categoria": producto_doc.get("categoria", ""),
                "marca": producto_doc.get("marca", ""),
                "cantidad": cantidad,
                "precioUnitario": precio_unitario,
                "subtotal": subtotal
            })

            total += subtotal

        venta_doc = {
            "productos": productos_venta,
            "metodoPago": metodo_pago,
            "total": total,
            "usuario": usuario,
            "rol": rol,
            "estado": "Registrada",
            "fecha": datetime.now()
        }

        resultado = self.ventas_collection.insert_one(venta_doc)

        for item in productos_venta:
            self.productos_collection.update_one(
                {"_id": item["productoId"]},
                {"$inc": {"stock": -item["cantidad"]}}
            )

        return {
            "ok": True,
            "message": "Venta registrada correctamente",
            "ventaId": str(resultado.inserted_id),
            "total": total
        }