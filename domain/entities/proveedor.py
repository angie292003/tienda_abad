from dataclasses import dataclass
from typing import Optional


@dataclass
class Proveedor:
    nombre: str
    telefono: str
    direccion: str
    correo: str
    estado: bool = True
    id: Optional[str] = None

    def to_dict(self):
        data = {
            "nombre": self.nombre,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "correo": self.correo,
            "estado": self.estado
        }

        if self.id:
            data["id"] = self.id

        return data