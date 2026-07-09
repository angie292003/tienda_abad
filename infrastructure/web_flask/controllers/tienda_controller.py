from flask import Blueprint, jsonify, request, session, Response

from application.use_cases.obtener_tiendas import obtener_tiendas
from application.use_cases.crear_tienda import crear_tienda
from application.use_cases.actualizar_tienda import actualizar_tienda
from infrastructure.database.tienda_repo_impl import TiendaRepoImpl


tienda_bp = Blueprint("tienda", __name__)


def normalizar_rol():
    rol = session.get("rol", "cliente").strip().lower()

    if rol == "admin":
        return "administrador"

    return rol


def esta_autenticado():
    return "usuario" in session


def tiene_rol(roles_permitidos):
    return normalizar_rol() in roles_permitidos


@tienda_bp.route("/api/v1/tiendas", methods=["GET"])
def api_obtener_tiendas():

    if not esta_autenticado():
        return jsonify({
            "ok": False,
            "message": "No autenticado"
        }), 401

    repo = TiendaRepoImpl()

    tiendas = obtener_tiendas(repo)

    return jsonify({
        "ok": True,
        "tiendas": tiendas
    }), 200


@tienda_bp.route("/api/v1/tiendas", methods=["POST"])
def api_crear_tienda():

    if not esta_autenticado():
        return jsonify({
            "ok": False,
            "message": "No autenticado"
        }), 401

    if not tiene_rol(["administrador"]):
        return jsonify({
            "ok": False,
            "message": "Solo el administrador puede registrar tiendas"
        }), 403

    data = request.get_json() or {}

    repo = TiendaRepoImpl()

    resultado = crear_tienda(data, repo)

    if not resultado["ok"]:
        return jsonify(resultado), 400

    return jsonify(resultado), 201


@tienda_bp.route("/api/v1/tiendas/<tienda_id>", methods=["PUT"])
def api_actualizar_tienda(tienda_id):

    if not esta_autenticado():
        return jsonify({
            "ok": False,
            "message": "No autenticado"
        }), 401

    if not tiene_rol(["administrador"]):
        return jsonify({
            "ok": False,
            "message": "Solo el administrador puede actualizar tiendas"
        }), 403

    data = request.get_json() or {}

    repo = TiendaRepoImpl()

    resultado = actualizar_tienda(
        tienda_id,
        data,
        repo
    )

    if not resultado["ok"]:
        return jsonify(resultado), 400

    return jsonify(resultado), 200


@tienda_bp.route("/api/v1/tiendas/xml", methods=["GET"])
def api_tiendas_xml():

    if not esta_autenticado():
        return Response(
            "<error>No autenticado</error>",
            status=401,
            mimetype="application/xml"
        )

    repo = TiendaRepoImpl()

    tiendas = obtener_tiendas(repo)

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += "<tiendas>\n"

    for tienda in tiendas:
        xml += "  <tienda>\n"
        xml += f"    <nombre>{tienda.get('nombre', '')}</nombre>\n"
        xml += f"    <direccion>{tienda.get('direccion', '')}</direccion>\n"
        xml += f"    <categoria>{tienda.get('categoria', '')}</categoria>\n"
        xml += f"    <estado>{tienda.get('estado', '')}</estado>\n"
        xml += "  </tienda>\n"

    xml += "</tiendas>"

    return Response(
        xml,
        mimetype="application/xml"
    )