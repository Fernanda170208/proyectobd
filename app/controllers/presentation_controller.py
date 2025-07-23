# app/controllers/presentation_controller.py
from flask import Blueprint, render_template

# Esta es la línea que define la variable que run.py no puede encontrar
presentation_bp = Blueprint('presentation', __name__)

@presentation_bp.route('/')
def home():
    """Muestra la página de presentación pública."""
    return render_template('home.html')