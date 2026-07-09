from domain.entities.tienda import Tienda
from domain.interfaces.tienda_repo import TiendaRepository


def actualizar_tienda(
    tienda_id: str,
    data: dict,
    repo: TiendaRepository
):

    nombre = (data.get("nombre") or "").strip()
    direccion = (data.get("direccion") or "").strip()
    categoria = (data.get("categoria") or "").strip()
    estado = (data.get("estado") or "Activa").strip()

    if not tienda_id:
        return {
            "ok": False,
            "message": "ID de tienda inválido"
        }

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
        id=tienda_id,
        nombre=nombre,
        direccion=direccion,
        categoria=categoria,
        estado=estado
    )

    tienda_actualizada = repo.actualizar_por_id(
        tienda_id,
        tienda
    )

    if not tienda_actualizada:
        return {
            "ok": False,
            "message": "No se pudo actualizar la tienda"
        }

    return {
        "ok": True,
        "message": "Tienda actualizada correctamente",
        "tienda": tienda_actualizada.to_dict()
    }