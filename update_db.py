import sqlite3

# Conectar a la base de datos
conexion = sqlite3.connect('tomyvet.db')
cursor = conexion.cursor()

# Nombre correcto de la tabla basado en la salida del script anterior
nombre_tabla = 'patients'  # Asegúrate de usar el nombre correcto

# Función para verificar si una columna existe en una tabla
def columna_existe(nombre_tabla, nombre_columna):
    cursor.execute(f"PRAGMA table_info({nombre_tabla})")
    columnas = [columna[1] for columna in cursor.fetchall()]
    return nombre_columna in columnas

# Columnas a agregar
columnas_a_agregar = ['country', 'region', 'comuna']

# Intentar agregar las columnas si no existen
for columna in columnas_a_agregar:
    if not columna_existe(nombre_tabla, columna):
        try:
            cursor.execute(f"ALTER TABLE {nombre_tabla} ADD COLUMN {columna} TEXT")
            print(f"Columna '{columna}' agregada exitosamente.")
        except sqlite3.OperationalError as e:
            print(f"Error al agregar columna '{columna}': {e}")
    else:
        print(f"La columna '{columna}' ya existe en la tabla '{nombre_tabla}'.")

conexion.commit()
conexion.close()
