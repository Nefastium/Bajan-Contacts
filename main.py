from __future__ import print_function

import os.path
import httplib2
import flet as ft

from flet_route import routing,path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']


def main(page: ft.Page):
    page.clean()
    page.window_width = 500
    page.window_height = 700
    page.scroll = "adaptive"
    """Shows basic usage of the People API.
    Prints the name of the first 10 connections.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('people', 'v1', credentials=creds)

        # Call the People API

        page.appbar = ft.AppBar(
                leading=ft.Icon(ft.icons.LOCATION_PIN, color=ft.colors.GREEN_500),
                leading_width=40,
                title=ft.Text("Bajan Contacts"),
                center_title=False,
                bgcolor=ft.colors.SURFACE_VARIANT,
            )
        
        def buscar_usuario(e):
            valor_a_buscar = buscar.value
            for person in connections:
                name = None
                names = person.get('names', [])
                if names:
                    name = names[0].get('displayName')
                    # Comprueba si los caracteres están en el nombre
                    if valor_a_buscar in name:
                        msj = f"Nombre encontrado: {name}"
                        page.clean()
                        page.appbar = ft.AppBar(
                            leading=ft.Icon(ft.icons.LOCATION_PIN, color=ft.colors.GREEN_500),
                            leading_width=40,
                            title=ft.Text("Bajan Contacts"),
                            center_title=False,
                            bgcolor=ft.colors.SURFACE_VARIANT,
                        )
                        page.add(
                            ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.icons.ARROW_BACK,
                                            icon_color="green300",
                                            icon_size=30,
                                            tooltip="Atras",
                                            on_click= lambda e: main(page)
                                        )
                                    ]
                                ),
                            )
                        name = None
                        names = person.get('names', [])
                        if names:
                            name = names[0].get('displayName')
                            
                        email = None
                        emails = person.get('emailAddresses', [])
                        if emails:
                            email = emails[0].get('value')
                            
                        phone = None
                        phones = person.get('phoneNumbers', [])
                        if phones:
                            phone = phones[0].get('value')
                        
                        address = None
                        direccionAjustada = "No_Info"
                        addresses = person.get('addresses', [])
                        if addresses:
                            address = addresses[0].get('formattedValue')

                            def reemplazar_espacios_saltos(address):
                                return address.replace(" ", "+").replace("\n", "+")
                            
                            direccionAjustada = reemplazar_espacios_saltos(address)
                            url = "Link: [Ubicacion](https://www.google.com/maps?q=" + direccionAjustada +"&hl=es&authuser=2)"

                        if not name:
                            name = "Sin información"
                        if not phone:
                            phone = "Sin información"
                        if not email:
                            email = "Sin información"
                        if not address:
                            address = "Sin información"
                        bs, show_bs = crear_bs_para_contacto(name, phone, email, address, direccionAjustada)
                        page.add(
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.icons.ACCOUNT_CIRCLE,
                                        icon_color="green500",
                                        icon_size=30,
                                        on_click=show_bs
                                    ),
                                    ft.Text(
                                        name,
                                        size=20, 
                                        color=ft.colors.WHITE,
                                    )
                                ]
                            )
                        )
            else:
                msj = "No hay Informacion"
            print(msj)

        buscar = ft.TextField(label="Buscar", width=210)
        page.add(
            ft.Row(
                    [
                        buscar,
                        ft.IconButton(
                            icon=ft.icons.SEARCH,
                            icon_color="green500",
                            icon_size=30,
                            tooltip="Buscar",
                            on_click=buscar_usuario
                        ),
                        ft.IconButton(
                            icon=ft.icons.FILTER_LIST,
                            icon_color="green500",
                            icon_size=30,
                            tooltip="Filtrar",
                        ),
                        ft.IconButton(
                            icon=ft.icons.ACCOUNT_CIRCLE,
                            icon_color="green500",
                            icon_size=45,
                            tooltip="Perfil",
                        )
                    ]
                ),
            )
        
        results = service.people().connections().list(
            resourceName='people/me',
            # pageSize=10,
            personFields='names,emailAddresses,phoneNumbers,addresses').execute()
        
        connections = results.get('connections', [])
        i = 0

        def crear_bs_para_contacto(nombre, telefono, correo, ubicacion, ubi_link):
            def bs_dismissed(e):
                print("Algo fallo en el procedimiento!")
            def close_bs(e):
                bs.open = False
                bs.update()
            def show_bs(e):
                bs.open = True
                bs.update()

            
            bs = ft.BottomSheet(
                ft.Container(
                    ft.Column(
                        [
                            ft.Text("Datos del contacto", size=20),
                            ft.Row(
                                [
                                    ft.IconButton(icon=ft.icons.ACCOUNT_CIRCLE, icon_color="green500", icon_size=30),
                                    ft.Text(nombre, size=15),
                                ]
                            ),     
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.icons.LOCAL_PHONE,
                                        icon_color="green500",
                                        icon_size=30
                                    ),
                                    ft.Text(
                                        telefono,
                                        size=15,
                                    ),
                                ]
                            ),
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.icons.MAIL,
                                        icon_color="green500",
                                        icon_size=30
                                    ),
                                    ft.Text(
                                        correo,
                                        size=15,
                                    ),
                                ]
                            ),
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.icons.LOCATION_PIN,
                                        icon_color="green500",
                                        icon_size=30,
                                        on_click=lambda e: page.launch_url("https://www.google.com/maps?q=" + ubi_link +"&hl=es&authuser=2")
                                    ),
                                    ft.Text(
                                        ubicacion,
                                        size=15,
                                    ),
                                ]
                            ),
                            ft.ElevatedButton("Salir", color="green500", on_click=close_bs),
                        ],
                        tight=True,
                    ),
                    padding=20,
                    width=900,
                ),
                open=False,
                on_dismiss=bs_dismissed,
            )
            page.overlay.append(bs)
            return bs, show_bs

        for person in connections:
            name = None
            names = person.get('names', [])
            if names:
                name = names[0].get('displayName')
                
            email = None
            emails = person.get('emailAddresses', [])
            if emails:
                email = emails[0].get('value')
                
            phone = None
            phones = person.get('phoneNumbers', [])
            if phones:
                phone = phones[0].get('value')
            
            address = None
            direccionAjustada = "No_Info"
            addresses = person.get('addresses', [])
            if addresses:
                address = addresses[0].get('formattedValue')

                def reemplazar_espacios_saltos(address):
                    return address.replace(" ", "+").replace("\n", "+")
                
                direccionAjustada = reemplazar_espacios_saltos(address)
                url = "Link: [Ubicacion](https://www.google.com/maps?q=" + direccionAjustada +"&hl=es&authuser=2)"

            if not name:
                name = "Sin información"
            if not phone:
                phone = "Sin información"
            if not email:
                email = "Sin información"
            if not address:
                address = "Sin información"
            bs, show_bs = crear_bs_para_contacto(name, phone, email, address, direccionAjustada)
            page.add(
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.icons.ACCOUNT_CIRCLE,
                            icon_color="green500",
                            icon_size=30,
                            on_click=show_bs
                        ),
                        ft.Text(
                            name,
                            size=20, 
                            color=ft.colors.WHITE,
                        )
                    ]
                )
            )
            i += 1
    except HttpError as err:
        print(err)
    page.update()
ft.app(target=main)