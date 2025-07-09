import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_PATH = "mascotas.db"

def cargar_especialidades():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM especialidades ORDER BY nombre")
        especialidades = [row[0] for row in cursor.fetchall()]
        conn.close()
        return especialidades
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar las especialidades: {e}")
        return []

def actualizar_estado():
    if activo_var.get() == 1:
        label_estado.config(text="")
    else:
        label_estado.config(text="Veterinario inactivo", fg="red")

def guardar_veterinario():
    nombre = entry_nombre.get().strip()
    apellido = entry_apellido.get().strip()
    telefono = entry_telefono.get().strip()
    matricula = entry_matricula.get().strip()
    especialidad = combo_especialidad.get()
    activo = activo_var.get()

    if not nombre or not apellido or not especialidad:
        messagebox.showwarning("Campos incompletos", "Por favor completá nombre, apellido y especialidad.")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
         
        cursor.execute("SELECT id FROM especialidades WHERE nombre = ?", (especialidad,))
        resultado = cursor.fetchone()
        if resultado:
            id_especialidad = resultado[0]
        else:
            messagebox.showerror("Error", "La especialidad seleccionada no existe.")
            return

        cursor.execute("""
            INSERT INTO veterinarios (nombre, apellido, telefono, matricula, id_especialidad, activo)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre, apellido, telefono, matricula, id_especialidad, activo))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Veterinario guardado correctamente.")

        # ✅ Limpiar los campos luego del guardado
        entry_nombre.delete(0, tk.END)
        entry_apellido.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)
        entry_matricula.delete(0, tk.END)
        combo_especialidad.set('')  # Limpia el combobox
        activo_var.set(1)  # Por defecto lo vuelve a marcar como activo
        #actualizar_estado()  # Actualiza el texto dinámico a "Veterinario activo"

        #ventana.destroy()
    except Exception as e:
        messagebox.showerror("Error al guardar", str(e))


ventana = tk.Tk()
ventana.title("Cargar Veterinario Nuevo")
ventana.geometry("450x480")  # un poco más alta para ajustar todo
ventana.configure(bg="#e9d8a6")

label_font = ("Segoe UI", 11, "bold")
entry_font = ("Segoe UI", 11)
label_fg = "#3b2f2f"
entry_bg = "#f0faff"
entry_border = "#87cefa"
combo_font = ("Segoe UI", 11)

style = ttk.Style()
style.theme_use('default')
style.configure("White.TCombobox", 
                fieldbackground="white", 
                background="white", 
                foreground="black",
                arrowcolor="#3399ff", 
                borderwidth=1)
style.map("WhiteBlue.TCombobox",
    fieldbackground=[("readonly", "white")],
    foreground=[("readonly", "black"), ("selected", "black")],
    arrowcolor=[("active", "#3399ff"), ("readonly", "#3399ff")],
    background=[("readonly", "white"), ("active", "white"), ("selected", "white")]
)



combo_especialidad = ttk.Combobox(ventana, values=cargar_especialidades(),
                                  state="readonly", width=26, font=combo_font,
                                  style="Custom.TCombobox")

tk.Label(ventana, text="Nombre:", bg="#e9d8a6", fg=label_fg, font=label_font, width=12, anchor="e").grid(row=0, column=0, padx=0, pady=(25,6))
entry_nombre = ttk.Entry(ventana, width=28, font=entry_font, style="Celeste.TEntry")
entry_nombre.grid(row=0, column=1, sticky="w", padx=50, pady=(25,6))

tk.Label(ventana, text="Apellido:", bg="#e9d8a6", fg=label_fg, font=label_font).grid(row=1, column=0, sticky="e", padx=0, pady=6)
entry_apellido = ttk.Entry(ventana, width=28, font=entry_font, style="Celeste.TEntry")
entry_apellido.grid(row=1, column=1, sticky="w", padx=50, pady=6)

tk.Label(ventana, text="Teléfono:", bg="#e9d8a6", fg=label_fg, font=label_font).grid(row=2, column=0, sticky="e", padx=0, pady=6)
entry_telefono = ttk.Entry(ventana, width=28, font=entry_font, style="Celeste.TEntry")
entry_telefono.grid(row=2, column=1, sticky="w", padx=50, pady=6)

tk.Label(ventana, text="Matrícula:", bg="#e9d8a6", fg=label_fg, font=label_font).grid(row=3, column=0, sticky="e", padx=0, pady=6)
entry_matricula = ttk.Entry(ventana, width=28, font=entry_font, style="Celeste.TEntry")
entry_matricula.grid(row=3, column=1, sticky="w", padx=50, pady=6)

tk.Label(ventana, text="Especialidad:", bg="#e9d8a6", fg=label_fg, font=label_font).grid(row=4, column=0, sticky="e", padx=0, pady=6)
combo_especialidad = ttk.Combobox(ventana, values=cargar_especialidades(), state="readonly", width=26, font=combo_font, style="WhiteBlue.TCombobox")
combo_especialidad.grid(row=4, column=1, sticky="w", padx=50, pady=6)

activo_var = tk.IntVar(value=1)
check_activo = tk.Checkbutton(ventana, text="Veterinario activo", variable=activo_var,
                               bg="#e9d8a6", fg="#007f00", font=label_font,
                               selectcolor="#d0ffd0", activebackground="#e9d8a6",
                               activeforeground="#007f00", command=actualizar_estado)
check_activo.grid(row=5, column=1, sticky="w", padx=50, pady=(10,15))

label_estado = tk.Label(ventana, text="", bg="#e9d8a6", fg="green", font=("Segoe UI", 11, "bold"))
label_estado.grid(row=6, column=1, sticky="w", padx=50, pady=(4, 6))

actualizar_estado()

estilo_boton_guardar = {
    "bg": "white",  
    "activebackground": "#3399ff",  
    "fg": "black",
    "relief": "flat",
    "borderwidth": 0,
    "highlightthickness": 0,
    "font": ("Arial", 10, "bold"),
    "width": 10
}

boton_guardar = tk.Button(ventana, text="Guardar", command=guardar_veterinario, **estilo_boton_guardar)
boton_guardar.grid(row=7, column=1, sticky="w", padx=70, pady=(30, 5))

def cerrar_ventana():
    ventana.destroy()

estilo_boton_cerrar = {
    "bg": "white",
    "activebackground": "#3399ff",
    "fg": "black",
    "relief": "flat",
    "borderwidth": 0,
    "highlightthickness": 0,
    "font": ("Arial", 10, "bold"),
    "width": 10
}

boton_cerrar = tk.Button(ventana, text="Cerrar", command=cerrar_ventana, **estilo_boton_cerrar)
boton_cerrar.grid(row=8, column=1, sticky="w", padx=70, pady=(20, 15))

ventana.mainloop()