import flet as ft

def main(page: ft.Page):
    def bs_dismissed(e):
        print("Algo fallo en el procedimiento!")

    def show_bs(e):
        bs.open = True
        bs.update()

    def close_bs(e):
        bs.open = False
        bs.update()

    bs = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    ft.Text(
                        "Datos del contacto",
                        size=20,
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.icons.ACCOUNT_CIRCLE,
                                icon_color="green500",
                                icon_size=30
                            ),
                            ft.Text(
                                "Nombre",
                                size=15,
                            ),
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
                                "Telefono",
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
                                "Correo electronico",
                                size=15,
                            ),
                        ]
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.icons.LOCATION_PIN,
                                icon_color="green500",
                                icon_size=30
                            ),
                            ft.Text(
                                "Ver ubicacion",
                                size=15,
                            ),
                        ]
                    ),
                    ft.ElevatedButton(
                        "Salir",
                        color="green500",
                        on_click=close_bs
                    ),
                ],
                tight=True,
            ),
            padding=20,
            width=900,
        ),
        open=True,
        on_dismiss=bs_dismissed,
    )
    page.overlay.append(bs)
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
                    "Contacto",
                    size=20,
                ),
            ]
        ),
    )
ft.app(target=main)