from domain.interfaces.tienda_repo import TiendaRepository


def obtener_tiendas(repo: TiendaRepository):
    tiendas = repo.obtener_todas()

    return [
        tienda.to_dict()
        for tienda in tiendas
    ]