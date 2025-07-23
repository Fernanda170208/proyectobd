# run.py
import os
from flask import Flask
from app.controllers.presentation_controller import presentation_bp
from app.controllers.auth_controller import auth_bp
from app.controllers.task_controller import task_bp

basedir = os.path.abspath(os.path.dirname(__file__))
template_folder_path = os.path.join(basedir, 'app', 'templates')
static_folder_path = os.path.join(basedir, 'app', 'static')

def create_app():
    app = Flask(__name__,
                template_folder=template_folder_path,
                static_folder=static_folder_path)
    
    # Render usa una variable de entorno para las claves secretas
    app.secret_key = os.getenv('SECRET_KEY', 'una-clave-secreta-por-defecto-para-local')
    
    app.register_blueprint(presentation_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)
    
    return app

# Esta variable 'app' es la que Gunicorn buscará
app = create_app()

# El bloque if __name__ == '__main__' ya no es estrictamente necesario
# para el despliegue con Gunicorn, pero es bueno mantenerlo para pruebas locales.
if __name__ == '__main__':
    app.run() 