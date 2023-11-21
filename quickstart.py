from __future__ import print_function

import os.path
import httplib2
import flet as ft

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']


def main(page: ft.Page):
    page.window_width = 400
    page.window_height = 900
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
        page.add(ft.Text("Lista de los 10 primeros contactos"))
        results = service.people().connections().list(
            resourceName='people/me',
            pageSize=10,
            personFields='names,emailAddresses,phoneNumbers,addresses').execute()
        connections = results.get('connections', [])
        i = 0
        for person in connections:
            page.add(ft.Text(f'Contacto {i}'))
            names = person.get('names', [])
            if names:
                name = names[0].get('displayName')
                page.add(ft.Text("Nombre: " + name))
                
            emails = person.get('emailAddresses', [])
            if emails:
                email = emails[0].get('value')
                page.add(ft.Text("Correo electronico: " + email))
                
            phones = person.get('phoneNumbers', [])
            if phones:
                phone = phones[0].get('value')
                page.add(ft.Text("Telefono: " + phone))
            
            addresses = person.get('addresses', [])
            if addresses:
                address = addresses[0].get('formattedValue')
                def reemplazar_espacios_saltos(address):
                    return address.replace(" ", "+").replace("\n", "+")
                direccionAjustada = reemplazar_espacios_saltos(address)
                url = "Link: [Ubicacion](https://www.google.com/maps?q=" + direccionAjustada +"&hl=es&authuser=2)"
                page.add(ft.Text("Direccion: " + address))
                page.add(ft.Markdown(
                    url,
                    on_tap_link=lambda e: page.launch_url(e.data),
                ))
            page.add(ft.Text("----------------------------------"))
            i += 1
    except HttpError as err:
        print(err)
    page.update()
ft.app(target=main, view=ft.AppView.WEB_BROWSER)