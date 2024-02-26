import os 
from flask import Flask
from . import db
from . import mails

def create_app():

    """
    Crea y configura una instancia de la aplicación Flask.

    Retorna:
    Flask: Una instancia de la aplicación Flask configurada.

    Configuración:
    - `SENDGRID_KEY`: Clave de la API de SendGrid para el servicio de correos.
    - `SECRET_KEY`: Clave secreta utilizada por Flask para operaciones criptográficas.
    - `DATABASE_HOST`: Dirección del host de la base de datos.
    - `DATABASE_PASSWORD`: Contraseña de la base de datos.
    - `DATABASE_USER`: Usuario de la base de datos.
    - `DATABASE`: Nombre de la base de datos.

    La configuración se obtiene de las variables de entorno.
    """
    app = Flask(__name__)

    app.config.from_mapping(
        FROM_EMAIL = os.environ.get('FROM_EMAIL'),
        SENDGRID_KEY = os.environ.get('SENDGRID_API_KEY'),
        SECRET_KEY = os.environ.get('SECRET_KEY'),
        DATABASE_HOST = os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD = os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER = os.environ.get('FLASK_DATABASE_USER'),
        DATABASE = os.environ.get('FLASK_DATABASE')
    )

    db.init_app(app)

    app.register_blueprint(mails.bp)
    
    return app

