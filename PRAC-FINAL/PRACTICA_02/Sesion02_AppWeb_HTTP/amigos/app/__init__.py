from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Inicializamos las extensiones
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # --- CONFIGURACIÓN FORZADA PARA QUE FUNCIONE YA ---
    # Usamos un archivo SQLite en la carpeta actual
    db_path = os.path.join(os.getcwd(), 'amigos.sqlite')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'clave-secreta-para-practica'
    # --------------------------------------------------

    db.init_app(app)
    migrate.init_app(app, db)

    # Registramos los Blueprints (las rutas)
    from .api.views import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from .html.views import html as html_blueprint
    app.register_blueprint(html_blueprint, url_prefix='/html')

    # --- MAGIA: CREAR TABLAS AUTOMÁTICAMENTE AL ARRANCAR ---
    with app.app_context():
        db.create_all()
        print(f"✅ BASE DE DATOS INICIADA EN: {db_path}")
    # -------------------------------------------------------

    return app