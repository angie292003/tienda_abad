from datetime import datetime

from werkzeug.security import generate_password_hash

from domain.entities.usuario import Usuario
from domain.interfaces.usuario_repo import UsuarioRepository


def crear_usuario(data: dict, repo: UsuarioRepository):

    nombre = (data.get("nombre") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = (data.get("password") or "").strip()
    rol = (data.get("rol") or "").strip()
    estado = data.get("estado", True)

    if isinstance(estado, str):
        estado = estado.lower() == "true"

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

    if not password:
        return {
            "ok": False,
            "message": "La contraseña es obligatoria"
        }

    if len(password) < 6:
        return {
            "ok": False,
            "message": "La contraseña debe tener mínimo 6 caracteres"
        }

    if rol not in ["admin", "trabajador", "cliente"]:
        return {
            "ok": False,
            "message": "Rol inválido"
        }

    password_hash = generate_password_hash(password)

    usuario = Usuario(
        nombre=nombre,
        email=email,
        password=password_hash,
        rol=rol,
        estado=estado,
        fecha_registro=datetime.now().strftime("%Y-%m-%d")
    )

    usuario_creado = repo.crear(usuario)

    if not usuario_creado:
        return {
            "ok": False,
            "message": "No se pudo crear el usuario. Puede que el correo ya exista."
        }

    return {
        "ok": True,
        "message": "Usuario registrado correctamente",
        "usuario": usuario_creado.to_dict()
    }