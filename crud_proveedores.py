import flet as ft
from db_connection import get_connection

def main(page: ft.Page):
    page.title = "CRUD Proveedores"
    page.scroll = ft.ScrollMode.AUTO

    editing_id = None

    # Campos del formulario
    nombre = ft.TextField(label="Nombre")
    telefono = ft.TextField(
        label="Teléfono",
        max_length=10,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    contacto = ft.TextField(label="Correo")
    rfc = ft.TextField(
        label="RFC",
        max_length=13,
        keyboard_type=ft.KeyboardType.TEXT  # Ahora permite letras y números
    )
    output = ft.Text("")
    proveedores_list = ft.Column()
    botones = ft.Row()

    def limpiar_campos():
        nombre.value = telefono.value = contacto.value = rfc.value = ""
        output.value = ""
        page.update()

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
        cursor.execute("SELECT id_proveedor, nombre, telefono, contacto, rfc FROM Proveedores")
        for id_prov, nom, tel, cont, rfc_val in cursor.fetchall():
            proveedores_list.controls.append(
                ft.Row([
                    ft.Text(f"{id_prov} - {nom} - {tel} - {cont} - {rfc_val}", expand=True),
                    ft.IconButton(icon=ft.icons.EDIT,   on_click=lambda e, i=id_prov: editar_proveedor(i)),
                    ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, i=id_prov: eliminar_proveedor(i))
                ])
            )
        conn.close()
        page.update()

    def validar_campos():
        # Teléfono: exactamente 10 dígitos numéricos
        if len(telefono.value or "") != 10 or not telefono.value.isdigit():
            output.value = "El teléfono debe tener 10 dígitos numéricos."
            page.update()
            return False
        # RFC: exactamente 13 caracteres alfanuméricos
        valor_rfc = (rfc.value or "").upper()
        if len(valor_rfc) != 13 or not valor_rfc.isalnum():
            output.value = "El RFC debe tener 13 caracteres (letras y números)."
            page.update()
            return False
        return True

    def registrar_proveedor(e):
        if not validar_campos() or not nombre.value:
            return
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # forzamos mayúsculas en el RFC
            cursor.execute(
                "INSERT INTO Proveedores (nombre, telefono, contacto, rfc) VALUES (%s, %s, %s, %s)",
                (nombre.value, telefono.value, contacto.value, rfc.value.upper())
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
            cursor.execute("DELETE FROM Proveedores WHERE id_proveedor = %s", (id_prov,))
            conn.commit()
            output.value = "Proveedor eliminado"
        except Exception as ex:
            output.value = f"Error al eliminar: {ex}"
        finally:
            conn.close()
            cargar_proveedores()

    def editar_proveedor(id_prov):
        nonlocal editing_id
        editing_id = id_prov
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT nombre, telefono, contacto, rfc FROM Proveedores WHERE id_proveedor = %s",
            (id_prov,)
        )
        result = cursor.fetchone()
        conn.close()
        if result:
            nombre.value, telefono.value, contacto.value, rfc.value = result
        output.value = ""
        actualizar_botones()

    def guardar_cambios(e):
        nonlocal editing_id
        if not validar_campos() or not nombre.value:
            return
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE Proveedores SET nombre=%s, telefono=%s, contacto=%s, rfc=%s WHERE id_proveedor=%s",
                (nombre.value, telefono.value, contacto.value, rfc.value.upper(), editing_id)
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
        limpiar_campos()
        editing_id = None
        output.value = "Edición cancelada"
        actualizar_botones()

    page.add(
        ft.Text("Registrar / Editar Proveedor", size=20, weight="bold"),
        nombre,
        telefono,
        contacto,
        rfc,
        botones,
        output,
        ft.Divider(),
        ft.Text("Lista de Proveedores", size=20),
        proveedores_list
    )

    # Inicialización
    actualizar_botones()
    cargar_proveedores()

ft.app(target=main)
