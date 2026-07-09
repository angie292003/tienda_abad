from domain.entities.proveedor import Proveedor
from domain.interfaces.proveedor_repo import ProveedorRepository


def crear_proveedor(data: dict, repo: ProveedorRepository):

    nombre = (data.get("nombre") or "").strip()
    telefono = (data.get("telefono") or "").strip()
    direccion = (data.get("direccion") or "").strip()
    correo = (data.get("correo") or "").strip()
    estado = data.get("estado", True)

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
        nombre=nombre,
        telefono=telefono,
        direccion=direccion,
        correo=correo,
        estado=bool(estado)
    )

    proveedor_creado = repo.crear(proveedor)

    return {
        "ok": True,
        "message": "Proveedor registrado correctamente",
        "proveedor": proveedor_creado.to_dict()
    }