from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.tienda import Tienda


class TiendaRepository(ABC):

    @abstractmethod
    def obtener_todas(self) -> List[Tienda]:
        pass

    @abstractmethod
    def crear(self, tienda: Tienda) -> Tienda:
        pass

    @abstractmethod
    def actualizar_por_id(
        self,
        tienda_id: str,
        tienda: Tienda
    ) -> Optional[Tienda]:
        pass