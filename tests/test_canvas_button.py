# -*- coding: utf-8 -*-
import tkinter as tk

def boton_presionado():
    print("¡Botón presionado!")

def crear_boton_canvas(root, texto, comando, x=50, y=50,
                       color_fondo="#b08968", color_hover="#ddb892", color_texto="black"):
    ancho = 200
    alto = 40

    canvas = tk.Canvas(root, width=ancho, height=alto, bg=root['bg'], highlightthickness=0)
    rect = canvas.create_rectangle(0, 0, ancho, alto, fill=color_fondo, outline=color_fondo)
    texto_id = canvas.create_text(ancho//2, alto//2, text=texto, fill=color_texto, font=("Arial", 10, "bold"))

    def al_entrar(event):
        canvas.itemconfig(rect, fill=color_hover)

    def al_salir(event):
        canvas.itemconfig(rect, fill=color_fondo)

    def al_click(event):
        comando()

    canvas.bind("<Enter>", al_entrar)
    canvas.bind("<Leave>", al_salir)
    canvas.bind("<Button-1>", al_click)

    canvas.place(x=x, y=y)
    return canvas

# Ventana principal
ventana = tk.Tk()
ventana.title("Botón Canvas Personalizado")
ventana.geometry("320x200")
ventana.config(bg="#e9d8a6")  # Fondo beige

# Crear botón
crear_boton_canvas(ventana, "Abrir Formulario", boton_presionado)

ventana.mainloop()