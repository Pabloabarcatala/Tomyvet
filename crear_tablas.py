import sqlite3

conexion = sqlite3.connect('tomyvet.db')
cursor = conexion.cursor()

# Crear tabla de usuarios
cursor.execute('''
CREATE TABLE IF NOT EXISTS Usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# Crear tabla de pacientes
cursor.execute('''
CREATE TABLE IF NOT EXISTS Pacientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    nombre_dueno TEXT NOT NULL,
    direccion_dueno TEXT NOT NULL,
    telefono_dueno TEXT NOT NULL,
    tipo_animal TEXT NOT NULL,
    raza TEXT NOT NULL,
    edad INTEGER NOT NULL,
    historial_medico TEXT
)
''')

# Crear tabla de citas
cursor.execute('''
CREATE TABLE IF NOT EXISTS Citas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_paciente TEXT NOT NULL,
    fecha TEXT NOT NULL,
    motivo TEXT NOT NULL
)
''')

# Crear tabla de inventario
cursor.execute('''
CREATE TABLE IF NOT EXISTS Inventario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_medicamento TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL
)
''')

# Crear tabla de facturas
cursor.execute('''
CREATE TABLE IF NOT EXISTS Facturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_paciente TEXT NOT NULL,
    monto_total REAL NOT NULL,
    fecha TEXT NOT NULL
)
''')

conexion.commit()
conexion.close()
