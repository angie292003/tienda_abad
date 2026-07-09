from domain.entities.tienda import Tienda
from domain.interfaces.tienda_repo import TiendaRepository


def crear_tienda(data: dict, repo: TiendaRepository):

    nombre = (data.get("nombre") or "").strip()
    direccion = (data.get("direccion") or "").strip()
    categoria = (data.get("categoria") or "").strip()
    estado = (data.get("estado") or "Activa").strip()

    if not nombre:
        return {
            "ok": False,
            "message": "El nombre de la tienda es obligatorio"
        }

    if not direccion:
        return {
            "ok": False,
            "message": "La dirección es obligatoria"
        }

    if not categoria:
        return {
            "ok": False,
            "message": "La categoría es obligatoria"
        }

    if estado not in ["Activa", "Inactiva"]:
        return {
            "ok": False,
            "message": "Estado inválido"
        }

    tienda = Tienda(
        nombre=nombre,
        direccion=direccion,
        categoria=categoria,
        estado=estado
    )

    tienda_creada = repo.crear(tienda)

    return {
        "ok": True,
        "message": "Tienda registrada correctamente",
        "tienda": tienda_creada.to_dict()
    }