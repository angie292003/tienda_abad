from domain.entities.proveedor import Proveedor
from domain.interfaces.proveedor_repo import ProveedorRepository


def normalizar_estado(valor):

    if isinstance(valor, bool):
        return valor

    if isinstance(valor, str):
        return valor.lower() == "true"

    return True


def actualizar_proveedor(
    proveedor_id: str,
    data: dict,
    repo: ProveedorRepository
):

    nombre = (data.get("nombre") or "").strip()
    telefono = (data.get("telefono") or "").strip()
    direccion = (data.get("direccion") or "").strip()
    correo = (data.get("correo") or "").strip()
    estado = normalizar_estado(data.get("estado", True))

    if not proveedor_id:
        return {
            "ok": False,
            "message": "ID del proveedor inválido"
        }

    if not nombre:
        return {
            "ok": False,
            "message": "El nombre del proveedor es obligatorio"
        }

    if not telefono:
        return {
            "ok": False,
            "message": "El teléfono es obligatorio"
        }

    if not direccion:
        return {
            "ok": False,
            "message": "La dirección es obligatoria"
        }

    if not correo:
        return {
            "ok": False,
            "message": "El correo es obligatorio"
        }

    if "@" not in correo:
        return {
            "ok": False,
            "message": "El correo no tiene un formato válido"
        }

    proveedor = Proveedor(
        id=proveedor_id,
        nombre=nombre,
        telefono=telefono,
        direccion=direccion,
        correo=correo,
        estado=estado
    )

    proveedor_actualizado = repo.actualizar_por_id(
        proveedor_id,
        proveedor
    )

    if not proveedor_actualizado:
        return {
            "ok": False,
            "message": "No se pudo actualizar el proveedor"
        }

    return {
        "ok": True,
        "message": "Proveedor actualizado correctamente",
        "proveedor": proveedor_actualizado.to_dict()
    }