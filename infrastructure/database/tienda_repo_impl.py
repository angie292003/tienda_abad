from typing import List

from bson import ObjectId

from domain.entities.tienda import Tienda
from domain.interfaces.tienda_repo import TiendaRepository
from infrastructure.database.mongo_connection import db


class TiendaRepoImpl(TiendaRepository):

    def __init__(self):
        self.collection = db["stores"]

    def obtener_todas(self) -> List[Tienda]:

        documentos = self.collection.find().sort("nombre", 1)

        tiendas = []

        for doc in documentos:
            tiendas.append(
                Tienda(
                    id=str(doc.get("_id")),
                    nombre=doc.get("nombre", ""),
                    direccion=doc.get("direccion", ""),
                    categoria=doc.get("categoria", ""),
                    estado=doc.get("estado", "Activa")
                )
            )

        return tiendas

    def crear(self, tienda: Tienda) -> Tienda:

        data = {
            "nombre": tienda.nombre,
            "direccion": tienda.direccion,
            "categoria": tienda.categoria,
            "estado": tienda.estado
        }

        resultado = self.collection.insert_one(data)

        tienda.id = str(resultado.inserted_id)

        return tienda

    def actualizar_por_id(
        self,
        tienda_id: str,
        tienda: Tienda
    ):

        try:
            object_id = ObjectId(tienda_id)

            data = {
                "nombre": tienda.nombre,
                "direccion": tienda.direccion,
                "categoria": tienda.categoria,
                "estado": tienda.estado
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

            return Tienda(
                id=str(doc.get("_id")),
                nombre=doc.get("nombre", ""),
                direccion=doc.get("direccion", ""),
                categoria=doc.get("categoria", ""),
                estado=doc.get("estado", "Activa")
            )

        except Exception:
            return None