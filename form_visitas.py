import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime

DB_PATH = "mascotas.db"

def validar_fecha(fecha_texto):
    try:
        datetime.datetime.strptime(fecha_texto, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def cargar_mascotas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre FROM mascotas")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def cargar_veterinarios():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre FROM veterinarios WHERE activo=1")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def cargar_especialidades_veterinario(id_veterinario):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.nombre FROM especialidades e
        JOIN veterinarios_especialidades ve ON e.id = ve.id_especialidad
        WHERE ve.id_veterinario = ?
    """, (id_veterinario,))
    resultados = [fila[0] for fila in cursor.fetchall()]
    conn.close()
    return resultados

def cargar_todas_especialidades():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM especialidades")
    resultados = [fila[0] for fila in cursor.fetchall()]
    conn.close()
    return resultados

def cargar_visitas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            v.id,
            m.nombre AS mascota,
            vet.nombre AS veterinario,
            e.nombre AS especialidad,
            v.fecha,
            v.motivo,
            v.observaciones
        FROM visitas v
        JOIN mascotas m ON v.id_mascota = m.id
        JOIN veterinarios vet ON v.id_veterinario = vet.id
        JOIN especialidades e ON v.id_especialidad = e.id
        ORDER BY v.fecha DESC
    """)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def actualizar_combo_especialidad(event=None):
    veterinario_nombre = combo_veterinario.get()
    if not veterinario_nombre:
        combo_especialidad['values'] = []
        combo_especialidad.set('')
        return
    id_vet = dic_veterinarios.get(veterinario_nombre)
    especialidades = cargar_especialidades_veterinario(id_vet)
    combo_especialidad['values'] = especialidades
    if especialidades:
        combo_especialidad.set(especialidades[0])  # seleccionamos la primera especialidad
    else:
        combo_especialidad.set('')  # limpiamos si no hay especialidades
        
def guardar_visita():
    mascota = combo_mascotas.get()
    veterinario = combo_veterinario.get()
    especialidad_nombre = combo_especialidad.get()
    fecha = entry_fecha.get()
    motivo = combo_motivo.get()
    observaciones = text_observaciones.get("1.0", tk.END).strip()

    if not (mascota and veterinario and especialidad_nombre and fecha and motivo):
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    if not validar_fecha(fecha):
        messagebox.showerror("Error", "Fecha inválida. Usá el formato YYYY-MM-DD.")
        return

    id_mascota = dic_mascotas.get(mascota)
    id_veterinario = dic_veterinarios.get(veterinario)

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM especialidades WHERE nombre = ?", (especialidad_nombre,))
        res = cursor.fetchone()
        if not res:
            messagebox.showerror("Error", "Especialidad no encontrada.")
            conn.close()
            return
        id_especialidad = res[0]

        cursor.execute("""
            INSERT INTO visitas (id_mascota, id_veterinario, id_especialidad, fecha, motivo, observaciones)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (id_mascota, id_veterinario, id_especialidad, fecha, motivo, observaciones))

        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Visita guardada correctamente.")

        # Limpiar campos
        combo_mascotas.set('')
        combo_veterinario.set('')
        combo_especialidad['values'] = []
        combo_especialidad.set('')
        entry_fecha.delete(0, tk.END)
        combo_motivo.set('')
        text_observaciones.delete("1.0", tk.END)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar la visita: {e}")

    finally:
        try:
            conn.close()
        except:
            pass        

def abrir_ventana_visitas():
    ventana_visitas = tk.Toplevel(root)
    ventana_visitas.title("Visitas Guardadas")
    ventana_visitas.geometry("900x400")

    # Tabla (Treeview)
    columnas = ("id", "mascota", "veterinario", "especialidad", "fecha", "motivo", "observaciones")
    tree = ttk.Treeview(ventana_visitas, columns=columnas, show='headings')

    for col in columnas:
        tree.heading(col, text=col.capitalize())
        tree.column(col, anchor='center', width=120)
    tree.column("observaciones", width=200)

    tree.pack(expand=True, fill='both')

    def cargar_datos():
        for fila in tree.get_children():
            tree.delete(fila)
        datos = cargar_visitas()
        for fila in datos:
            tree.insert('', tk.END, values=fila)
            #linea nueva
     # Frame para botones
    frame_botones = tk.Frame(ventana_visitas)
    frame_botones.pack(pady=5)
    btn_refrescar = tk.Button(frame_botones, text="Actualizar", command=cargar_datos,
                             bg="#d2bc90", fg="black", activebackground="#3399ff",
                             relief="flat", borderwidth=0, font=("Arial", 10, "bold"), width=15)
    btn_refrescar.pack(side=tk.LEFT, padx=5)

    btn_cerrar = tk.Button(frame_botones, text="Cerrar", command=ventana_visitas.destroy,
                          bg="white", fg="black", activebackground="#3399ff",
                          relief="flat", borderwidth=0, font=("Arial", 10, "bold"), width=15)
    btn_cerrar.pack(side=tk.LEFT, padx=5)


    #codigo original nuestro
    #btn_refrescar = tk.Button(ventana_visitas, text="Actualizar", command=cargar_datos)
    #btn_refrescar.pack(pady=5)

    cargar_datos()

# --- Interfaz gráfica principal ---

root = tk.Tk()
root.title("Formulario de Visitas")
root.geometry("480x460")
root.config(bg="#e9d8a6")#nuevo

lista_mascotas = cargar_mascotas()
lista_veterinarios = cargar_veterinarios()

dic_mascotas = {nombre: _id for _id, nombre in lista_mascotas}
dic_veterinarios = {nombre: _id for _id, nombre in lista_veterinarios}

tk.Label(root, text="Mascota", bg="#e9d8a6").grid(row=0, column=0, padx=10, pady=5, sticky='e')
combo_mascotas = ttk.Combobox(root, values=list(dic_mascotas.keys()), state="readonly")
combo_mascotas.grid(row=0, column=1, padx=(10, 20), pady=(30, 5))#modifico esto padx=10, pady=5

tk.Label(root, text="Veterinario", bg="#e9d8a6" ).grid(row=1, column=0, padx=10, pady=5, sticky='e')
combo_veterinario = ttk.Combobox(root, values=list(dic_veterinarios.keys()), state="readonly")
combo_veterinario.grid(row=1, column=1, padx=(10, 20))
combo_veterinario.bind("<<ComboboxSelected>>", actualizar_combo_especialidad)

tk.Label(root, text="Especialidad", bg="#e9d8a6").grid(row=2, column=0, padx=10, pady=5, sticky='e')
combo_especialidad = ttk.Combobox(root, values=[], state="readonly")
combo_especialidad.grid(row=2, column=1, padx=(10, 20))

tk.Label(root, text="Fecha (YYYY-MM-DD)", bg="#e9d8a6").grid(row=3, column=0, padx=10, pady=5, sticky='e')
entry_fecha = tk.Entry(root)
entry_fecha.grid(row=3, column=1, padx=(10, 20))
tk.Label(root, text="Ej: 2025-06-21", fg="black", font=("Arial", 8), bg="#e9d8a6").grid(row=4, column=1, sticky='w', padx=(20,0), pady=(0, 5))

tk.Label(root, text="Motivo", bg="#e9d8a6").grid(row=5, column=0, padx=10, pady=5, sticky='e')
motivos = ["Consulta", "Vacunación", "Control", "Emergencia", "Desparasitación", "Otros"]
combo_motivo = ttk.Combobox(root, values=motivos, state="readonly")
combo_motivo.grid(row=5, column=1, padx=(10, 20))

tk.Label(root, text="Observaciones", bg="#e9d8a6").grid(row=6, column=0, padx=10, pady=5, sticky='ne')
text_observaciones = tk.Text(root, width=30, height=5)
text_observaciones.grid(row=6, column=1, padx=(0, 10), pady=5, sticky='w')

#btn_guardar = tk.Button(root, text="Guardar Visita", bg="#e9d8a6", command=guardar_visita)
btn_guardar = tk.Button(
    root,
    text="Guardar Visita",
    command=guardar_visita,
    bg="white",                 # Fondo blanco
    activebackground="#3399ff", # Fondo azul al presionar
    fg="black",                 # Texto negro
    relief="flat",              # Elimina relieve/3D
    borderwidth=0,             # Sin borde
    highlightthickness=0       # Sin borde resaltado
)
btn_guardar.grid(row=7, column=0, columnspan=2, pady=30, padx=(80,0))#agregue pady y padx

btn_ver_visitas = tk.Button(root, text="Ver Visitas Guardadas", bg="#e9d8a6", command=abrir_ventana_visitas, activebackground="#3399ff", fg="black", relief="flat", borderwidth=0, highlightthickness=0)
#btn_ver_visitas.grid(row=8, column=0, columnspan=2, pady=10, padx=(80, 0))
btn_ver_visitas.grid(row=8, column=0, columnspan=2, pady=(0, 15), padx=(80, 0))

btn_cerrar = tk.Button(root, text="Cerrar", command=root.destroy,
                       bg="white", fg="black", activebackground="#3399ff",
                       relief="flat", borderwidth=0, font=("Arial", 10, "bold"), width=10)
btn_cerrar.grid(row=9, column=0, columnspan=2, pady=(0, 15), padx=(80, 0))

root.mainloop()






