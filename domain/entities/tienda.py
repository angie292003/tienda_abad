from dataclasses import dataclass
from typing import Optional


@dataclass
class Tienda:
    nombre: str
    direccion: str
    categoria: str
    estado: str = "Activa"
    id: Optional[str] = None

    def to_dict(self):
        data = {
            "nombre": self.nombre,
            "direccion": self.direccion,
            "categoria": self.categoria,
            "estado": self.estado
        }

        if self.id:
            data["id"] = self.id

        return data