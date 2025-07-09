import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkinter import ROUND

DB_PATH = "mascotas.db"

def guardar_mascota():
    nombre = entry_nombre.get().strip()
    especie = entry_especie.get().strip()
    raza = entry_raza.get().strip()
    edad = entry_edad.get().strip()
    duenio_nombre = entry_duenio_nombre.get().strip()
    duenio_apellido = entry_duenio_apellido.get().strip()

    if not (nombre and especie and edad and duenio_nombre and duenio_apellido):
        messagebox.showwarning("Campos vacíos", "Completá todos los campos obligatorios (*)")
        return
    
    try:
        edad_int = int(edad)
        if edad_int < 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Valor inválido", "La edad debe ser un número entero positivo")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id FROM duenios
            WHERE LOWER(nombre) = LOWER(?) AND LOWER(apellido) = LOWER(?)
        """, (duenio_nombre, duenio_apellido))
        resultado = cursor.fetchone()

        if resultado:
            id_duenio = resultado[0]
        else:
            cursor.execute("INSERT INTO duenios (nombre, apellido) VALUES (?, ?)", (duenio_nombre, duenio_apellido))
            id_duenio = cursor.lastrowid

        cursor.execute("""
            INSERT INTO mascotas (nombre, especie, raza, edad, id_duenio)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, especie, raza, edad_int, id_duenio))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", f"Mascota '{nombre}' guardada correctamente.")

        entry_nombre.delete(0, tk.END)
        entry_especie.delete(0, tk.END)
        entry_raza.delete(0, tk.END)
        entry_edad.delete(0, tk.END)
        entry_duenio_nombre.delete(0, tk.END)
        entry_duenio_apellido.delete(0, tk.END)

        actualizar_mascotas()

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al guardar: {e}")

def eliminar_duenio():
    nombre = entry_duenio_nombre.get().strip()
    apellido = entry_duenio_apellido.get().strip()

    if not (nombre and apellido):
        messagebox.showwarning("Campos vacíos", "Completá nombre y apellido del dueño a eliminar.")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id FROM duenios
            WHERE LOWER(nombre) = LOWER(?) AND LOWER(apellido) = LOWER(?)
        """, (nombre, apellido))
        resultado = cursor.fetchone()

        if not resultado:
            messagebox.showinfo("No encontrado", "Ese dueño no está registrado.")
            conn.close()
            return

        id_duenio = resultado[0]
        cursor.execute("SELECT COUNT(*) FROM mascotas WHERE id_duenio = ?", (id_duenio,))
        cantidad = cursor.fetchone()[0]

        if cantidad > 0:
            messagebox.showerror("Error", "Este dueño tiene mascotas asociadas. Eliminá primero las mascotas antes de borrarlo.")
            conn.close()
            return

        cursor.execute("DELETE FROM duenios WHERE id = ?", (id_duenio,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Dueño eliminado correctamente.")

        #estas dos lineas son nuevas
        entry_duenio_nombre.delete(0, tk.END)
        entry_duenio_apellido.delete(0, tk.END)

        actualizar_mascotas()

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar: {e}")

        

      


def actualizar_mascotas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.id, m.nombre || ' (' || d.nombre || ' ' || IFNULL(d.apellido, '') || ')'
        FROM mascotas m
        JOIN duenios d ON m.id_duenio = d.id
    """)
    mascotas = cursor.fetchall()
    conn.close()

    mascota_map.clear()
    combo_mascotas['values'] = []
    for id_m, nombre in mascotas:
        mascota_map[nombre] = id_m
    combo_mascotas['values'] = list(mascota_map.keys())

def completar_datos_mascota(event):
    seleccion = combo_mascotas.get()
    if seleccion not in mascota_map:
        return
    id_mascota = mascota_map[seleccion]
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.nombre, m.especie, m.raza, m.edad, d.nombre || ' ' || IFNULL(d.apellido, '')
        FROM mascotas m
        JOIN duenios d ON m.id_duenio = d.id
        WHERE m.id = ?
    """, (id_mascota,))
    datos = cursor.fetchone()
    conn.close()

    if datos:
        entry_nombre2.config(state='normal')
        entry_nombre2.delete(0, tk.END)
        entry_nombre2.insert(0, datos[0])
        entry_nombre2.config(state='readonly')

        entry_especie2.config(state='normal')
        entry_especie2.delete(0, tk.END)
        entry_especie2.insert(0, datos[1])
        entry_especie2.config(state='readonly')

        entry_raza2.config(state='normal')
        entry_raza2.delete(0, tk.END)
        entry_raza2.insert(0, datos[2])
        entry_raza2.config(state='readonly')

        entry_edad2.config(state='normal')
        entry_edad2.delete(0, tk.END)
        entry_edad2.insert(0, str(datos[3]))
        entry_edad2.config(state='readonly')

        entry_duenio2.config(state='normal')
        entry_duenio2.delete(0, tk.END)
        entry_duenio2.insert(0, datos[4])
        entry_duenio2.config(state='readonly')

def eliminar_mascota():
    seleccion = combo_mascotas.get()
    if seleccion not in mascota_map:
        messagebox.showwarning("Atención", "Seleccioná una mascota para eliminar.")
        return

    id_mascota = mascota_map[seleccion]

    confirmacion = messagebox.askyesno("Confirmar", f"¿Seguro que querés eliminar a {seleccion}?")
    if not confirmacion:
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM mascotas WHERE id = ?", (id_mascota,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Mascota eliminada correctamente.")
        actualizar_mascotas()
        limpiar_campos_verificar_mascota()#linea nueva
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar la mascota: {e}")

#lineas nuevas para que, cuando se elimine la mascota, se limpien los campos
def limpiar_campos_verificar_mascota():
    entry_nombre2.config(state="normal")
    entry_nombre2.delete(0, tk.END)
    entry_nombre2.config(state="readonly")

    entry_especie2.config(state="normal")
    entry_especie2.delete(0, tk.END)
    entry_especie2.config(state="readonly")

    entry_raza2.config(state="normal")
    entry_raza2.delete(0, tk.END)
    entry_raza2.config(state="readonly")

    entry_edad2.config(state="normal")
    entry_edad2.delete(0, tk.END)
    entry_edad2.config(state="readonly")

    entry_duenio2.config(state="normal")
    entry_duenio2.delete(0, tk.END)
    entry_duenio2.config(state="readonly")

    combo_mascotas.set("")



    
    





def mostrar_duenios():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, apellido FROM duenios")
    duenios = [f"{n} {a}" for n, a in cursor.fetchall()]
    conn.close()
    mensaje = "\n".join(duenios) if duenios else "No hay dueños registrados."
    messagebox.showinfo("Dueños registrados", mensaje)


#notebook = ttk.Notebook(root)
#notebook.pack(pady=20, fill='both', expand=True)
    

# --- INTERFAZ ---
root = tk.Tk()
root.title("Formulario de Mascotas")
root.geometry("520x430")
root.config(bg="#e9d8a6")

# Estilo de las pestañas
style = ttk.Style()
style.theme_use("default")
style.configure("TNotebook", background="#e9d8a6", borderwidth=0)
style.configure("TNotebook.Tab", padding=[10, 5], background="white", borderwidth=1)
style.map("TNotebook.Tab",
          background=[("selected", "#cce5ff")],
          foreground=[("selected", "black")])


estilo_boton = {
    "bg": "white",
    "activebackground": "#3399ff",
    "fg": "black",
    "relief": "flat",
    "borderwidth": 0,
    "highlightthickness": 0,
    "font": ("Arial", 10, "bold"),
    "width": 20
}

# Frame contenedor para separar del borde
#frame_contenedor = tk.Frame(root, bg="#e9d8a6")
#frame_contenedor.pack(fill="both", expand=True, padx=10, pady=(5, 5))

#notebook = ttk.Notebook(frame_contenedor)
#notebook.pack(fill="both", expand=True)

# Frame contenedor centrado con fondo beige
frame_contenedor = tk.Frame(root, bg="#e9d8a6")
frame_contenedor.pack(fill="both", expand=True)

# Otro frame interno para centrar el notebook sin ocupar todo el ancho
#frame_interno = tk.Frame(frame_contenedor, bg="#e9d8a6")
#frame_interno.pack(pady=10)

# Notebook centrado
notebook = ttk.Notebook(frame_contenedor)
#notebook = ttk.Notebook(frame_contenedor)
#notebook.pack(pady=(0, 10))
#notebook.pack(padx=120, pady=20, fill="x", expand=False)

frame_notebook = tk.Frame(frame_contenedor, bg="#e9d8a6")
frame_notebook.pack(pady=(0, 0), padx=(30, 0))

notebook = ttk.Notebook(frame_notebook)
notebook.pack()

mascota_map = {}



# --- PESTAÑA 1: CARGAR MASCOTA ---
p1 = tk.Frame(notebook, bg="#e9d8a6")
notebook.add(p1, text="Cargar Mascota")

# Contenedor para centrar todo el contenido de la pestaña
p1_contenedor = tk.Frame(p1, bg="#e9d8a6")
p1_contenedor.pack(expand=True)

# Contenedor de los campos
form_frame = tk.Frame(p1_contenedor, bg="#e9d8a6")
form_frame.pack(pady=10)

labels = ["Nombre*", "Especie*", "Raza", "Edad*", "Nombre del dueño*", "Apellido del dueño*"]
entries = []
for i, label in enumerate(labels):
    tk.Label(form_frame, text=label, bg="#e9d8a6").grid(row=i, column=0, sticky="e", padx=10, pady=5)
    entry = tk.Entry(form_frame, width=30)
    entry.grid(row=i, column=1, padx=(10, 80), pady=5)
    entries.append(entry)

entry_nombre, entry_especie, entry_raza, entry_edad, entry_duenio_nombre, entry_duenio_apellido = entries



# Contenedor común para todos los botones (centrado)
botones_frame = tk.Frame(p1_contenedor, bg="#e9d8a6")
botones_frame.pack(pady=10)

# Botón "Guardar Mascota"
boton_guardar = tk.Button(botones_frame, text="Guardar Mascota", command=guardar_mascota, **estilo_boton)
boton_guardar.pack(pady=5, anchor="center")

# Botón "Eliminar Dueño"
boton_eliminar = tk.Button(botones_frame, text="Eliminar Dueño", command=eliminar_duenio, **estilo_boton)
boton_eliminar.pack(pady=5, anchor="center")

# Botón "Ver Dueños Registrados"
boton_ver = tk.Button(botones_frame, text="Ver Dueños Registrados", command=mostrar_duenios, **estilo_boton)
boton_ver.pack(pady=5, anchor="center")

# --- PESTAÑA 2: VERIFICAR MASCOTA ---
p2 = tk.Frame(notebook, bg="#e9d8a6")
notebook.add(p2, text="Verificar Mascotas")

style = ttk.Style()#nueva
style.theme_use('default')#nueva

#Configuracion base del combobox
style.configure("White.TCombobox", 
                fieldbackground="white", 
                background="white", 
                foreground="black",
                arrowcolor="#3399ff", 
                borderwidth=1)#nueva

style.map("WhiteBlue.TCombobox",
    fieldbackground=[("readonly", "white")],
    foreground=[("readonly", "black")],
    arrowcolor=[("active", "#3399ff"), ("readonly", "#3399ff")],
    background=[("readonly", "white"), ("active", "white"), ]
) #nuevo


tk.Label(p2, text="Seleccioná una mascota:", bg="#e9d8a6").grid(row=0, column=0, padx=10, pady=10, sticky="e")
combo_mascotas = ttk.Combobox(p2, state="readonly", style="WhiteBlue.TCombobox")#nuevo antes de readonly
combo_mascotas.grid(row=0, column=1, padx=(10, 80), pady=10)
combo_mascotas.bind("<<ComboboxSelected>>", completar_datos_mascota)

labels2 = ["Nombre", "Especie", "Raza", "Edad", "Dueño"]
entries2 = []

for i, label in enumerate(labels2):
    tk.Label(p2, text=label, bg="#e9d8a6").grid(row=i+1, column=0, sticky="e", padx=5, pady=5)
    entry = tk.Entry(p2, state="readonly", bg="white", readonlybackground="white")
    entry.grid(row=i+1, column=1, padx=(10, 80), pady=5)
    entries2.append(entry)

entry_nombre2, entry_especie2, entry_raza2, entry_edad2, entry_duenio2 = entries2

tk.Button(p2, text="Eliminar Mascota", command=eliminar_mascota,
          
          bg="#e9d8a6", relief="flat", borderwidth=0, highlightthickness=0).grid(row=7, column=0, columnspan=2, pady=(30, 10))

#linea nueva
def cerrar_ventana():
    root.destroy()

# Botón "Cerrar"
boton_cerrar = tk.Button(botones_frame, text="Cerrar", command=cerrar_ventana, **estilo_boton)
boton_cerrar.config(width=12)
boton_cerrar.pack(pady=5, anchor="center")



actualizar_mascotas()
root.mainloop()
