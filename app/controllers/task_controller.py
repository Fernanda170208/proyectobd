# app/controllers/task_controller.py

# -------------------------------------
# 1. IMPORTACIONES NECESARIAS
# -------------------------------------
# Importamos las herramientas de Flask que usaremos
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
# Importamos 'wraps' para crear decoradores de forma correcta
from functools import wraps

# Importamos TODAS las funciones que necesitamos de nuestro modelo de tareas
from app.models.task_model import get_filtered_tasks, get_task_by_id, update_task, add_task, delete_task_by_id

# -------------------------------------
# 2. DEFINICIÓN DEL BLUEPRINT
# -------------------------------------
# Creamos un Blueprint para agrupar todas las rutas relacionadas con las tareas.
task_bp = Blueprint('task', __name__)

# ----------------------------------------------------
# 3. DECORADOR DE SEGURIDAD (LOGIN REQUERIDO)
# ----------------------------------------------------
# Esta es una función "decoradora". Su propósito es proteger rutas para que
# solo usuarios que han iniciado sesión puedan acceder a ellas.
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Revisa si el 'user_id' NO está guardado en la sesión del navegador.
        if 'user_id' not in session:
            # Si no está, muestra un mensaje de advertencia.
            flash('Debes iniciar sesión para acceder a esta página.', 'warning')
            # Y redirige al usuario a la página de inicio.
            return redirect(url_for('presentation.home'))
        # Si el 'user_id' SÍ está en la sesión, permite que la función original se ejecute.
        return f(*args, **kwargs)
    return decorated_function

# -------------------------------------
# 4. DEFINICIÓN DE LAS RUTAS
# -------------------------------------

# --- Ruta para el Panel Principal de Tareas ---
@task_bp.route('/dashboard')
@login_required # Aplicamos el decorador de seguridad
def dashboard():
    # Obtenemos el ID del usuario que está actualmente logueado desde la sesión.
    user_id = session['user_id']
    
    # Obtenemos los valores de los filtros desde la URL (ej: /dashboard?search=comprar)
    search_text = request.args.get('search', None)
    filtro_prioridad = request.args.get('filtro_prioridad', None)
    filtro_categoria = request.args.get('filtro_categoria', None)

    # El formulario envía los IDs como texto. Los convertimos a número (integer)
    # o los dejamos como None si el usuario seleccionó "Todas".
    filtro_prioridad = int(filtro_prioridad) if filtro_prioridad else None
    filtro_categoria = int(filtro_categoria) if filtro_categoria else None

    # Llamamos a la función del modelo que sabe cómo buscar y filtrar en la BD.
    tasks = get_filtered_tasks(user_id, search_text, filtro_prioridad, filtro_categoria)
    
    # Mostramos la plantilla 'dashboard.html' y le pasamos la lista de tareas
    # y los valores de los filtros para que los menús desplegables "recuerden" la selección.
    return render_template('dashboard.html', tasks=tasks, 
                           search_query=search_text,
                           selected_priority=filtro_prioridad,
                           selected_category=filtro_categoria)

# --- Ruta para Añadir una Nueva Tarea ---
@task_bp.route('/add', methods=['POST'])
@login_required
def add():
    user_id = session['user_id']
    try:
        nombre = request.form['nombre']
        descripcion = request.form.get('descripcion', '') # .get es más seguro para campos opcionales
        id_categoria = int(request.form['id_categoria'])
        id_prioridad = int(request.form['id_prioridad'])

        add_task(nombre, descripcion, id_prioridad, id_categoria, user_id)
        flash('¡Tarea añadida con éxito!', 'success')
    except Exception as e:
        flash(f'Error al añadir la tarea: {e}', 'danger')
            
    return redirect(url_for('task.dashboard'))

# --- Ruta para Mostrar el Formulario de Edición ---
@task_bp.route('/edit/<int:task_id>', methods=['GET'])
@login_required
def edit_task_form(task_id):
    # Obtenemos los datos de la tarea específica que se quiere editar.
    task = get_task_by_id(task_id)
    if task is None:
        flash('La tarea que intentas editar no existe.', 'danger')
        return redirect(url_for('task.dashboard'))
    
    # Mostramos la plantilla 'edit_task.html' y le pasamos los datos de la tarea
    # para que pueda rellenar los campos del formulario.
    return render_template('edit_task.html', task=task)

# --- Ruta para Procesar la Actualización de una Tarea ---
@task_bp.route('/update/<int:task_id>', methods=['POST'])
@login_required
def update_task_action(task_id):
    try:
        nombre = request.form['nombre']
        descripcion = request.form.get('descripcion', '')
        id_prioridad = int(request.form['id_prioridad'])
        id_categoria = int(request.form['id_categoria'])
        id_estado = int(request.form['id_estado'])
        
        update_task(task_id, nombre, descripcion, id_prioridad, id_categoria, id_estado)
        flash('¡Tarea actualizada correctamente!', 'success')
    except Exception as e:
        flash(f'Error al actualizar la tarea: {e}', 'danger')

    return redirect(url_for('task.dashboard'))

# --- Ruta para Eliminar una Tarea ---
@task_bp.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete(task_id):
    try:
        delete_task_by_id(task_id)
        flash('Tarea eliminada con éxito.', 'info')
    except Exception as e:
        flash(f'Error al eliminar la tarea: {e}', 'danger')

    return redirect(url_for('task.dashboard'))