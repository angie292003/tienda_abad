from flask import Blueprint, jsonify, request, session

from application.use_cases.obtener_usuario import obtener_usuarios
from application.use_cases.crear_usuario import crear_usuario
from application.use_cases.actualizar_usuario import actualizar_usuario
from infrastructure.database.usuario_repo_impl import UsuarioRepoImpl


admin_usuario_bp = Blueprint("admin_usuario", __name__)


def normalizar_rol():
    rol = session.get("rol", "cliente").strip().lower()

    if rol == "admin":
        return "administrador"

    return rol


def esta_autenticado():
    return "usuario" in session


def es_administrador():
    return normalizar_rol() == "administrador"


@admin_usuario_bp.route("/api/v1/usuarios", methods=["GET"])
def api_obtener_usuarios():

    if not esta_autenticado():
        return jsonify({
            "ok": False,
            "message": "No autenticado"
        }), 401

    if not es_administrador():
        return jsonify({
            "ok": False,
            "message": "Solo el administrador puede consultar usuarios"
        }), 403

    repo = UsuarioRepoImpl()

    usuarios = obtener_usuarios(repo)

    return jsonify({
        "ok": True,
        "usuarios": usuarios
    }), 200


@admin_usuario_bp.route("/api/v1/usuarios", methods=["POST"])
def api_crear_usuario():

    if not esta_autenticado():
        return jsonify({
            "ok": False,
            "message": "No autenticado"
        }), 401

    if not es_administrador():
        return jsonify({
            "ok": False,
            "message": "Solo el administrador puede registrar usuarios"
        }), 403

    data = request.get_json() or {}

    repo = UsuarioRepoImpl()

    resultado = crear_usuario(data, repo)

    if not resultado["ok"]:
        return jsonify(resultado), 400

    return jsonify(resultado), 201


@admin_usuario_bp.route("/api/v1/usuarios/<usuario_id>", methods=["PUT"])
def api_actualizar_usuario(usuario_id):

    if not esta_autenticado():
        return jsonify({
            "ok": False,
            "message": "No autenticado"
        }), 401

    if not es_administrador():
        return jsonify({
            "ok": False,
            "message": "Solo el administrador puede actualizar usuarios"
        }), 403

    data = request.get_json() or {}

    repo = UsuarioRepoImpl()

    resultado = actualizar_usuario(
        usuario_id,
        data,
        repo
    )

    if not resultado["ok"]:
        return jsonify(resultado), 400

    return jsonify(resultado), 200