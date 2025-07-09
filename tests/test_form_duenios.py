import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Test Combobox")
root.geometry("300x100")
root.configure(bg="#e9d8a6")  # fondo como el tuyo

# No configurar ningún estilo manual
# Usamos el Combobox por defecto como lo maneja macOS

combo = ttk.Combobox(root, values=["Uno", "Dos", "Tres"], state="readonly", width=20)
combo.pack(pady=20)

root.mainloop()