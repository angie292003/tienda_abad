from typing import Dict

from werkzeug.security import check_password_hash
from domain.interfaces.usuario_repo import UsuarioRepository


def verificar_password(password_guardada: str, password_ingresada: str) -> bool:
    """
    Permite trabajar con contraseñas hasheadas y también con texto plano temporalmente.
    Lo correcto en producción es usar siempre hash.
    """

    if not password_guardada:
        return False

    try:
        if ":" in password_guardada and "$" in password_guardada:
            return check_password_hash(password_guardada, password_ingresada)
    except Exception:
        return False

    return password_guardada == password_ingresada


def login_usuario(email: str, password: str, repo: UsuarioRepository) -> Dict:

    usuario = repo.obtener_por_email(email)

    if usuario is None:
        return {
            "ok": False,
            "message": "Usuario no encontrado"
        }

    if not verificar_password(usuario.password_hash, password):
        return {
            "ok": False,
            "message": "Contraseña incorrecta"
        }

    return {
        "ok": True,
        "usuario": usuario.to_dict()
    }