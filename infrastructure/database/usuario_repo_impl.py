from typing import List, Optional

from bson import ObjectId

from domain.entities.usuario import Usuario
from domain.interfaces.usuario_repo import UsuarioRepository
from infrastructure.database.mongo_connection import db


class UsuarioLogin:
    """
    Esta clase es para que el login antiguo siga funcionando.
    Convierte el documento de MongoDB en un objeto con atributos.
    """

    def __init__(self, doc: dict):
        self.id = str(doc.get("_id"))
        self.email = doc.get("email", "")
        self.password_hash = doc.get("password", "")
        self.password = doc.get("password", "")
        self.rol = doc.get("rol", "cliente")
        self.estado = bool(doc.get("estado", True))
        self.nombre = doc.get("nombre", "")
        self.fecha_registro = doc.get("fechaRegistro", "")

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "rol": self.rol,
            "estado": self.estado,
            "nombre": self.nombre,
            "fechaRegistro": self.fecha_registro
        }


class UsuarioRepoImpl(UsuarioRepository):
    """
    Esta clase es para el módulo nuevo de administración de usuarios.
    Sirve para listar, crear y actualizar usuarios.
    """

    def __init__(self):
        self.collection = db["users"]

    def obtener_todos(self) -> List[Usuario]:

        documentos = self.collection.find().sort("nombre", 1)

        usuarios = []

        for doc in documentos:
            usuarios.append(
                Usuario(
                    id=str(doc.get("_id")),
                    nombre=doc.get("nombre", ""),
                    email=doc.get("email", ""),
                    rol=doc.get("rol", "cliente"),
                    estado=bool(doc.get("estado", True)),
                    fecha_registro=doc.get("fechaRegistro", "")
                )
            )

        return usuarios

    def crear(self, usuario: Usuario) -> Optional[Usuario]:

        existe = self.collection.find_one({
            "email": usuario.email
        })

        if existe:
            return None

        data = {
            "nombre": usuario.nombre,
            "email": usuario.email,
            "password": usuario.password,
            "rol": usuario.rol,
            "estado": usuario.estado,
            "fechaRegistro": usuario.fecha_registro
        }

        resultado = self.collection.insert_one(data)

        usuario.id = str(resultado.inserted_id)

        return usuario

    def actualizar_por_id(
        self,
        usuario_id: str,
        usuario: Usuario
    ) -> Optional[Usuario]:

        try:
            object_id = ObjectId(usuario_id)

            usuario_existente = self.collection.find_one({
                "_id": object_id
            })

            if not usuario_existente:
                return None

            correo_duplicado = self.collection.find_one({
                "email": usuario.email,
                "_id": {"$ne": object_id}
            })

            if correo_duplicado:
                return None

            data = {
                "nombre": usuario.nombre,
                "email": usuario.email,
                "rol": usuario.rol,
                "estado": usuario.estado,
                "fechaRegistro": usuario.fecha_registro
            }

            if usuario.password:
                data["password"] = usuario.password

            resultado = self.collection.update_one(
                {"_id": object_id},
                {"$set": data}
            )

            if resultado.matched_count == 0:
                return None

            doc = self.collection.find_one({
                "_id": object_id
            })

            return Usuario(
                id=str(doc.get("_id")),
                nombre=doc.get("nombre", ""),
                email=doc.get("email", ""),
                rol=doc.get("rol", "cliente"),
                estado=bool(doc.get("estado", True)),
                fecha_registro=doc.get("fechaRegistro", "")
            )

        except Exception:
            return None


class UsuarioRepositoryMongo:
    """
    Esta clase mantiene funcionando el login antiguo.
    El login espera usuario.password_hash, por eso devolvemos UsuarioLogin.
    """

    def __init__(self):
        self.collection = db["users"]

    def buscar_por_email(self, email: str):

        email = (email or "").strip().lower()

        usuario_doc = self.collection.find_one({
            "email": email
        })

        if not usuario_doc:
            return None

        return UsuarioLogin(usuario_doc)

    def buscar_por_correo(self, email: str):
        return self.buscar_por_email(email)

    def obtener_por_email(self, email: str):
        return self.buscar_por_email(email)