import sqlite3
import datos

def test_cargar():
    duenios = datos.cargar_duenios()
    print("Dueños cargados:", duenios)

def test_insertar():
    exito = datos.insertar_duenio("TestNombre", "TestApellido", "123456789", "test@mail.com", "Calle Falsa 123", "CiudadX")
    print("Inserción exitosa:", exito)

def test_buscar():
    resultados = datos.buscar_duenios("TestNombre")
    print("Resultados búsqueda:", resultados)

def test_eliminar():
    exito = datos.eliminar_duenio_db("TestNombre", "TestApellido", "123456789")
    print("Eliminación exitosa:", exito)

if __name__ == "__main__":
    test_insertar()
    test_cargar()
    test_buscar()
    test_eliminar()
    test_cargar()