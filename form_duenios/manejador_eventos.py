#Funciones que se usan para guardar dueño, eliminar, modificar, buscar(llaman a las funciones de datos.py)

import tkinter as tk
from tkinter import messagebox
from form_duenios import base_datos

def inicializar_formulario(ventana, widgets):
    # Cargar combo al iniciar
    widgets["combo_duenios"]['values'] = base_datos.cargar_duenios()

def limpiar_campos(entries):
    for entry in entries.values():
        entry.delete(0, tk.END)

def guardar(widgets):
    entries = widgets["entries"]
    nombre = entries["nombre"].get().strip()
    apellido = entries["apellido"].get().strip()
    telefono = entries["telefono"].get().strip()
    email = entries["email"].get().strip()
    direccion = entries["dirección"].get().strip()
    ciudad = entries["ciudad"].get().strip()

    if base_datos.guardar_duenio(nombre, apellido, telefono, email, direccion, ciudad):
        messagebox.showinfo("Éxito", "Dueño guardado correctamente")
        limpiar_campos(entries)
        widgets["combo_duenios"]['values'] = base_datos.cargar_duenios()

def eliminar(widgets):
    dueño = widgets["combo_duenios"].get()
    if not dueño:
        messagebox.showwarning("Atención", "Seleccioná un dueño para eliminar.")
        return
    try:
        nombre, apellido, telefono = dueño.split(" ", 2)
    except ValueError:
        messagebox.showerror("Error", "Formato de dueño inválido.")
        return
    if base_datos.eliminar_duenio(nombre, apellido, telefono):
        messagebox.showinfo("Éxito", f"Dueño '{dueño}' eliminado correctamente.")
        widgets["combo_duenios"]['values'] = base_datos.cargar_duenios()
        widgets["combo_duenios"].set("")

def modificar(widgets):
    seleccionado = widgets["combo_duenios"].get()
    if not seleccionado:
        messagebox.showwarning("Atención", "Seleccioná un dueño para modificar.")
        return
    try:
        nombre_apellido, telefono_orig = seleccionado.split(" | ")
        nombre_orig, apellido_orig = nombre_apellido.split(" ", 1)
    except ValueError:
        messagebox.showerror("Error", "Formato de dueño inválido.")
        return

    entries = widgets["entries"]
    nombre_nuevo = entries["nombre"].get().strip()
    apellido_nuevo = entries["apellido"].get().strip()
    telefono_nuevo = entries["telefono"].get().strip()
    email_nuevo = entries["email"].get().strip()
    direccion_nueva = entries["dirección"].get().strip()
    ciudad_nueva = entries["ciudad"].get().strip()

    if not nombre_nuevo or not apellido_nuevo or not telefono_nuevo:
        messagebox.showwarning("Faltan datos", "Nombre, apellido y teléfono son obligatorios.")
        return

    if base_datos.modificar_duenio(nombre_nuevo, apellido_nuevo, telefono_nuevo, email_nuevo, direccion_nueva, ciudad_nueva,
                                  nombre_orig, apellido_orig, telefono_orig):
        messagebox.showinfo("Éxito", "Datos modificados correctamente.")
        widgets["combo_duenios"]['values'] = base_datos.cargar_duenios()
        widgets["combo_duenios"].set(f"{nombre_nuevo} {apellido_nuevo} | {telefono_nuevo}")

def cargar_datos(event, widgets):
    seleccionado = widgets["combo_duenios"].get()
    if not seleccionado:
        return
    try:
        nombre, apellido, telefono = seleccionado.split(" ", 2)
    except ValueError:
        messagebox.showerror("Error", "Formato de dueño inválido.")
        return

    try:
        conn = base_datos.sqlite3.connect(base_datos.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nombre, apellido, telefono, email, direccion, ciudad
            FROM duenios
            WHERE nombre = ? AND apellido = ? AND telefono = ?
        """, (nombre, apellido, telefono))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            entries = widgets["entries"]
            entries["nombre"].delete(0, tk.END)
            entries["nombre"].insert(0, resultado[0])
            entries["apellido"].delete(0, tk.END)
            entries["apellido"].insert(0, resultado[1])
            entries["telefono"].delete(0, tk.END)
            entries["telefono"].insert(0, resultado[2])
            entries["email"].delete(0, tk.END)
            entries["email"].insert(0, resultado[3])
            entries["dirección"].delete(0, tk.END)
            entries["dirección"].insert(0, resultado[4])
            entries["ciudad"].delete(0, tk.END)
            entries["ciudad"].insert(0, resultado[5])
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la información: {e}")

def buscar(widgets):
    termino = widgets["entry_busqueda"].get().strip()
    if not termino:
        widgets["combo_duenios"]['values'] = base_datos.cargar_duenios()
        return
    filtrados = base_datos.buscar_duenios_por_termino(termino)
    if filtrados:
        widgets["combo_duenios"]['values'] = filtrados
    else:
        messagebox.showinfo("Sin resultados", "No se encontraron coincidencias.")

def conectar_eventos(widgets):
    widgets["boton_guardar"].config(command=lambda: guardar(widgets))
    widgets["boton_eliminar"].config(command=lambda: eliminar(widgets))
    widgets["boton_modificar"].config(command=lambda: modificar(widgets))
    widgets["combo_duenios"].bind("<<ComboboxSelected>>", lambda e: cargar_datos(e, widgets))
    widgets["boton_buscar"].config(command=lambda: buscar(widgets))