import flet as ft
import mysql.connector


conn=mysql.connector.connect(
    host= 'localhost',
    database= 'pdi',
    user= 'root',
    password= 'root'
)
# Crear un cursor para interactuar con la base de datos
cursor=conn.cursor()


def main(page: ft.Page):
    page.window_width = 1000
    page.window_height = 800

    def buscar_usuario(e):
            # Realizar una consulta SQL para buscar datos
            consulta = "SELECT nombre FROM usuarios WHERE nombre = %s"
            valor_a_buscar = [usuario.value]
            cursor.execute(consulta,valor_a_buscar)
            # Obtener los resultados de la consulta
            resultados = cursor.fetchone()
            if resultados is None:
                print("feo")
                resultados = "agregue texto al campo"
            else:
                resultados=resultados[0]
            msj.value= resultados
            page.update()


    usuario=ft.TextField(hint_text="Ingrese nombre de usuario")
    boton=ft.FilledButton(text="buscar",on_click=buscar_usuario)
    msj=ft.Text("")
    page.add(ft.Text("CheckTask"))
    page.add(ft.Column(controls=[
        usuario,
        boton,
    ]))
    page.add(msj)
    page.update()
    
    

ft.app(target = main)