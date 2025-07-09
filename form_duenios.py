import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

DB_PATH = "mascotas.db"

def cargar_duenios():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, apellido, telefono FROM duenios")
        resultados = cursor.fetchall()
        conn.close()
        # Formateamos la lista para mostrar en el combobox, con nombre, apellido y telefono
        return [f"{nombre} {apellido} | {telefono}" for nombre, apellido, telefono in resultados]
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los dueños: {e}")
        return []

def guardar_duenio():
    nombre = entry_nombre.get().strip()
    apellido = entry_apellido.get().strip()
    telefono = entry_telefono.get().strip()
    email = entry_email.get().strip()
    direccion = entry_direccion.get().strip()
    ciudad = entry_ciudad.get().strip()

    if not nombre:
        messagebox.showwarning("Falta nombre", "El campo nombre es obligatorio.")
        return
    if not apellido:
        messagebox.showwarning("Falta apellido", "El campo apellido es obligatorio.")
        return
    if not telefono:
        messagebox.showwarning("Falta teléfono", "El campo teléfono es obligatorio.")
        return
    if not (email and direccion and ciudad):
        messagebox.showwarning("Campos vacíos", "Completá todos los campos.")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO duenios (nombre, apellido, telefono, email, direccion, ciudad)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre, apellido, telefono, email, direccion, ciudad))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Dueño guardado correctamente")

        entry_nombre.delete(0, tk.END)
        entry_apellido.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_direccion.delete(0, tk.END)
        entry_ciudad.delete(0, tk.END)

        combo_duenios['values'] = cargar_duenios()

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Ventana principal
ventana = tk.Tk()
ventana.title("Formulario Dueños")
ventana.geometry("480x550")

# Configurar color de fondo igual que la ventana principal
ventana.config(bg="#e9d8a6")

# Estilo para Entry sin borde externo blanco y altura uniforme
style = ttk.Style()
#style.theme_use("default")


# En un momento pensamos en personalizar el estilo del Combobox para que se viera 
# más integrado con el diseño del formulario (colores, bordes, flecha, etc.).
# Probamos varias configuraciones, pero después decidimos dejar el estilo por defecto 
# porque se ve bien en todos los sistemas y evitamos complicaciones.
# Por eso este bloque lo dejamos comentado.

# Crear un estilo personalizado para el Combobox
#style.configure("Custom.TCombobox",
                #fieldbackground="white",  # fondo caja texto
                #background="white",       # fondo general
                #bordercolor="white",      # borde blanco (o el mismo que fondo)
                #lightcolor="white",       # borde claro para foco
                #darkcolor="white",        # borde oscuro para foco
                #arrowcolor="blue")        # flecha azul sistema

# Opcional: aplicar mapeos para estados (hover, focus, etc)
#style.map("Custom.TCombobox",
          #fieldbackground=[('readonly', 'white')],
          #background=[('readonly', 'white')],
          #arrowcolor=[('active', 'blue'), ('!disabled', 'blue')],
          #foreground=[('readonly', 'black')],
          #selectbackground=[('readonly', '#f0f0f0')],
          #selectforeground=[('readonly', 'black')])


# Estilo común para botones
estilo_boton = {
    "bg": "#a7d3f5",
    "activebackground": "#90c2eb",
    "fg": "black",
    "relief": "flat",
    "borderwidth": 0,
    "highlightthickness": 0,
    "font": ("Arial", 10, "bold"),
    "width": 20
}

# Etiqueta
tk.Label(ventana, text="Nombre:", bg="#e9d8a6").grid(row=0, column=0, sticky="e", padx=(15, 5), pady=(20, 5))
# Campo de entrada sin borde exterior blanco, fondo blanco interior
entry_nombre = tk.Entry(ventana, bg="white", relief="flat", highlightthickness=0, bd=1)
entry_nombre.grid(row=0, column=1, padx=(0, 100), pady=(20, 5), ipady=4)

# Etiquetas y campos con fondo beige uniforme y campos sin borde blanco exterior, altura uniforme

tk.Label(ventana, text="Apellido:", bg="#e9d8a6").grid(row=1, column=0, sticky="e", padx=(15, 5), pady=5)
entry_apellido = tk.Entry(ventana, bg="white", relief="flat", highlightthickness=0, bd=1)
entry_apellido.grid(row=1, column=1, padx=(0, 100), pady=5, ipady=4)

tk.Label(ventana, text="Teléfono:", bg="#e9d8a6").grid(row=2, column=0, sticky="e", padx=(15, 5), pady=5)
entry_telefono = tk.Entry(ventana, bg="white", relief="flat", highlightthickness=0, bd=1)
entry_telefono.grid(row=2, column=1, padx=(0, 100), pady=5, ipady=4)

tk.Label(ventana, text="Email:", bg="#e9d8a6").grid(row=3, column=0, sticky="e", padx=(15, 5), pady=5)
entry_email = tk.Entry(ventana, bg="white", relief="flat", highlightthickness=0, bd=1)
entry_email.grid(row=3, column=1, padx=(0, 100), pady=5, ipady=4)

tk.Label(ventana, text="Dirección:", bg="#e9d8a6").grid(row=4, column=0, sticky="e", padx=(15, 5), pady=5)
entry_direccion = tk.Entry(ventana, bg="white", relief="flat", highlightthickness=0, bd=1)
entry_direccion.grid(row=4, column=1, padx=(0, 100), pady=5, ipady=4)

tk.Label(ventana, text="Ciudad:", bg="#e9d8a6").grid(row=5, column=0, sticky="e", padx=(15, 5), pady=5)
entry_ciudad = tk.Entry(ventana, bg="white", relief="flat", highlightthickness=0, bd=1)
entry_ciudad.grid(row=5, column=1, padx=(0, 100), pady=5, ipady=4)
frame_guardar = tk.Frame(ventana, bg="#e9d8a6")
frame_guardar.grid(row=6, column=0, columnspan=2, pady=15, padx=(50, 0))
boton_guardar = tk.Button(frame_guardar, text="Guardar Dueño", command=guardar_duenio, **estilo_boton)
boton_guardar.pack()



def eliminar_duenio():
    dueño = combo_duenios.get()
    if not dueño:
        messagebox.showwarning("Atención", "Seleccioná un dueño para eliminar.")
        return

    try:
        nombre_apellido, telefono = dueño.split(" | ")
        nombre, apellido = nombre_apellido.split(" ", 1)
    except ValueError:
        messagebox.showerror("Error", "Formato de dueño inválido.")
        return

    print("Intentando eliminar dueño:")
    print("Nombre:", nombre)
    print("Apellido:", apellido)
    print("Teléfono:", telefono)

    try:
        conn = sqlite3.connect("mascotas.db")
        cursor = conn.cursor()

        # Verificamos si el dueño existe antes de eliminar
        cursor.execute("SELECT * FROM duenios WHERE nombre = ? AND apellido = ? AND telefono = ?", (nombre, apellido, telefono))
        resultado = cursor.fetchone()
        print("Resultado de búsqueda en BD antes de borrar:", resultado)

        if resultado:
            cursor.execute("DELETE FROM duenios WHERE nombre = ? AND apellido = ? AND telefono = ?", (nombre, apellido, telefono))
            conn.commit()
            messagebox.showinfo("Éxito", f"Dueño '{dueño}' eliminado correctamente.")
            combo_duenios['values'] = cargar_duenios()
            combo_duenios.set("")
        else:
            messagebox.showwarning("No encontrado", "No se encontró un dueño con esos datos. No se eliminó nada.")

        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el dueño: {e}")



# Etiqueta y Combobox con estilo aplicado
tk.Label(ventana, text="Dueños registrados:", bg="#e9d8a6").grid(row=7, column=0, sticky="e", padx=5, pady=5)
combo_duenios = ttk.Combobox(ventana, values=cargar_duenios(), state="readonly", width=30)
combo_duenios.grid(row=7, column=1, padx=5, pady=5)



def cargar_datos_seleccion(event):
    seleccionado = combo_duenios.get()
    if not seleccionado:
        return
    
    try:
        #nombre, apellido, telefono = seleccionado.split(" ", 2)# linea reempazada por las dos de abajo
        nombre_apellido, telefono = seleccionado.split(" | ")#linea nueva
        nombre, apellido = nombre_apellido.split(" ", 1)#linea nueva
    except ValueError:
        messagebox.showerror("Error", "Formato de dueño inválido.")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nombre, apellido, telefono, email, direccion, ciudad
            FROM duenios
            WHERE nombre = ? AND apellido = ? AND telefono = ?
        """, (nombre, apellido, telefono))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            entry_nombre.delete(0, tk.END)
            entry_nombre.insert(0, resultado[0])
            entry_apellido.delete(0, tk.END)
            entry_apellido.insert(0, resultado[1])
            entry_telefono.delete(0, tk.END)
            entry_telefono.insert(0, resultado[2])
            entry_email.delete(0, tk.END)
            entry_email.insert(0, resultado[3])
            entry_direccion.delete(0, tk.END)
            entry_direccion.insert(0, resultado[4])
            entry_ciudad.delete(0, tk.END)
            entry_ciudad.insert(0, resultado[5])
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la información: {e}")

combo_duenios.bind("<<ComboboxSelected>>", cargar_datos_seleccion)

def eliminar_duenio():
    dueño = combo_duenios.get()
    if not dueño:
        messagebox.showwarning("Atención", "Seleccioná un dueño para eliminar.")
        return

    try:
        nombre_apellido, telefono = dueño.split(" | ")
        nombre, apellido = nombre_apellido.split(" ", 1)
    except ValueError:
        messagebox.showerror("Error", "Formato de dueño inválido.")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM duenios WHERE nombre = ? AND apellido = ? AND telefono = ?",
                       (nombre, apellido, telefono))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", f"Dueño '{dueño}' eliminado correctamente.")
        combo_duenios['values'] = cargar_duenios()
        combo_duenios.set("")

        entry_nombre.delete(0, tk.END)
        entry_apellido.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_direccion.delete(0, tk.END)
        entry_ciudad.delete(0, tk.END)


    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el dueño: {e}")

frame_eliminar = tk.Frame(ventana, bg="#e9d8a6")
frame_eliminar.grid(row=8, column=0, columnspan=2, pady=5, padx=(50, 0))
boton_eliminar = tk.Button(frame_eliminar, text="Eliminar Dueño", command=eliminar_duenio, **estilo_boton)
boton_eliminar.pack()

def modificar_dueño():
    seleccionado = combo_duenios.get()
    if not seleccionado:
        messagebox.showwarning("Atención", "Seleccioná un dueño para modificar.")
        return

    try:
        nombre_apellido, telefono_orig = seleccionado.split(" | ")
        nombre_orig, apellido_orig = nombre_apellido.split(" ", 1)
    except ValueError:
        messagebox.showerror("Error", "Formato de dueño inválido.")
        return

    nombre_nuevo = entry_nombre.get().strip()
    apellido_nuevo = entry_apellido.get().strip()
    telefono_nuevo = entry_telefono.get().strip()
    email_nuevo = entry_email.get().strip()
    direccion_nueva = entry_direccion.get().strip()
    ciudad_nueva = entry_ciudad.get().strip()

    if not nombre_nuevo or not apellido_nuevo or not telefono_nuevo:
        messagebox.showwarning("Faltan datos", "Nombre, apellido y teléfono son obligatorios.")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE duenios
            SET nombre = ?, apellido = ?, telefono = ?, email = ?, direccion = ?, ciudad = ?
            WHERE nombre = ? AND apellido = ? AND telefono = ?
        """, (nombre_nuevo, apellido_nuevo, telefono_nuevo, email_nuevo, direccion_nueva, ciudad_nueva,
              nombre_orig, apellido_orig, telefono_orig))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Datos modificados correctamente.")
        combo_duenios['values'] = cargar_duenios()
        combo_duenios.set(f"{nombre_nuevo} {apellido_nuevo} | {telefono_nuevo}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo modificar el dueño: {e}")

frame_modificar = tk.Frame(ventana, bg="#e9d8a6")
frame_modificar.grid(row=9, column=0, columnspan=2, pady=10, padx=(50, 0))
boton_modificar = tk.Button(frame_modificar, text="Modificar Dueño", command=modificar_dueño, **estilo_boton)
boton_modificar.pack()


#nuevas lineas de codigo
def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_direccion.delete(0, tk.END)
    entry_ciudad.delete(0, tk.END)


# ---------------------------------------------------------------
# FUNCIONALIDAD DE BÚSQUEDA DE DUEÑOS
#
# El campo "Buscar dueño" permite filtrar los valores que se ven 
# en el Combobox "Dueños registrados". Al escribir parte del nombre, 
# apellido o teléfono, se muestran solo las coincidencias.
#
# IMPORTANTE:
# - Esta búsqueda no completa automáticamente los campos del formulario.
# - El usuario debe seleccionar una opción del combobox manualmente.
# - Una vez seleccionada, los datos se cargan automáticamente.
#
# Esto se hizo así para evitar errores de coincidencia y permitir
# que el usuario confirme cuál registro desea consultar/modificar.
# ---------------------------------------------------------------


def buscar_duenio():
    termino = entry_busqueda.get().strip().lower()
    if not termino:
        combo_duenios['values'] = cargar_duenios()
        combo_duenios.set('')
        limpiar_campos()
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, apellido, telefono FROM duenios")
        resultados = cursor.fetchall()
        conn.close()

        filtrados = []
        for nombre, apellido, telefono in resultados:
            texto_completo = f"{nombre} {apellido} {telefono}".lower()
            if termino in texto_completo:
                filtrados.append(f"{nombre} {apellido} | {telefono}")

        if filtrados:
            combo_duenios['values'] = filtrados
            combo_duenios.set('')#agregado nuevo
        else:
            messagebox.showinfo("Sin resultados", "No se encontraron coincidencias.")
            combo_duenios['values'] = []
            combo_duenios.set('')
            limpiar_campos()

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo realizar la búsqueda: {e}")

#nueva linea 
def limpiar_busqueda():
    entry_busqueda.delete(0, tk.END)
    combo_duenios['values'] = cargar_duenios()
    combo_duenios.set('')
    limpiar_campos()



tk.Label(ventana, text="Buscar dueño:", bg="#e9d8a6").grid(row=10, column=0, sticky="e", padx=5, pady=(10, 5))
entry_busqueda = tk.Entry(ventana, width=30)
entry_busqueda.grid(row=10, column=1, padx=5, pady=(10, 5), sticky="w")
entry_busqueda.bind("<KeyRelease>", lambda event: buscar_duenio())#nuevo

#nueva linea
# Fila nueva para el botón "Limpiar", debajo
boton_limpiar = tk.Button(ventana, text="Limpiar datos de busqueda", command=limpiar_busqueda, **{**estilo_boton, "width": 22})
boton_limpiar.grid(row=11, column=0, columnspan=2,  pady=(0, 15), padx=(50, 0))


#Funcion para cerrar ventana
def cerrar_ventana():
    ventana.destroy()  # Cierra la ventana actual

# Botón Cerrar
boton_cerrar = tk.Button(ventana, text="Cerrar", command=cerrar_ventana, **{**estilo_boton, "width": 18})
boton_cerrar.grid(row=12, column=0, columnspan=2, pady=(20, 15), padx=(50, 0))

#Version anterior con boton de busqueda manual
#frame_buscar = tk.Frame(ventana, bg="#e9d8a6")
#frame_buscar.grid(row=11, column=0, columnspan=2, pady=10, padx=(50, 0)) 
#boton_buscar = tk.Button(frame_buscar, text="Buscar", command=buscar_duenio, **estilo_boton)
#boton_buscar.pack()
# NOTA: Esta parte fue reemplazada por busqueda automatica al escribir en el campo


#ventana.mainloop()
if __name__ == "__main__":
    ventana.mainloop()







