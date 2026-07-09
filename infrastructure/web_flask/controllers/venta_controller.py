from flask import Blueprint, jsonify, request, session

from application.use_cases.obtener_ventas import obtener_ventas
from application.use_cases.crear_ventas import crear_venta
from infrastructure.database.venta_repo_impl import VentaRepoImpl


venta_bp = Blueprint("venta", __name__)


def normalizar_rol():
    rol = session.get("rol", "cliente").strip().lower()

    if rol == "admin":
        return "administrador"

    return rol


def esta_autenticado():
    return "usuario" in session


def tiene_rol(roles_permitidos):
    return normalizar_rol() in roles_permitidos


@venta_bp.route("/api/v1/ventas", methods=["GET"])
def api_obtener_ventas():

    if not esta_autenticado():
        return jsonify({
            "ok": False,
            "message": "No autenticado"
        }), 401

    if not tiene_rol(["administrador", "trabajador"]):
        return jsonify({
            "ok": False,
            "message": "No tiene permisos para consultar ventas"
        }), 403

    repo = VentaRepoImpl()

    ventas = obtener_ventas(repo)

    return jsonify({
        "ok": True,
        "ventas": ventas
    }), 200


@venta_bp.route("/api/v1/ventas", methods=["POST"])
def api_crear_venta():

    if not esta_autenticado():
        return jsonify({
            "ok": False,
            "message": "No autenticado"
        }), 401

    data = request.get_json() or {}

    data["usuario"] = session.get("usuario")
    data["rol"] = normalizar_rol()

    repo = VentaRepoImpl()

    resultado = crear_venta(data, repo)

    if not resultado["ok"]:
        return jsonify(resultado), 400

    return jsonify(resultado), 201