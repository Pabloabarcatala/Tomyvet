import sqlite3

# Conectar a la base de datos
conexion = sqlite3.connect('tomyvet.db')
cursor = conexion.cursor()

# Agregar las nuevas columnas a la tabla Patients
try:
    cursor.execute('ALTER TABLE Patients ADD COLUMN country TEXT')
    cursor.execute('ALTER TABLE Patients ADD COLUMN region TEXT')
    cursor.execute('ALTER TABLE Patients ADD COLUMN comuna TEXT')
    print("Columnas agregadas exitosamente")
except sqlite3.OperationalError as e:
    print(f"Error al agregar las columnas: {e}")

# Confirmar los cambios
conexion.commit()
conexion.close()
