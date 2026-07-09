from domain.interfaces.productos_repo import ProductoRepository


def obtener_productos(repo: ProductoRepository):
    productos = repo.obtener_todos()

    return [
        producto.to_dict()
        for producto in productos
    ]