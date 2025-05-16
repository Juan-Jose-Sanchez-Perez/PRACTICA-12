import flet as ft 
from db_connection import get_connection

def main(page: ft.Page):
    page.title = "CRUD Proveedores"
    page.scroll = ft.ScrollMode.AUTO

    # Estado de edición: None = modo registro, sino = id del proveedor a editar
    editing_id = None

    # Campos del formulario
    nombre = ft.TextField(label="Nombre")
    telefono = ft.TextField(label="Teléfono")
    contacto = ft.TextField(label="Correo")
    output = ft.Text("")
    proveedores_list = ft.Column()
    # Contenedor para los botones (Registrar o Guardar/Cancelar)
    botones = ft.Row()

    def limpiar_campos():
        nombre.value = telefono.value = contacto.value = ""
        output.value = ""
    
    def actualizar_botones():
        botones.controls.clear()
        if editing_id is None:
            botones.controls.append(ft.ElevatedButton("Registrar", on_click=registrar_proveedor))
        else:
            botones.controls.append(ft.ElevatedButton("Guardar cambios", on_click=guardar_cambios))
            botones.controls.append(ft.ElevatedButton("Cancelar", on_click=cancelar_edicion))
        page.update()

    def cargar_proveedores():
        proveedores_list.controls.clear()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Proveedores")
        for id_prov, nom, tel, cont in cursor.fetchall():
            proveedores_list.controls.append(
                ft.Row([
                    ft.Text(f"{id_prov} - {nom} - {tel} - {cont}", expand=True),
                    ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, id=id_prov: editar_proveedor(id)),
                    ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, id=id_prov: eliminar_proveedor(id))
                ])
            )
        conn.close()
        page.update()

    def registrar_proveedor(e):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Proveedores (nombre, telefono, contacto) VALUES (%s, %s, %s)",
                (nombre.value, telefono.value, contacto.value)
            )
            conn.commit()
            output.value = "Proveedor registrado correctamente"
            limpiar_campos()
        except Exception as ex:
            output.value = f"Error: {ex}"
        finally:
            conn.close()
            cargar_proveedores()

    def eliminar_proveedor(id_prov):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM Proveedores WHERE id_proveedor = %s",
                (id_prov,)
            )
            conn.commit()
            output.value = "Proveedor eliminado"
        except Exception as ex:
            output.value = f"Error al eliminar: {ex}"
        finally:
            conn.close()
            cargar_proveedores()

    def editar_proveedor(id_prov):
        nonlocal editing_id
        # Paso a modo edición
        editing_id = id_prov
        # Cargo datos al formulario
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT nombre, telefono, contacto FROM Proveedores WHERE id_proveedor = %s",
            (id_prov,)
        )
        result = cursor.fetchone()
        conn.close()
        if result:
            nombre.value, telefono.value, contacto.value = result
        actualizar_botones()

    def guardar_cambios(e):
        nonlocal editing_id
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE Proveedores SET nombre=%s, telefono=%s, contacto=%s WHERE id_proveedor=%s",
                (nombre.value, telefono.value, contacto.value, editing_id)
            )
            conn.commit()
            output.value = "Proveedor actualizado"
            limpiar_campos()
            editing_id = None
        except Exception as ex:
            output.value = f"Error al actualizar: {ex}"
        finally:
            conn.close()
            actualizar_botones()
            cargar_proveedores()

    def cancelar_edicion(e):
        nonlocal editing_id
        # Cancelo edición, limpio y vuelvo a modo registro
        limpiar_campos()
        editing_id = None
        output.value = "Edición cancelada"
        actualizar_botones()

    # Construcción del layout
    page.add(
        ft.Text("Registrar / Editar Proveedor", size=20, weight="bold"),
        nombre,
        telefono,
        contacto,
        botones,          # aquí irán dinámicamente Registrar ó Guardar/Cancelar
        output,
        ft.Divider(),
        ft.Text("Lista de Proveedores", size=20),
        proveedores_list
    )

    # Inicializo botones y lista
    actualizar_botones()
    cargar_proveedores()

ft.app(target=main)
