from werkzeug.security import generate_password_hash

from domain.entities.usuario import Usuario
from domain.interfaces.usuario_repo import UsuarioRepository


def actualizar_usuario(
    usuario_id: str,
    data: dict,
    repo: UsuarioRepository
):

    nombre = (data.get("nombre") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = (data.get("password") or "").strip()
    rol = (data.get("rol") or "").strip()
    estado = data.get("estado", True)
    fecha_registro = (data.get("fechaRegistro") or "").strip()

    if isinstance(estado, str):
        estado = estado.lower() == "true"

    if not usuario_id:
        return {
            "ok": False,
            "message": "ID de usuario inválido"
        }

    if not nombre:
        return {
            "ok": False,
            "message": "El nombre es obligatorio"
        }

    if not email:
        return {
            "ok": False,
            "message": "El correo es obligatorio"
        }

    if "@" not in email:
        return {
            "ok": False,
            "message": "El correo no tiene un formato válido"
        }

    if rol not in ["admin", "trabajador", "cliente"]:
        return {
            "ok": False,
            "message": "Rol inválido"
        }

    password_hash = None

    if password:
        if len(password) < 6:
            return {
                "ok": False,
                "message": "La contraseña debe tener mínimo 6 caracteres"
            }

        password_hash = generate_password_hash(password)

    usuario = Usuario(
        id=usuario_id,
        nombre=nombre,
        email=email,
        password=password_hash,
        rol=rol,
        estado=estado,
        fecha_registro=fecha_registro
    )

    usuario_actualizado = repo.actualizar_por_id(
        usuario_id,
        usuario
    )

    if not usuario_actualizado:
        return {
            "ok": False,
            "message": "No se pudo actualizar el usuario"
        }

    return {
        "ok": True,
        "message": "Usuario actualizado correctamente",
        "usuario": usuario_actualizado.to_dict()
    }