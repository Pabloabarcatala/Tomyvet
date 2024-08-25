import sqlite3
from app import app

# Crear el contexto de la aplicación
with app.app_context():
    # Conectar a la base de datos
    conexion = sqlite3.connect('tomyvet.db')
    cursor = conexion.cursor()

    # Agregar columna image a la tabla Patients
    try:
        cursor.execute('ALTER TABLE Patient ADD COLUMN image TEXT')
        print("Columna 'image' agregada exitosamente.")
    except sqlite3.OperationalError as e:
        print(f"Error al agregar la columna 'image': {e}")

    # Confirmar los cambios
    conexion.commit()
    conexion.close()
