from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.usuario import Usuario


class UsuarioRepository(ABC):

    @abstractmethod
    def obtener_todos(self) -> List[Usuario]:
        pass

    @abstractmethod
    def crear(self, usuario: Usuario) -> Usuario:
        pass

    @abstractmethod
    def actualizar_por_id(
        self,
        usuario_id: str,
        usuario: Usuario
    ) -> Optional[Usuario]:
        pass