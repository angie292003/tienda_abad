from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.productos import Producto


class ProductoRepository(ABC):

    @abstractmethod
    def obtener_todos(self) -> List[Producto]:
        pass

    @abstractmethod
    def crear(self, producto: Producto) -> Producto:
        pass

    @abstractmethod
    def actualizar_por_id(
        self,
        producto_id: str,
        producto: Producto
    ) -> Optional[Producto]:
        pass

    @abstractmethod
    def eliminar_por_id(self, producto_id: str) -> bool:
        pass