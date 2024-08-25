import sqlite3

# Conectar a la base de datos
conexion = sqlite3.connect('tomyvet.db')
cursor = conexion.cursor()

# Listar todas las tablas en la base de datos
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tablas en la base de datos:")
for table in tables:
    print(table[0])

conexion.close()

