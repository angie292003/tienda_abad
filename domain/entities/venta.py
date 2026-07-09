from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Venta:
    productos: List[dict]
    metodo_pago: str
    total: float
    usuario: str
    rol: str
    estado: str
    fecha: str
    id: Optional[str] = None

    def to_dict(self):
        data = {
            "productos": self.productos,
            "metodoPago": self.metodo_pago,
            "total": self.total,
            "usuario": self.usuario,
            "rol": self.rol,
            "estado": self.estado,
            "fecha": self.fecha
        }

        if self.id:
            data["id"] = self.id

        return data