import flet as ft
from db_connection import get_connection

def main(page: ft.Page):
    page.title = "CRUD Clientes"
    page.scroll = ft.ScrollMode.AUTO

    
    editing_tel = None

    # Campos de entrada
    telefono = ft.TextField(
        label="Teléfono",
        max_length=10,                            
        keyboard_type=ft.KeyboardType.NUMBER
    )
    nombre = ft.TextField(label="Nombre")
    correo = ft.TextField(label="Correo")
    direccion = ft.TextField(label="Dirección")
    output = ft.Text("")
    clientes_list = ft.Column()
    botones = ft.Row()  # aquí irán Registrar o bien Guardar cambios + Cancelar

    def limpiar_campos():
        telefono.value = nombre.value = correo.value = direccion.value = ""
        # no limpiamos output aquí para preservar mensajes de error/validación
        page.update()

    def actualizar_botones():
        botones.controls.clear()
        if editing_tel is None:
            botones.controls.append(
                ft.ElevatedButton("Registrar", on_click=registrar_cliente)
            )
        else:
            botones.controls.append(
                ft.ElevatedButton("Guardar cambios", on_click=guardar_cambios)
            )
            botones.controls.append(
                ft.ElevatedButton("Cancelar", on_click=cancelar_edicion)
            )
        page.update()

    # Cargar clientes
    def cargar_clientes():
        clientes_list.controls.clear()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT telefono, nombre, correo, direccion, fecha_registro FROM Clientes"
        )
        for tel, nom, mail, dir_, fecha in cursor.fetchall():
            clientes_list.controls.append(
                ft.Row([
                    ft.Text(f"{tel} – {nom} – {mail} – {dir_} – {fecha}", expand=True),
                    ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, t=tel: editar_cliente(t)),
                    ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, t=tel: eliminar_cliente(t))
                ])
            )
        conn.close()
        page.update()

    # Registrar nuevo cliente
    def registrar_cliente(e):
        # Validación de teléfono
        if len(telefono.value or "") != 10 or not telefono.value.isdigit():
            output.value = "El teléfono debe tener exactamente 10 dígitos numéricos."
            page.update()
            return

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Clientes (telefono, nombre, correo, direccion) VALUES (%s, %s, %s, %s)",
                (telefono.value, nombre.value, correo.value, direccion.value)
            )
            conn.commit()
            output.value = "Cliente registrado"
            limpiar_campos()
        except Exception as ex:
            output.value = f"Error: {ex}"
        finally:
            conn.close()
            cargar_clientes()

    # Eliminar cliente
    def eliminar_cliente(tel):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Clientes WHERE telefono = %s", (tel,))
            conn.commit()
            output.value = "Cliente eliminado"
        except Exception as ex:
            output.value = f"Error al eliminar: {ex}"
        finally:
            conn.close()
            cargar_clientes()

    # Pasar a modo edición
    def editar_cliente(tel):
        nonlocal editing_tel
        editing_tel = tel
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT nombre, correo, direccion FROM Clientes WHERE telefono = %s",
            (tel,)
        )
        result = cursor.fetchone()
        conn.close()
        if result:
            nombre.value, correo.value, direccion.value = result
            telefono.value = tel  # mantenemos el teléfono como clave
        output.value = ""
        actualizar_botones()

    # Guardar cambios de la edición
    def guardar_cambios(e):
        nonlocal editing_tel
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE Clientes
                SET nombre=%s, correo=%s, direccion=%s
                WHERE telefono=%s
                """,
                (nombre.value, correo.value, direccion.value, editing_tel)
            )
            conn.commit()
            output.value = "Cliente actualizado"
            limpiar_campos()
            editing_tel = None
        except Exception as ex:
            output.value = f"Error al actualizar: {ex}"
        finally:
            conn.close()
            actualizar_botones()
            cargar_clientes()

    # Cancelar la edición
    def cancelar_edicion(e):
        nonlocal editing_tel
        limpiar_campos()
        editing_tel = None
        output.value = "Edición cancelada"
        actualizar_botones()

    # Montaje de la UI
    page.add(
        ft.Text("Registrar / Editar Cliente", size=20, weight="bold"),
        telefono,
        nombre,
        correo,
        direccion,
        botones,      # Aquí aparecen Registrar ó Guardar cambios + Cancelar
        output,
        ft.Divider(),
        ft.Text("Lista de Clientes", size=20),
        clientes_list
    )

    # Inicialización
    actualizar_botones()
    cargar_clientes()

ft.app(target=main)
