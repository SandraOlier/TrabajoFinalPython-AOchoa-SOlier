# consultas.py
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date

def ventana_consultas():
    def guardar_consulta():
        conn = sqlite3.connect("veterinaria.db")
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO consultas (id_mascota, fecha, motivo, tratamiento)
                VALUES (?, ?, ?, ?)
            """, (
                int(combo_mascota.get().split(" - ")[0]),
                entry_fecha.get(),
                entry_motivo.get(),
                entry_tratamiento.get()
            ))
            conn.commit()
            messagebox.showinfo("Consulta registrada", "La consulta fue guardada correctamente")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def obtener_mascotas():
        conn = sqlite3.connect("veterinaria.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id_mascota, nombre FROM mascotas")
        lista = [f"{m[0]} - {m[1]}" for m in cursor.fetchall()]
        conn.close()
        return lista

    win = tk.Toplevel()
    win.title("Registrar Consulta")
    win.geometry("320x350")

    tk.Label(win, text="Mascota").pack()
    combo_mascota = ttk.Combobox(win, values=obtener_mascotas())
    combo_mascota.pack()

    tk.Label(win, text="Fecha").pack()
    entry_fecha = tk.Entry(win)
    entry_fecha.insert(0, date.today().isoformat())  # Fecha actual por defecto
    entry_fecha.pack()

    tk.Label(win, text="Motivo").pack()
    entry_motivo = tk.Entry(win)
    entry_motivo.pack()

    tk.Label(win, text="Tratamiento").pack()
    entry_tratamiento = tk.Entry(win)
    entry_tratamiento.pack()

    tk.Button(win, text="Guardar Consulta", command=guardar_consulta).pack(pady=10)