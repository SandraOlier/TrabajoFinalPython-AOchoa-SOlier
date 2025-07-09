import tkinter as tk

def barrita_menu(ventana):
    barra = tk.Menu(ventana)
    ventana.config(menu=barra)

    menu_archivo = tk.Menu(barra, tearoff=0)
    barra.add_cascade(label="Archivo", menu=menu_archivo)
    menu_archivo.add_command(label="Salir", command=ventana.quit)

    menu_ayuda = tk.Menu(barra, tearoff=0)
    barra.add_cascade(label="Ayuda", menu=menu_ayuda)
    menu_ayuda.add_command(label="Acerca de...", command=lambda: tk.messagebox.showinfo("Acerca de", "Sistema Veterinario v1.0"))