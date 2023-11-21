import flet as ft

def main(page: ft.Page):
    page.title = "BajanContacts"
    page.window_width= 400
    page.window_height=700
    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.LOCATION_PIN, color=ft.colors.GREEN_500),
        leading_width=40,
        title=ft.Text("Bajan Contacts"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
    )
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 10
    page.update()

    
    # page.add(ft.Text("Bajan Contacts",size=30, color=ft.colors.WHITE))
    page.add(
        ft.Row(
            [
                ft.TextField(label="Buscar", width=180),
                ft.IconButton(
                    icon=ft.icons.SEARCH,
                    icon_color="green300",
                    icon_size=30,
                    tooltip="Buscar",
                ),
                ft.IconButton(
                    icon=ft.icons.FILTER_LIST,
                    icon_color="green300",
                    icon_size=30,
                    tooltip="Filtrar",
                ),
                ft.IconButton(
                    icon=ft.icons.ACCOUNT_CIRCLE,
                    icon_color="green300",
                    icon_size=45,
                    tooltip="Perfil",
                )
            ]
        ),
    )
    page.add(
        ft.Row(
            [
                ft.IconButton(
                    icon=ft.icons.ACCOUNT_CIRCLE,
                    icon_color="green500",
                    icon_size=30,
                ),
                ft.Text(
                    "Contacto guardado",
                    size=20, 
                    color=ft.colors.WHITE
                ),
                ft.IconButton(
                    icon=ft.icons.LOCATION_PIN,
                    icon_color="green500",
                    icon_size=30,
                )
            ]
        )
    )

    # def open_url(e):
    #     page.launch_url(e.data)
    # page.add(
    #     ft.Markdown(
    #         "[Link a mi perfil de Github](https://github.com/eliasgrolon)",
    #         extension_set="gitHubWeb",
    #         on_tap_link=open_url,
    #         expand=True,
    #     ),
    # )
    
ft.app(target=main)
