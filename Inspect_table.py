import sqlite3

# Conectar a la base de datos
conexion = sqlite3.connect('tomyvet.db')
cursor = conexion.cursor()

# Verificar el contenido de la tabla
cursor.execute("PRAGMA table_info(Patient);")
columns = cursor.fetchall()

print("Columnas en la tabla 'Patient':")
for column in columns:
    print(column)

conexion.close()
