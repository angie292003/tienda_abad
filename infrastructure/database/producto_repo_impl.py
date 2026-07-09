from typing import List

from bson import ObjectId

from domain.entities.productos import Producto
from domain.interfaces.productos_repo import ProductoRepository
from infrastructure.database.mongo_connection import db


class ProductoRepoImpl(ProductoRepository):

    def __init__(self):
        self.collection = db["producto"]

    def obtener_todos(self) -> List[Producto]:

        documentos = self.collection.find().sort("nombre", 1)

        productos = []

        for doc in documentos:
            proveedor_id = doc.get("proveedorId")

            productos.append(
                Producto(
                    id=str(doc.get("_id")),
                    nombre=doc.get("nombre", ""),
                    categoria=doc.get("categoria", ""),
                    marca=doc.get("marca", ""),
                    precio_compra=float(doc.get("precioCompra", 0)),
                    precio_venta=float(doc.get("precioVenta", 0)),
                    stock=int(doc.get("stock", 0)),
                    stock_minimo=int(doc.get("stockMinimo", 0)),
                    unidad_medida=doc.get("unidadMedida", ""),
                    estado=bool(doc.get("estado", True)),
                    proveedor_id=str(proveedor_id) if proveedor_id else ""
                )
            )

        return productos

    def crear(self, producto: Producto) -> Producto:

        data = {
            "nombre": producto.nombre,
            "categoria": producto.categoria,
            "marca": producto.marca,
            "precioCompra": producto.precio_compra,
            "precioVenta": producto.precio_venta,
            "stock": producto.stock,
            "stockMinimo": producto.stock_minimo,
            "unidadMedida": producto.unidad_medida,
            "estado": producto.estado,
            "proveedorId": ObjectId(producto.proveedor_id)
        }

        resultado = self.collection.insert_one(data)

        producto.id = str(resultado.inserted_id)

        return producto

    def eliminar_por_id(self, producto_id: str) -> bool:

        try:
            resultado = self.collection.delete_one({
                "_id": ObjectId(producto_id)
            })

            return resultado.deleted_count > 0

        except Exception:
            return False
        
    def actualizar_por_id(
        self,
        producto_id: str,
        producto: Producto
    ):

        try:
            object_id = ObjectId(producto_id)

            data = {
                "nombre": producto.nombre,
                "categoria": producto.categoria,
                "marca": producto.marca,
                "precioCompra": producto.precio_compra,
                "precioVenta": producto.precio_venta,
                "stock": producto.stock,
                "stockMinimo": producto.stock_minimo,
                "unidadMedida": producto.unidad_medida,
                "estado": producto.estado,
                "proveedorId": ObjectId(producto.proveedor_id)
            }

            resultado = self.collection.update_one(
                {"_id": object_id},
                {"$set": data}
            )

            if resultado.matched_count == 0:
                return None

            doc = self.collection.find_one({"_id": object_id})

            if not doc:
                return None

            proveedor_id = doc.get("proveedorId")

            return Producto(
                id=str(doc.get("_id")),
                nombre=doc.get("nombre", ""),
                categoria=doc.get("categoria", ""),
                marca=doc.get("marca", ""),
                precio_compra=float(doc.get("precioCompra", 0)),
                precio_venta=float(doc.get("precioVenta", 0)),
                stock=int(doc.get("stock", 0)),
                stock_minimo=int(doc.get("stockMinimo", 0)),
                unidad_medida=doc.get("unidadMedida", ""),
                estado=bool(doc.get("estado", True)),
                proveedor_id=str(proveedor_id) if proveedor_id else ""
            )

        except Exception:
            return None        