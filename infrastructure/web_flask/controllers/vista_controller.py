import os

from flask import Blueprint, render_template, session, abort


vista_bp = Blueprint("vista", __name__)


@vista_bp.route("/views/home/<nombre_vista>")
def cargar_vista_home(nombre_vista):

    if "usuario" not in session:
        return "No autorizado", 401

    vistas_permitidas = {
        "productos.html",
        "ventas.html",
        "proveedores.html",
        "tiendas.html",
        "usuarios.html",
        "reportes.html",
        "perfil.html",
        "configuracion.html",
        "carrito.html"
    }

    if nombre_vista not in vistas_permitidas:
        abort(404)

    return render_template(
        f"home/{nombre_vista}",
        google_maps_api_key=os.getenv("GOOGLE_MAPS_API_KEY", "")
    )