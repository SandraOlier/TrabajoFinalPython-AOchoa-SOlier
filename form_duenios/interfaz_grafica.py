#Codigo que crea el formulario, los widgets(labels,entries,botones), los empaqueta y configura layouts, bindings, estilos.

import tkinter as tk
from tkinter import ttk

def crear_ventana_formulario():
    ventana = tk.Tk()
    ventana.title("Formulario Dueños")
    ventana.geometry("480x500")

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

    # Labels y Entries
    etiquetas = ["Nombre:", "Apellido:", "Teléfono:", "Email:", "Dirección:", "Ciudad:"]
    entries = {}

    for i, texto in enumerate(etiquetas):
        tk.Label(ventana, text=texto).grid(row=i, column=0, sticky="e", padx=5, pady=5)
        entry = tk.Entry(ventana)
        entry.grid(row=i, column=1)
        entries[texto[:-1].lower()] = entry  # clave: nombre, apellido, etc.

    # Botón Guardar (en frame para centrar)
    frame_guardar = tk.Frame(ventana)
    frame_guardar.grid(row=6, column=0, columnspan=2, pady=15)
    boton_guardar = tk.Button(frame_guardar, text="Guardar Dueño", **estilo_boton)
    boton_guardar.pack()

    # Combo Dueños Registrados
    tk.Label(ventana, text="Dueños registrados:").grid(row=7, column=0, sticky="e", padx=5, pady=5)
    combo_duenios = ttk.Combobox(ventana, values=[], state="readonly", width=30)
    combo_duenios.grid(row=7, column=1, padx=5, pady=5)

    # Botones Eliminar y Modificar (en frames para centrar)
    frame_eliminar = tk.Frame(ventana)
    frame_eliminar.grid(row=8, column=0, columnspan=2, pady=5)
    boton_eliminar = tk.Button(frame_eliminar, text="Eliminar Dueño", **estilo_boton)
    boton_eliminar.pack()

    frame_modificar = tk.Frame(ventana)
    frame_modificar.grid(row=9, column=0, columnspan=2, pady=10)
    boton_modificar = tk.Button(frame_modificar, text="Modificar Dueño", **estilo_boton)
    boton_modificar.pack()

    # Campo Buscar Dueño
    tk.Label(ventana, text="Buscar dueño:").grid(row=10, column=0, sticky="e", padx=5, pady=5)
    entry_busqueda = tk.Entry(ventana, width=30)
    entry_busqueda.grid(row=10, column=1, padx=5, pady=5)

    # Botón Buscar (en frame para centrar)
    frame_buscar = tk.Frame(ventana)
    frame_buscar.grid(row=11, column=0, columnspan=2, pady=10)
    boton_buscar = tk.Button(frame_buscar, text="Buscar", **estilo_boton)
    boton_buscar.pack()

    # Retornamos referencias a widgets para manejo en eventos
    return {
        "ventana": ventana,
        "entries": entries,
        "boton_guardar": boton_guardar,
        "combo_duenios": combo_duenios,
        "boton_eliminar": boton_eliminar,
        "boton_modificar": boton_modificar,
        "entry_busqueda": entry_busqueda,
        "boton_buscar": boton_buscar
    }