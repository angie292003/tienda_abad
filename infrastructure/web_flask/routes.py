from infrastructure.web_flask.controllers.admin_usuario_controller import admin_usuario_bp
from infrastructure.web_flask.controllers.usuario_controller import auth_bp
from infrastructure.web_flask.controllers.tienda_controller import tienda_bp
from infrastructure.web_flask.controllers.producto_controller import producto_bp
from infrastructure.web_flask.controllers.venta_controller import venta_bp
from infrastructure.web_flask.controllers.proveedor_controller import proveedor_bp
from infrastructure.web_flask.controllers.vista_controller import vista_bp

def register_routes(app):

    app.register_blueprint(admin_usuario_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(tienda_bp)
    app.register_blueprint(producto_bp)
    app.register_blueprint(venta_bp)
    app.register_blueprint(proveedor_bp)
    app.register_blueprint(vista_bp)