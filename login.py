import flet as ft
from config.database import *

def main(page: ft.Page):
    def login(e):
        cursor.execute("select * from usuario where nombre = %s", (usuarioDato.value,))
        data = cursor.fetchone()
        if data:
            print(f"Bienvenido {usuarioDato.value}")
        else:
            print("Usuario no encontrado. Registrese")
            
        page.update()
    page.window_width = 400
    page.window_height = 900
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.LOCATION_PIN, color=ft.colors.GREEN_500),
        leading_width=40,
        title=ft.Text("Bajan Contacts"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
    )
    
    usuarioDato = ft.TextField(
        label="Usuario", 
        hint_text="Ingrese usuario: "
    )

    contraseñaDato = ft.TextField(
        label="Contraseña", 
        hint_text="Ingrese contraseña", 
        password=True, 
        can_reveal_password=True
    )

    boton = ft.ElevatedButton(
        text="Iniciar sesion",
        color="green500", 
        on_click=login
    )

    page.add(
        usuarioDato, 
        contraseñaDato, 
        boton
    )

    def registrar(e):
        cursor.execute("select * from usuario where nombre = %s", (usuarioDato.value,))
        data = cursor.fetchone()
        if data:
            print("El usuario ya existe, elija uno diferente")
        else:
            cursor.execute("insert into usuario values (%s, %s)", (usuarioDato.value, contraseñaDato.value))
            data = cursor.fetchall()
            conn.commit()
            print("Registro ingresado correctamente")
            page.update()
    
    botonRegistro = ft.ElevatedButton(
        text="Registrar", 
        color="green500",
        on_click=registrar
    )

    page.add(botonRegistro)
    
ft.app(target=main)