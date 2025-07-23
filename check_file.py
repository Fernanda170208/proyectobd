# check_file.py
import os

print("\n--- INICIANDO VERIFICACIÓN FORENSE DE ARCHIVOS ---\n")

# 1. Calculamos la ruta base de nuestro proyecto
basedir = os.path.abspath(os.path.dirname(__file__))
print(f"[PASO 1] La carpeta raíz de tu proyecto es:\n   '{basedir}'\n")

# 2. Construimos la ruta completa a la carpeta de plantillas
templates_dir = os.path.join(basedir, 'app', 'templates')
print(f"[PASO 2] La ruta a la carpeta de plantillas debería ser:\n   '{templates_dir}'")

# 3. Verificamos si esa carpeta realmente existe
if os.path.isdir(templates_dir):
    print("   [RESULTADO] ¡ÉXITO! La carpeta 'templates' SÍ EXISTE.\n")
else:
    print("   [RESULTADO] ¡¡¡ERROR CRÍTICO!!! La carpeta 'templates' NO EXISTE o el nombre está mal escrito.\n")

# 4. Construimos la ruta completa al archivo index.html
index_file = os.path.join(templates_dir, 'index.html')
print(f"[PASO 3] La ruta al archivo HTML debería ser:\n   '{index_file}'")

# 5. Verificamos si ese archivo final existe
if os.path.isfile(index_file):
    print("   [RESULTADO] ¡ÉXITO TOTAL! El archivo 'index.html' SÍ EXISTE.\n")
else:
    print("   [RESULTADO] ¡¡¡ERROR CRÍTICO!!! El archivo 'index.html' NO EXISTE o el nombre está mal escrito.\n")

print("--- VERIFICACIÓN FINALIZADA ---\n")