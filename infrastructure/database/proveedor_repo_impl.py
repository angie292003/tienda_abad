from typing import List

from bson import ObjectId

from domain.entities.proveedor import Proveedor
from domain.interfaces.proveedor_repo import ProveedorRepository
from infrastructure.database.mongo_connection import db


class ProveedorRepoImpl(ProveedorRepository):

    def __init__(self):
        self.collection = db["proveedores"]

    def obtener_todos(self) -> List[Proveedor]:

        documentos = self.collection.find().sort("nombre", 1)

        proveedores = []

        for doc in documentos:
            proveedores.append(
                Proveedor(
                    id=str(doc.get("_id")),
                    nombre=doc.get("nombre", ""),
                    telefono=doc.get("telefono", ""),
                    direccion=doc.get("direccion", ""),
                    correo=doc.get("correo", ""),
                    estado=bool(doc.get("estado", True))
                )
            )

        return proveedores

    def crear(self, proveedor: Proveedor) -> Proveedor:

        data = {
            "nombre": proveedor.nombre,
            "telefono": proveedor.telefono,
            "direccion": proveedor.direccion,
            "correo": proveedor.correo,
            "estado": proveedor.estado
        }

        resultado = self.collection.insert_one(data)

        proveedor.id = str(resultado.inserted_id)

        return proveedor

    def desactivar_por_id(self, proveedor_id: str) -> bool:

        try:
            resultado = self.collection.update_one(
                {"_id": ObjectId(proveedor_id)},
                {"$set": {"estado": False}}
            )

            return resultado.modified_count > 0

        except Exception:
            return False
    def actualizar_por_id(
        self,
        proveedor_id: str,
        proveedor: Proveedor
    ):

        try:
            object_id = ObjectId(proveedor_id)

            data = {
                "nombre": proveedor.nombre,
                "telefono": proveedor.telefono,
                "direccion": proveedor.direccion,
                "correo": proveedor.correo,
                "estado": proveedor.estado
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

            return Proveedor(
                id=str(doc.get("_id")),
                nombre=doc.get("nombre", ""),
                telefono=doc.get("telefono", ""),
                direccion=doc.get("direccion", ""),
                correo=doc.get("correo", ""),
                estado=bool(doc.get("estado", True))
            )

        except Exception:
            return None