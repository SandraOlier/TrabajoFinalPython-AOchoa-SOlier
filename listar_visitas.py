import sqlite3

def listar_visitas():
    conn = sqlite3.connect("/Users/Andrea/Desktop/mascotas.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT v.id, m.nombre AS mascota, vet.nombre AS veterinario, esp.nombre AS especialidad, v.fecha, v.motivo
        FROM visitas v
        JOIN mascotas m ON v.id_mascota = m.id
        JOIN veterinarios vet ON v.id_veterinario = vet.id
        JOIN especialidades esp ON v.id_especialidad = esp.id;
    """)
    
    filas = cursor.fetchall()
    conn.close()
    
    for fila in filas:
        id_visita, mascota, veterinario, especialidad, fecha, motivo = fila
        print(f"Visita #{id_visita}: Mascota: {mascota}, Veterinario: {veterinario} ({especialidad}), Fecha: {fecha}, Motivo: {motivo}")

if __name__ == "__main__":
    listar_visitas()
