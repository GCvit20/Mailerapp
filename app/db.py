import mysql.connector 
import click
from flask import current_app, g
from flask.cli import with_appcontext
from .schema import instructions

def get_db():

    """
    Obtiene una conexión a la base de datos y un cursor asociado.

    Si la conexión a la base de datos no existe en el contexto global (g),
    se crea una nueva conexión utilizando la configuración de la aplicación Flask.

    Retorna:
    tuple: Una tupla que contiene la conexión a la base de datos y el cursor asociado.
           (db, c) donde db es un objeto de conexión MySQL y c es un cursor.

    La conexión a la base de datos y el cursor se almacenan en el contexto global (g)
    para ser reutilizados en la misma solicitud.

    Configuración:
    - `DATABASE_HOST`: Dirección del host de la base de datos.
    - `DATABASE_USER`: Usuario de la base de datos.
    - `DATABASE_PASSWORD`: Contraseña de la base de datos.
    - `DATABASE`: Nombre de la base de datos.
    """

    if 'db' not in g:
         g.db = mysql.connector.connect(
              host = current_app.config['DATABASE_HOST'],
              user = current_app.config['DATABASE_USER'],
              password = current_app.config['DATABASE_PASSWORD'],
              database = current_app.config['DATABASE']
         )
         g.c = g.db.cursor(dictionary=True)
    return g.db, g.c

def close_db(e=None):
    """
    Cierra la conexión a la base de datos.

    Este método es llamado al finalizar la solicitud. Si una conexión a la base de datos
    existe en el contexto global (g), la conexión se cierra adecuadamente.

    Parámetros:
    - e: Excepción (opcional).

    Retorna:
    None
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """
    Inicializa la base de datos ejecutando instrucciones SQL.

    Utiliza la función get_db() para obtener una conexión a la base de datos
    y un cursor asociado. Luego, ejecuta las instrucciones SQL almacenadas en
    la variable `instructions` y realiza la confirmación de la transacción.

    Retorna:
    None
    """
    db, c = get_db()

    for i in instructions:
        c.execute(i)
    db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    Comando de línea de comandos para inicializar la base de datos.

    Este comando llama a la función init_db() y muestra un mensaje indicando
    que la base de datos ha sido inicializada.

    Parámetros:
    None

    Retorna:
    None
    """
    init_db()
    click.echo('Base de datos inicializada')

def init_app(app):
    """
    Inicializa la aplicación Flask con funciones relacionadas con la base de datos.

    - Configura el cierre automático de la conexión a la base de datos al finalizar cada solicitud.
    - Agrega el comando de línea de comandos 'init-db' para inicializar la base de datos.

    Parámetros:
    - app: Instancia de la aplicación Flask.

    Retorna:
    None
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
