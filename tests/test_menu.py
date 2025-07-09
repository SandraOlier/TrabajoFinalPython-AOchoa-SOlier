# -*- coding: utf-8 -*-

import tkinter as tk

def main():
    ventana = tk.Tk()
    ventana.title("Prueba barra de menú")
    ventana.geometry("300x200")

    # Crear la barra de menú
    barra_menu = tk.Menu(ventana)
    ventana.config(menu=barra_menu)

    # Menú "Inicio"
    menu_inicio = tk.Menu(barra_menu, tearoff=0)
    menu_inicio.add_command(label="Opción 1")
    menu_inicio.add_command(label="Salir", command=ventana.quit)
    barra_menu.add_cascade(label="Inicio", menu=menu_inicio)

    # Menú "Ayuda"
    menu_ayuda = tk.Menu(barra_menu, tearoff=0)
    menu_ayuda.add_command(label="Acerca de...")
    barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)

    ventana.mainloop()

if __name__ == "__main__":
    main()