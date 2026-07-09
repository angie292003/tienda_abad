from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.proveedor import Proveedor


class ProveedorRepository(ABC):

    @abstractmethod
    def obtener_todos(self) -> List[Proveedor]:
        pass

    @abstractmethod
    def crear(self, proveedor: Proveedor) -> Proveedor:
        pass

    @abstractmethod
    def actualizar_por_id(
        self,
        proveedor_id: str,
        proveedor: Proveedor
    ) -> Optional[Proveedor]:
        pass

    @abstractmethod
    def desactivar_por_id(self, proveedor_id: str) -> bool:
        pass