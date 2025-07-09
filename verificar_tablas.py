print("Ejecutando verificar_tablas.py...")
DB_PATH = "mascotas.db"
print(f"Usando base de datos en: {DB_PATH}")

import sqlite3

def verificar_tabla(nombre_tabla):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name=?
        """, (nombre_tabla,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado is not None
    except Exception as e:
        print(f"Error al acceder a la base de datos: {e}")
        return False

tablas_a_verificar = ["mascotas", "veterinarios", "especialidades", "visitas", "duenios"]

for tabla in tablas_a_verificar:
    existe = verificar_tabla(tabla)
    if existe:
        print(f"✅ La tabla '{tabla}' existe.")
    else:
        print(f"❌ La tabla '{tabla}' NO existe.")

