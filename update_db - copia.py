import sqlite3

# Conectar a la base de datos
conexion = sqlite3.connect('tomyvet.db')
cursor = conexion.cursor()

# Crear la tabla 'patients' con todas las columnas necesarias
cursor.execute('''
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    owner_name TEXT NOT NULL,
    owner_address TEXT NOT NULL,
    owner_phone TEXT NOT NULL,
    animal_type TEXT NOT NULL,
    breed TEXT NOT NULL,
    age INTEGER NOT NULL,
    medical_history TEXT,
    image TEXT,
    country TEXT,
    region TEXT,
    comuna TEXT
)
''')

# Confirmar los cambios
conexion.commit()
conexion.close()

print("Tabla 'patients' creada exitosamente con todas las columnas necesarias.")

