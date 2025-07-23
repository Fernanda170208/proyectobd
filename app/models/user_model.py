# app/models/user_model.py

# Importamos la función para reutilizar la conexión a la BD
from .task_model import get_db_connection
from psycopg2.extras import RealDictCursor

def create_user(nombre, correo, contrasena):
    conn = get_db_connection()
    if conn is None: return False
    cur = conn.cursor()
    cur.execute("CALL registrar_usuario(%s, %s, %s);", (nombre, correo, contrasena))
    conn.commit()
    cur.close()
    conn.close()
    return True

def find_user_by_email(correo):
    """Busca un usuario por su correo electrónico y devuelve sus datos."""
    conn = get_db_connection()
    if conn is None: 
        return None
    
    # Usamos RealDictCursor para que el resultado sea un diccionario
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM buscar_usuario_por_correo(%s);", (correo,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

def check_password(stored_password, plain_password):
    """Compara la contraseña guardada con la que el usuario ingresó (ambas en texto plano)."""
    # Como no hay encriptación, es una simple comparación de texto
    return stored_password == plain_password

def find_user_by_email(correo):
    """Busca un usuario por su correo electrónico y devuelve sus datos."""
    conn = get_db_connection()
    if conn is None: 
        return None
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    # Esta línea ahora funcionará porque 'buscar_usuario_por_correo' ya existe
    cur.execute("SELECT * FROM buscar_usuario_por_correo(%s);", (correo,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user