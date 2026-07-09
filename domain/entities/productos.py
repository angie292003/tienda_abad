from dataclasses import dataclass
from typing import Optional


@dataclass
class Producto:
    nombre: str
    categoria: str
    marca: str
    precio_compra: float
    precio_venta: float
    stock: int
    stock_minimo: int
    unidad_medida: str
    estado: bool
    proveedor_id: str
    id: Optional[str] = None

    def to_dict(self):
        data = {
            "nombre": self.nombre,
            "categoria": self.categoria,
            "marca": self.marca,
            "precioCompra": self.precio_compra,
            "precioVenta": self.precio_venta,
            "stock": self.stock,
            "stockMinimo": self.stock_minimo,
            "unidadMedida": self.unidad_medida,
            "estado": self.estado,
            "proveedorId": self.proveedor_id
        }

        if self.id:
            data["id"] = self.id

        return data