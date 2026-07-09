from flask import Blueprint, jsonify, request, session

from application.use_cases.obtener_proveedores import obtener_proveedores
from application.use_cases.crear_proveedor import crear_proveedor
from infrastructure.database.proveedor_repo_impl import ProveedorRepoImpl
from application.use_cases.actualizar_proveedor import actualizar_proveedor

proveedor_bp = Blueprint("proveedor", __name__)


def normalizar_rol():
    rol = session.get("rol", "cliente").strip().lower()

    if rol == "admin":
        return "administrador"

    return rol


def esta_autenticado():
    return "usuario" in session


def tiene_rol(roles_permitidos):
    return normalizar_rol() in roles_permitidos


@proveedor_bp.route("/api/v1/proveedores", methods=["GET"])
def api_obtener_proveedores():

    if not esta_autenticado():
        return jsonify({
            "ok": False,
            "message": "No autenticado"
        }), 401

    if not tiene_rol(["administrador", "trabajador"]):
        return jsonify({
            "ok": False,
            "message": "No tiene permisos para consultar proveedores"
        }), 403

    repo = ProveedorRepoImpl()

    proveedores = obtener_proveedores(repo)

    return jsonify({
        "ok": True,
        "proveedores": proveedores
    }), 200


@proveedor_bp.route("/api/v1/proveedores", methods=["POST"])
def api_crear_proveedor():

    if not esta_autenticado():
        return jsonify({
            "ok": False,
            "message": "No autenticado"
        }), 401

    if not tiene_rol(["administrador"]):
        return jsonify({
            "ok": False,
            "message": "Solo el administrador puede registrar proveedores"
        }), 403

    data = request.get_json() or {}

    repo = ProveedorRepoImpl()

    resultado = crear_proveedor(data, repo)

    if not resultado["ok"]:
        return jsonify(resultado), 400

    return jsonify(resultado), 201

@proveedor_bp.route("/api/v1/proveedores/<proveedor_id>", methods=["PUT"])
def api_actualizar_proveedor(proveedor_id):

    if not esta_autenticado():
        return jsonify({
            "ok": False,
            "message": "No autenticado"
        }), 401

    if not tiene_rol(["administrador"]):
        return jsonify({
            "ok": False,
            "message": "Solo el administrador puede actualizar proveedores"
        }), 403

    data = request.get_json() or {}

    repo = ProveedorRepoImpl()

    resultado = actualizar_proveedor(
        proveedor_id,
        data,
        repo
    )

    if not resultado["ok"]:
        return jsonify(resultado), 400

    return jsonify(resultado), 200

@proveedor_bp.route("/api/v1/proveedores/<proveedor_id>", methods=["DELETE"])
def api_desactivar_proveedor(proveedor_id):

    if not esta_autenticado():
        return jsonify({
            "ok": False,
            "message": "No autenticado"
        }), 401

    if not tiene_rol(["administrador"]):
        return jsonify({
            "ok": False,
            "message": "Solo el administrador puede desactivar proveedores"
        }), 403

    repo = ProveedorRepoImpl()

    desactivado = repo.desactivar_por_id(proveedor_id)

    if not desactivado:
        return jsonify({
            "ok": False,
            "message": "No se pudo desactivar el proveedor"
        }), 400

    return jsonify({
        "ok": True,
        "message": "Proveedor desactivado correctamente"
    }), 200