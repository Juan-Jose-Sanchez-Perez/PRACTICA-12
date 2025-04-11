import flet as ft

def main(page: ft.Page):
    page.title = "Gestión de Empleados"
    page.window_width = 600
    page.window_height = 500
    
    # Controles del formulario
    id_empleado = ft.TextField(label="ID Empleado", width=300)
    nombre = ft.TextField(label="Nombre", width=300)
    puesto = ft.TextField(label="Puesto", width=300)
    salario = ft.TextField(label="Salario", width=300)
    turno = ft.Dropdown(
        label="Turno",
        width=300,
        options=[
            ft.dropdown.Option("Matutino"),
            ft.dropdown.Option("Vespertino"),
            ft.dropdown.Option("Nocturno"),
        ]
    )
    
    # Botones
    btn_guardar = ft.ElevatedButton("Guardar", icon=ft.icons.SAVE)
    btn_limpiar = ft.ElevatedButton("Limpiar", icon=ft.icons.CLEAR)
    btn_eliminar = ft.ElevatedButton("Eliminar", icon=ft.icons.DELETE)
    
    # Diseño de la página
    page.add(
        ft.Column(
            controls=[
                ft.Text("Gestión de Empleados", size=24, weight="bold"),
                ft.Divider(),
                id_empleado,
                nombre,
                puesto,
                salario,
                turno,
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