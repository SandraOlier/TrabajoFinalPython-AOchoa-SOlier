import tkinter as tk
from tkinter import ttk
import sqlite3

def listar_visitas():
    conn = sqlite3.connect("/Users/Andrea/Desktop/mascotas.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT v.id, m.nombre, vet.nombre, esp.nombre, v.fecha, v.motivo
        FROM visitas v
        JOIN mascotas m ON v.id_mascota = m.id
        JOIN veterinarios vet ON v.id_veterinario = vet.id
        JOIN especialidades esp ON v.id_especialidad = esp.id;
    """)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def cargar_en_tabla():
    for fila in tree.get_children():
        tree.delete(fila)
    for visita in listar_visitas():
        tree.insert("", tk.END, values=visita)

root = tk.Tk()
root.title("Listado de Visitas")
root.geometry("800x400")

# Definir columnas
columns = ("ID", "Mascota", "Veterinario", "Especialidad", "Fecha", "Motivo")

tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.pack(fill=tk.BOTH, expand=True)

# Botón para cargar datos
btn_cargar = tk.Button(root, text="Cargar Visitas", command=cargar_en_tabla)
btn_cargar.pack(pady=10)

root.mainloop()
