from flask import Blueprint, jsonify, request, session

from application.use_cases.obtener_productos import obtener_productos
from application.use_cases.crear_producto import crear_producto
from infrastructure.database.producto_repo_impl import ProductoRepoImpl
from application.use_cases.actualizar_producto import actualizar_producto

producto_bp = Blueprint("producto", __name__)


def normalizar_rol():
    rol = session.get("rol", "cliente").strip().lower()

    if rol == "admin":
        return "administrador"

    return rol


def esta_autenticado():
    return "usuario" in session


def tiene_rol(roles_permitidos):
    return normalizar_rol() in roles_permitidos


@producto_bp.route("/api/v1/productos", methods=["GET"])
def api_obtener_productos():

    if not esta_autenticado():
        return jsonify({
            "ok": False,
            "message": "No autenticado"
        }), 401

    repo = ProductoRepoImpl()

    productos = obtener_productos(repo)

    return jsonify({
        "ok": True,
        "productos": productos
    }), 200


@producto_bp.route("/api/v1/productos", methods=["POST"])
def api_crear_producto():

    if not esta_autenticado():
        return jsonify({
            "ok": False,
            "message": "No autenticado"
        }), 401

    if not tiene_rol(["administrador", "trabajador"]):
        return jsonify({
            "ok": False,
            "message": "No tiene permisos para registrar productos"
        }), 403

    data = request.get_json() or {}

    repo = ProductoRepoImpl()

    resultado = crear_producto(data, repo)

    if not resultado["ok"]:
        return jsonify(resultado), 400

    return jsonify(resultado), 201

@producto_bp.route("/api/v1/productos/<producto_id>", methods=["PUT"])
def api_actualizar_producto(producto_id):

    if not esta_autenticado():
        return jsonify({
            "ok": False,
            "message": "No autenticado"
        }), 401

    if not tiene_rol(["administrador", "trabajador"]):
        return jsonify({
            "ok": False,
            "message": "No tiene permisos para actualizar productos"
        }), 403

    data = request.get_json() or {}

    repo = ProductoRepoImpl()

    resultado = actualizar_producto(producto_id, data, repo)

    if not resultado["ok"]:
        return jsonify(resultado), 400

    return jsonify(resultado), 200

@producto_bp.route("/api/v1/productos/<producto_id>", methods=["DELETE"])
def api_eliminar_producto(producto_id):

    if not esta_autenticado():
        return jsonify({
            "ok": False,
            "message": "No autenticado"
        }), 401

    if not tiene_rol(["administrador"]):
        return jsonify({
            "ok": False,
            "message": "Solo el administrador puede eliminar productos"
        }), 403

    repo = ProductoRepoImpl()

    eliminado = repo.eliminar_por_id(producto_id)

    if not eliminado:
        return jsonify({
            "ok": False,
            "message": "No se pudo eliminar el producto"
        }), 400

    return jsonify({
        "ok": True,
        "message": "Producto eliminado correctamente"
    }), 200