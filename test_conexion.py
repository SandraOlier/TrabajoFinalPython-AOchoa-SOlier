import sqlite3

DB_PATH = "/Users/Andrea/Desktop/mascotas.db"

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre FROM mascotas")
    resultados = cursor.fetchall()
    print("Mascotas en la base de datos:")
    for fila in resultados:
        print(f"ID: {fila[0]}, Nombre: {fila[1]}")
    conn.close()
except Exception as e:
    print(f"Error: {e}")