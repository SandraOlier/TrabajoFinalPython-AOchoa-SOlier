import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_PATH = 'mascotas.db'
lista_veterinarios_completa = []

def cargar_veterinarios():
    global lista_veterinarios_completa
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.id, v.nombre, v.apellido, v.telefono, e.nombre, v.activo
            FROM veterinarios v
            LEFT JOIN especialidades e ON v.id_especialidad = e.id
            ORDER BY v.nombre, v.apellido
        """)
        resultado = cursor.fetchall()
        conn.close()
        lista_veterinarios_completa = resultado
        return [f"{row[1]} {row[2]}" for row in resultado if row[5] == 1]
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los veterinarios: {e}")
        return []

def cargar_datos_veterinario(event):
    seleccion = combo_veterinarios.get()
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    label_especialidad_texto.set("Especialidad:")
    label_estado.config(text="", fg="black")

    for v in lista_veterinarios_completa:
        nombre_completo = f"{v[1]} {v[2]}"
        if seleccion == nombre_completo:
            entry_nombre.insert(0, v[1])
            entry_apellido.insert(0, v[2])
            entry_telefono.insert(0, v[3] if v[3] else "")
            label_especialidad_texto.set(v[4] if v[4] else "No asignada")
            if v[5] == 1:
                label_estado.config(text="Veterinario ACTIVO ✅", fg="green")
            else:
                label_estado.config(text="Veterinario INACTIVO ❌", fg="red")
            break

def cerrar_ventana():
    ventana.destroy()

# ---- INTERFAZ TKINTER ----
ventana = tk.Tk()
ventana.title("Formulario Veterinarios")
ventana.geometry("440x400")
ventana.configure(bg="#e9d8a6")

# Estilos
label_font = ("Segoe UI", 11, "bold")
entry_font = ("Segoe UI", 11)
label_fg = "#3b2f2f"
entry_bg = "#f0faff"
entry_border = "#87cefa"
combo_font = ("Segoe UI", 11)

# Estilo para los Entry
style = ttk.Style()
style.theme_use('default')
style.configure("Celeste.TEntry",
                fieldbackground=entry_bg,
                bordercolor=entry_border,
                lightcolor=entry_border,
                borderwidth=1)

# Estilo botón redondeado
style.configure("Rounded.TButton",
                font=("Segoe UI", 11, "bold"),
                background="white",
                foreground="black",
                borderwidth=0,
                focusthickness=0,
                relief="flat")

# Combo Veterinarios
tk.Label(ventana, text="Veterinarios:", bg="#e9d8a6", fg=label_fg, font=label_font).grid(row=0, column=0, sticky="e", padx=10, pady=(40, 10))
combo_veterinarios = ttk.Combobox(ventana, values=cargar_veterinarios(), state="readonly", width=28, font=combo_font)
combo_veterinarios.grid(row=0, column=1, sticky="w", padx=10, pady=(40, 10))
combo_veterinarios.set('')
combo_veterinarios.bind("<<ComboboxSelected>>", cargar_datos_veterinario)

# Nombre
tk.Label(ventana, text="Nombre:", bg="#e9d8a6", fg=label_fg, font=label_font).grid(row=1, column=0, sticky="e", padx=10, pady=6)
entry_nombre = ttk.Entry(ventana, width=28, font=entry_font, style="Celeste.TEntry")
entry_nombre.grid(row=1, column=1, sticky="w", padx=10, pady=6)

# Apellido
tk.Label(ventana, text="Apellido:", bg="#e9d8a6", fg=label_fg, font=label_font).grid(row=2, column=0, sticky="e", padx=10, pady=6)
entry_apellido = ttk.Entry(ventana, width=28, font=entry_font, style="Celeste.TEntry")
entry_apellido.grid(row=2, column=1, sticky="w", padx=10, pady=6)

# Teléfono
tk.Label(ventana, text="Teléfono:", bg="#e9d8a6", fg=label_fg, font=label_font).grid(row=3, column=0, sticky="e", padx=10, pady=6)
entry_telefono = ttk.Entry(ventana, width=28, font=entry_font, style="Celeste.TEntry")
entry_telefono.grid(row=3, column=1, sticky="w", padx=10, pady=6)

# Especialidad (label dinámico)
#comento estas 4 lineas, debo probar otra cosa
#label_especialidad_texto = tk.StringVar()
#label_especialidad_texto.set("Especialidad:")
#label_especialidad = tk.Label(ventana, textvariable=label_especialidad_texto, bg="#e9d8a6", fg="black", font=("Segoe UI", 11, "italic"))
#label_especialidad.grid(row=4, column=0, columnspan=2, sticky="w", padx=20, pady=(12, 6))
# Etiqueta estática "Especialidad:"
tk.Label(ventana, text="Especialidad:", bg="#e9d8a6", fg="black", font=("Segoe UI", 11, "italic")).grid(row=4, column=0, sticky="e", padx=(10, 5), pady=(12, 6))

# Etiqueta dinámica solo para el nombre de la especialidad
label_especialidad_texto = tk.StringVar()
label_especialidad_texto.set("No asignada")
label_especialidad = tk.Label(ventana, textvariable=label_especialidad_texto, bg="#e9d8a6", fg="black", font=("Segoe UI", 11, "italic"))
label_especialidad.grid(row=4, column=1, sticky="w", padx=(0, 10), pady=(12, 6))

# Veterinario activo
label_estado = tk.Label(ventana, text="", bg="#e9d8a6", font=("Segoe UI", 11, "bold"))
label_estado.grid(row=5, column=0, columnspan=2, pady=(4, 10))

# Botón cerrar
boton_cerrar = ttk.Button(
    ventana,
    text="Cerrar",
    command=cerrar_ventana,
    style="Rounded.TButton"
)
boton_cerrar.grid(row=6, column=0, columnspan=2, pady=15, padx=(100, 0))

ventana.mainloop()
