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

# Inspeccionar cada tabla para ver sus columnas
for table in tables:
    print(f"\nColumnas en la tabla '{table[0]}':")
    cursor.execute(f"PRAGMA table_info({table[0]});")
    columns = cursor.fetchall()
    for column in columns:
        print(column)

conexion.close()
