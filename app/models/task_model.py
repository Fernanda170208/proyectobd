# app/models/task_model.py
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Crea una conexión a la BD, usando la URL de Render si está disponible."""
    # Render establece una variable de entorno llamada DATABASE_URL
    database_url = os.getenv('DATABASE_URL')
    
    try:
        if database_url:
            # Si estamos en producción (Render), usamos la URL de conexión
            print("--- Conectando a la base de datos de producción (Render) ---")
            conn = psycopg2.connect(database_url)
        else:
            # Si estamos en local, usamos las variables del .env
            print("--- Conectando a la base de datos local ---")
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD')
            )
        return conn
    except psycopg2.Error as e:
        print(f"Error fatal al conectar a la base de datos: {e}")
        return None
    
# --- FUNCIÓN DE BÚSQUEDA MODIFICADA ---
def get_filtered_tasks(user_id, search_text=None, filtro_prioridad=None, filtro_categoria=None):
    """Obtiene las tareas de un usuario aplicando los filtros proporcionados."""
    conn = get_db_connection()
    if conn is None: return []
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "SELECT * FROM filtrar_tareas(%s, %s, %s, %s);",
        (user_id, search_text, filtro_prioridad, filtro_categoria)
    )
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return tasks

# --- NUEVA FUNCIÓN PARA OBTENER UNA TAREA ---
def get_task_by_id(task_id):
    """Obtiene los datos de una única tarea por su ID."""
    conn = get_db_connection()
    if conn is None: return None
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM get_tarea_por_id(%s);", (task_id,))
    task = cur.fetchone()
    cur.close()
    conn.close()
    return task

# --- NUEVA FUNCIÓN PARA ACTUALIZAR UNA TAREA ---
def update_task(task_id, nombre, descripcion, id_prioridad, id_categoria, id_estado):
    """Llama al procedimiento para actualizar una tarea existente."""
    conn = get_db_connection()
    if conn is None: return
    
    # Necesitamos el procedimiento original de tu BD
    # Nota: el procedimiento original no actualizaba el estado, se lo añadimos
    # como p_id_estado para completitud. Asumimos que existe un 
    # procedimiento actualizar_tarea con todos los campos.
    # Si no existe, puedes crearlo con:
    # CREATE OR REPLACE PROCEDURE actualizar_tarea(p_id_tarea INT, p_nombre TEXT, ...) ...
    # Aquí usaremos un UPDATE directo para asegurar que funcione.
    
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE tarea
        SET nombre = %s,
            descripcion = %s,
            id_prioridad = %s,
            id_categoria = %s,
            id_estado = %s,
            fecha_modificacion = NOW()
        WHERE id_tarea = %s;
        """,
        (nombre, descripcion, id_prioridad, id_categoria, id_estado, task_id)
    )
    conn.commit()
    cur.close()
    conn.close()


def add_task(nombre, descripcion, id_prioridad, id_categoria, id_usuario):
    conn = get_db_connection()
    if conn is None: return
    cur = conn.cursor()
    id_estado_pendiente = 1
    cur.execute(
        "CALL registrar_tarea(%s, %s, %s, %s, %s, %s);",
        (nombre, descripcion, id_estado_pendiente, id_prioridad, id_categoria, id_usuario)
    )
    conn.commit()
    cur.close()
    conn.close()

def delete_task_by_id(id_tarea):
    conn = get_db_connection()
    if conn is None: return
    cur = conn.cursor()
    cur.execute("CALL eliminar_tarea(%s);", (id_tarea,))
    conn.commit()
    cur.close()
    conn.close()