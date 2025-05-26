import flet as ft
import subprocess
import os
import sys

def main(page: ft.Page):
    page.title = "Menú Principal - Super_Uno"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    crud_scripts = {
        "Proveedores": "crud_proveedores.py",
        "Categorías": "crud_categorias.py",
        "Artículos": "crud_articulos.py",
        "Clientes": "crud_clientes.py",
        "Empleados": "crud_empleados.py",
        "Compras": "crud_compras.py",
        "Ventas": "crud_ventas.py"
    }

    def lanzar_script(script):
        # Usa el mismo intérprete que ejecuta este archivo
        subprocess.Popen([sys.executable, script], shell=True if os.name == "nt" else False)

    botones = []
    for label, script in crud_scripts.items():
        botones.append(ft.ElevatedButton(text=label, width=250, on_click=lambda e, s=script: lanzar_script(s)))

    page.add(
        ft.Text("Sistema de Gestión - Super_Uno", size=30, weight="bold"),
        ft.Column(botones, alignment=ft.MainAxisAlignment.CENTER)
    )

ft.app(target=main)
