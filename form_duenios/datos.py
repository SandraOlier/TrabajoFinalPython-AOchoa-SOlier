import sqlite3
import os
from tkinter import messagebox


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))

DB_PATH = os.path.join(PROJECT_DIR, 'mascotas.db')


def cargar_duenios():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, apellido, telefono FROM duenios")
        resultados = cursor.fetchall()
        conn.close()
        return [f"{nombre} {apellido} | {telefono}" for nombre, apellido, telefono in resultados]
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los dueños: {e}")
        return []

def insertar_duenio(nombre, apellido, telefono, email, direccion, ciudad):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO duenios (nombre, apellido, telefono, email, direccion, ciudad)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre, apellido, telefono, email, direccion, ciudad))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")
        return False

def eliminar_duenio_db(nombre, apellido, telefono):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM duenios WHERE nombre = ? AND apellido = ? AND telefono = ?",
                       (nombre, apellido, telefono))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el dueño: {e}")
        return False

def modificar_duenio_db(nombre_nuevo, apellido_nuevo, telefono_nuevo, email_nuevo, direccion_nueva, ciudad_nueva,
                        nombre_orig, apellido_orig, telefono_orig):
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
        return True
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo modificar el dueño: {e}")
        return False

def buscar_duenios(termino):
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
                filtrados.append(f"{nombre} {apellido} {telefono}")
        return filtrados
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo realizar la búsqueda: {e}")
        return []
