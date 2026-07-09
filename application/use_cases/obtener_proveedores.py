from domain.interfaces.proveedor_repo import ProveedorRepository


def obtener_proveedores(repo: ProveedorRepository):
    proveedores = repo.obtener_todos()

    return [
        proveedor.to_dict()
        for proveedor in proveedores
    ]