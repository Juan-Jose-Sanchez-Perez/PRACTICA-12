#JUAN JOSE SANCHEZ PEREZ         INTERFAZ HECHA CON: FLET

import flet as ft

def main(page: ft.Page):
    page.title = "Gestión de Proveedores"
    page.window_width = 600
    page.window_height = 500
    
    # Controles del formulario
    id_proveedor = ft.TextField(label="ID Proveedor", width=300)
    nombre = ft.TextField(label="Nombre", width=300)
    telefono = ft.TextField(label="Teléfono", width=300)
    contacto = ft.TextField(label="Contacto", width=300)
    
    # Botones
    btn_guardar = ft.ElevatedButton("Guardar", icon=ft.icons.SAVE)
    btn_limpiar = ft.ElevatedButton("Limpiar", icon=ft.icons.CLEAR)
    btn_eliminar = ft.ElevatedButton("Eliminar", icon=ft.icons.DELETE)
    
    # Diseño de la página
    page.add(
        ft.Column(
            controls=[
                ft.Text("Gestión de Proveedores", size=24, weight="bold"),
                ft.Divider(),
                id_proveedor,
                nombre,
                telefono,
                contacto,
                ft.Row(
                    controls=[btn_guardar, btn_limpiar, btn_eliminar],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

ft.app(target=main)