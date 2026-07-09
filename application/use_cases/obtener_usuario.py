from domain.interfaces.usuario_repo import UsuarioRepository


def obtener_usuarios(repo: UsuarioRepository):
    usuarios = repo.obtener_todos()

    return [
        usuario.to_dict()
        for usuario in usuarios
    ]