import tkinter as tk
from PIL import Image, ImageTk
import subprocess

from form_duenios import datos
from vista.vista import Frame, barrita_menu, crear_boton_canvas

# Función real para abrir formularios externos
def abrir_formulario(nombre_archivo):
    subprocess.Popen(["python3", nombre_archivo])

def main():
    ventana = tk.Tk()
    ventana.iconbitmap("img/icono.ico")
    ventana.title("Bienvenida - Sistema Veterinario")
    ventana.geometry("320x520")
    ventana.config(bg="#e9d8a6")

    # Imagen (PATITA.png)
    try:
        imagen = Image.open("img/PATITA.png")
        imagen = imagen.resize((80, 80))
        imagen_tk = ImageTk.PhotoImage(imagen)
        label_imagen = tk.Label(ventana, image=imagen_tk, bg="#e9d8a6")
        label_imagen.image = imagen_tk
        label_imagen.pack(pady=(20, 5), padx=30)  # <-- Ajustá el padding si querés más a la derecha
    except Exception as e:
        print(f"No se pudo cargar la imagen: {e}")

    # Texto de bienvenida
    label = tk.Label(ventana, text="Bienvenidos al sistema", font=("Arial", 16), bg="#e9d8a6")
    label.pack(pady=(0, 15))

    # Menú superior
    barrita_menu(ventana)

    # Marco principal
    app = Frame(root=ventana)

    # ✅ Botones personalizados con canvas - tonos marrones/beiges en degradé
    crear_boton_canvas(app, "Formulario Dueños", lambda: abrir_formulario("form_duenios.py"),
                       color_fondo="#9c6b4f", color_hover="#c69d7b", color_texto="black")

    crear_boton_canvas(app, "Formulario Mascotas", lambda: abrir_formulario("form_mascotas.py"),
                       color_fondo="#b08968", color_hover="#ddb892", color_texto="black")

    crear_boton_canvas(app, "Formulario Veterinarios", lambda: abrir_formulario("form_veterinarios.py"),
                       color_fondo="#c3a47a", color_hover="#e0cba6", color_texto="black")

    crear_boton_canvas(app, "Formulario Visitas", lambda: abrir_formulario("form_visitas.py"),
                       color_fondo="#d0b28d", color_hover="#eedfbe", color_texto="black")

    crear_boton_canvas(app, "Formulario Ver Visitas", lambda: abrir_formulario("ver_visitas.py"),
                       color_fondo="#d4c48f", color_hover="#e6dbb0", color_texto="black")
    
    crear_boton_canvas(app, "Formulario Nuevos Veterinarios", lambda: abrir_formulario("form_cargar_veterinarios_nuevos.py"),
                       color_fondo="#d8c799", color_hover="#f0e3b8", color_texto="black")

    ventana.mainloop()

if __name__ == '__main__':
    main()