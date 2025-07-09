import tkinter as tk

class Frame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=480, height=320)
        self.root = root
        self.pack(padx=10, pady=10)
        self.config(bg="#e9d8a6")  # Fondo beige

    def crear_boton(self, texto, comando, bg="#a7d3f5", activebg="#90c2eb", fg="black"):
        boton = tk.Button(
            self,
            text=texto,
            command=comando,
            width=25,
            bg=bg,
            activebackground=activebg,
            fg=fg,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            font=("Arial", 10, "bold")
        )
        boton.pack(pady=5)
        return boton


def barrita_menu(root):
    barra = tk.Menu(root)
    root.config(menu=barra)

    # Menú "Inicio"
    menu_inicio = tk.Menu(barra, tearoff=0)
    barra.add_cascade(label='Inicio', menu=menu_inicio)
    menu_inicio.add_command(label='Conectar DB', command=lambda: print("Conectando DB..."))
    menu_inicio.add_command(label='Desconectar DB', command=lambda: print("Desconectando DB..."))
    menu_inicio.add_separator()
    menu_inicio.add_command(label='Salir', command=root.destroy)

    # Menú "Consultas"
    menu_consultas = tk.Menu(barra, tearoff=0)
    barra.add_cascade(label='Consultas', menu=menu_consultas)
    menu_consultas.add_command(label='Ver Dueños', command=lambda: print("Mostrando Dueños"))
    menu_consultas.add_command(label='Ver Mascotas', command=lambda: print("Mostrando Mascotas"))
    menu_consultas.add_command(label='Ver Visitas', command=lambda: print("Mostrando Visitas"))

    # Menú "Acerca de..."
    menu_acerca = tk.Menu(barra, tearoff=0)
    barra.add_cascade(label='Acerca de...', menu=menu_acerca)
    menu_acerca.add_command(label='Versión 1.0', command=lambda: print("Versión 1.0"))
    menu_acerca.add_command(label='Autores', command=lambda: print("Autores"))

    # Menú "Ayuda"
    menu_ayuda = tk.Menu(barra, tearoff=0)
    barra.add_cascade(label='Ayuda', menu=menu_ayuda)
    menu_ayuda.add_command(label='Cómo usar el sistema', command=lambda: print("Ayuda - Cómo usar"))
    menu_ayuda.add_command(label='Contacto soporte', command=lambda: print("Contacto soporte"))


def crear_boton_canvas(root, texto, comando,
                       color_fondo="#b08968", color_hover="#ddb892", color_texto="black"):
    ancho = 200
    alto = 40

    canvas = tk.Canvas(root, width=ancho, height=alto, bg=root['bg'], highlightthickness=0)
    canvas.pack(pady=5)

    # Rectángulo con bordes "redondeados" simulados con ovales (solo esquinas)
    radio = 20  # radio para simular bordes redondeados

    # Fondo principal
    rect = canvas.create_rectangle(radio, 0, ancho - radio, alto, fill=color_fondo, outline=color_fondo)
    # Esquinas ovaladas izquierda y derecha para simular bordes redondeados
    oval_izq = canvas.create_oval(0, 0, radio*2, alto, fill=color_fondo, outline=color_fondo)
    oval_der = canvas.create_oval(ancho - 2*radio, 0, ancho, alto, fill=color_fondo, outline=color_fondo)

    texto_id = canvas.create_text(ancho // 2, alto // 2, text=texto, fill=color_texto, font=("Arial", 10, "bold"))

    def al_entrar(event):
        canvas.itemconfig(rect, fill=color_hover)
        canvas.itemconfig(oval_izq, fill=color_hover)
        canvas.itemconfig(oval_der, fill=color_hover)

    def al_salir(event):
        canvas.itemconfig(rect, fill=color_fondo)
        canvas.itemconfig(oval_izq, fill=color_fondo)
        canvas.itemconfig(oval_der, fill=color_fondo)

    def al_click(event):
        comando()

    # Asociar eventos al canvas entero
    canvas.tag_bind(rect, "<Enter>", al_entrar)
    canvas.tag_bind(rect, "<Leave>", al_salir)
    canvas.tag_bind(rect, "<Button-1>", al_click)

    canvas.tag_bind(oval_izq, "<Enter>", al_entrar)
    canvas.tag_bind(oval_izq, "<Leave>", al_salir)
    canvas.tag_bind(oval_izq, "<Button-1>", al_click)

    canvas.tag_bind(oval_der, "<Enter>", al_entrar)
    canvas.tag_bind(oval_der, "<Leave>", al_salir)
    canvas.tag_bind(oval_der, "<Button-1>", al_click)

    canvas.tag_bind(texto_id, "<Enter>", al_entrar)
    canvas.tag_bind(texto_id, "<Leave>", al_salir)
    canvas.tag_bind(texto_id, "<Button-1>", al_click)

    return canvas

