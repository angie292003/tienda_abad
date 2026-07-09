from abc import ABC, abstractmethod
from typing import List


class VentaRepository(ABC):

    @abstractmethod
    def obtener_todas(self) -> List[dict]:
        pass

    @abstractmethod
    def crear(self, data: dict) -> dict:
        pass