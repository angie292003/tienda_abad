from flask import (
    Blueprint,
    request,
    jsonify,
    session,
    render_template,
    redirect,
    url_for
)

from application.use_cases.login_usuario import login_usuario
from infrastructure.database.usuario_repo_impl import UsuarioRepositoryMongo


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def login_page():

    if "usuario" in session:
        return redirect(url_for("auth.home"))

    return render_template("index.html")


@auth_bp.route("/home")
def home():

    if "usuario" not in session:
        return redirect(url_for("auth.login_page"))

    return render_template(
        "home.html",
        usuario=session["usuario"],
        rol=session.get("rol", "cliente")
    )


@auth_bp.route("/api/v1/auth/login", methods=["POST"])
def auth_login():

    if not request.is_json:
        return jsonify({
            "ok": False,
            "message": "Contenido no válido"
        }), 400

    data = request.get_json() or {}

    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or len(password) < 6:
        return jsonify({
            "ok": False,
            "message": "Datos inválidos"
        }), 400

    repo = UsuarioRepositoryMongo()

    resultado = login_usuario(
        email=email,
        password=password,
        repo=repo
    )

    if not resultado["ok"]:
        return jsonify(resultado), 401

    usuario = resultado["usuario"]

    session["usuario"] = usuario["email"]
    session["rol"] = usuario["rol"]

    response = jsonify({
        "ok": True,
        "usuario": usuario["email"],
        "rol": usuario["rol"]
    })

    response.headers["Cache-Control"] = "no-store"

    return response


@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("auth.login_page"))