import tkinter as tk

def barra_menu(root):
    barra = tk.Menu(root)
    root.config(menu=barra)

    menu_inicio = tk.Menu(barra, tearoff=0)
    barra.add_cascade(label="Inicio", menu=menu_inicio)
    menu_inicio.add_command(label="Conectar DB")
    menu_inicio.add_command(label="Desconectar DB")
    menu_inicio.add_separator()
    menu_inicio.add_command(label="Salir", command=root.destroy)

    menu_ayuda = tk.Menu(barra, tearoff=0)
    barra.add_cascade(label="Ayuda", menu=menu_ayuda)
    menu_ayuda.add_command(label="Acerca de")
    menu_ayuda.add_command(label="Contacto")

def main():
    ventana = tk.Tk()
    ventana.geometry("300x200")
    ventana.title("Prueba barra de menú")

    barra_menu(ventana)

    ventana.mainloop()

if __name__ == "__main__":
    main()