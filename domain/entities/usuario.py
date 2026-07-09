from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:
    email: str
    rol: str
    estado: bool
    fecha_registro: str
    nombre: str
    password: Optional[str] = None
    id: Optional[str] = None

    def to_dict(self):
        data = {
            "email": self.email,
            "rol": self.rol,
            "estado": self.estado,
            "fechaRegistro": self.fecha_registro,
            "nombre": self.nombre
        }

        if self.id:
            data["id"] = self.id

        return data