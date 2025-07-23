# app/controllers/auth_controller.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user_model import create_user, find_user_by_email, check_password

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    correo = request.form['correo']
    contrasena = request.form['contrasena']
    
    user = find_user_by_email(correo)
    
    if user and check_password(user['contrasena'], contrasena):
        session.clear()
        session['user_id'] = user['id_usuario']
        session['user_name'] = user['nombre']
        return redirect(url_for('task.dashboard'))
    else:
        flash('Correo o contraseña incorrectos.', 'danger')
        return redirect(url_for('presentation.home'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        
        # --- ESTA ES LA PARTE QUE FALTABA Y QUE SOLUCIONA EL ERROR ---
        # Obtenemos los datos del formulario que el usuario envió desde la página de registro
        nombre = request.form['nombre']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        confirmar_contrasena = request.form['confirmar_contrasena']

        # --- Validaciones que ya tenías ---
        if contrasena != confirmar_contrasena:
            flash('Las contraseñas no coinciden. Por favor, verifícalas.', 'warning')
            return redirect(url_for('auth.register'))
        
        if find_user_by_email(correo):
            flash('El correo electrónico ya está registrado. Por favor, usa otro.', 'warning')
            return redirect(url_for('auth.register'))

        # Ahora el bloque try/except funcionará porque las variables ya existen
        try:
            # Esta llamada ahora tiene las variables 'nombre', 'correo' y 'contrasena' definidas
            create_user(nombre, correo, contrasena)
            flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('presentation.home'))
        except Exception as e:
            flash(f'Ocurrió un error inesperado al registrar el usuario: {e}', 'danger')
            return redirect(url_for('auth.register'))

    # Si el método es GET, simplemente muestra la página de registro
    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado la sesión correctamente.', 'info')
    return redirect(url_for('presentation.home'))