from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

# Inicialização das extensões
db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    """
    Cria e configura a aplicação Flask.
    Inicializa as extensões e registra os Blueprints.
    """
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Inicializar extensões
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Registro de rotas
    from .routes import (
        auth_routes,
        vendas_routes,
        despesas_routes,
        clientes_routes,
        funcionarios_routes,
        produtos_routes,
        relatorios_routes
    )
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(vendas_routes.bp)
    app.register_blueprint(despesas_routes.bp)
    app.register_blueprint(clientes_routes.bp)
    app.register_blueprint(funcionarios_routes.bp)
    app.register_blueprint(produtos_routes.bp)
    app.register_blueprint(relatorios_routes.bp)

    return app
