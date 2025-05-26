import flet as ft
from db_connection import get_connection

def main(page: ft.Page):
    page.title = "CRUD Categorías"
    page.scroll = ft.ScrollMode.AUTO

    
    editing_id = None

    # Controles del formulario
    nombre = ft.TextField(label="Nombre de la Categoría")
    proveedor_dropdown = ft.Dropdown(label="Proveedor", options=[])
    output = ft.Text("")
    categorias_list = ft.Column()
    botones = ft.Row()  # aquí irán Registrar o Guardar/Cancelar

    def limpiar_campos():
        nombre.value = ""
        proveedor_dropdown.value = None
        output.value = ""

    def actualizar_botones():
        botones.controls.clear()
        if editing_id is None:
            botones.controls.append(
                ft.ElevatedButton("Registrar", on_click=registrar_categoria)
            )
        else:
            botones.controls.append(
                ft.ElevatedButton("Guardar cambios", on_click=guardar_cambios)
            )
            botones.controls.append(
                ft.ElevatedButton("Cancelar", on_click=cancelar_edicion)
            )
        page.update()

    # Carga proveedores para el dropdown
    def cargar_proveedores():
        proveedor_dropdown.options.clear()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_proveedor, nombre FROM Proveedores")
        for id_prov, nombre_prov in cursor.fetchall():
            proveedor_dropdown.options.append(
                ft.dropdown.Option(key=str(id_prov), text=nombre_prov)
            )
        conn.close()
        page.update()

    # Carga lista de categorías
    def cargar_categorias():
        categorias_list.controls.clear()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.id_categoria, c.nombre, p.nombre 
            FROM Categorias c
            JOIN Proveedores p ON c.id_proveedor = p.id_proveedor
        """)
        for id_cat, nombre_cat, nombre_prov in cursor.fetchall():
            categorias_list.controls.append(
                ft.Row([
                    ft.Text(f"{id_cat} - {nombre_cat} ({nombre_prov})", expand=True),
                    ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, i=id_cat: editar_categoria(i)),
                    ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, i=id_cat: eliminar_categoria(i))
                ])
            )
        conn.close()
        page.update()

    # Registrar nueva categoría
    def registrar_categoria(e):
        if not proveedor_dropdown.value:
            output.value = "Selecciona un proveedor."
            page.update()
            return
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Categorias (nombre, id_proveedor) VALUES (%s, %s)",
                (nombre.value, proveedor_dropdown.value)
            )
            conn.commit()
            output.value = "Categoría registrada"
            limpiar_campos()
        except Exception as ex:
            output.value = f"Error: {ex}"
        finally:
            conn.close()
            cargar_categorias()

    # Eliminar categoría
    def eliminar_categoria(id_cat):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Categorias WHERE id_categoria = %s", (id_cat,))
            conn.commit()
            output.value = "Categoría eliminada"
        except Exception as ex:
            output.value = f"Error al eliminar: {ex}"
        finally:
            conn.close()
            cargar_categorias()

    # Pasar a modo edición
    def editar_categoria(id_cat):
        nonlocal editing_id
        editing_id = id_cat
        # Cargo los valores existentes
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT nombre, id_proveedor FROM Categorias WHERE id_categoria = %s",
            (id_cat,)
        )
        result = cursor.fetchone()
        conn.close()
        if result:
            nombre.value, proveedor_dropdown.value = result[0], str(result[1])
        actualizar_botones()

    # Guardar cambios de la edición
    def guardar_cambios(e):
        nonlocal editing_id
        if not proveedor_dropdown.value:
            output.value = "Selecciona un proveedor."
            page.update()
            return
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE Categorias SET nombre=%s, id_proveedor=%s WHERE id_categoria=%s",
                (nombre.value, proveedor_dropdown.value, editing_id)
            )
            conn.commit()
            output.value = "Categoría actualizada"
            limpiar_campos()
            editing_id = None
        except Exception as ex:
            output.value = f"Error al actualizar: {ex}"
        finally:
            conn.close()
            actualizar_botones()
            cargar_categorias()

    # Cancelar la edición
    def cancelar_edicion(e):
        nonlocal editing_id
        limpiar_campos()
        editing_id = None
        output.value = "Edición cancelada"
        actualizar_botones()

    # Montaje del layout
    page.add(
        ft.Text("Registrar / Editar Categoría", size=20, weight="bold"),
        nombre,
        proveedor_dropdown,
        botones,
        output,
        ft.Divider(),
        ft.Text("Lista de Categorías", size=20),
        categorias_list
    )

    # Inicialización
    cargar_proveedores()
    actualizar_botones()
    cargar_categorias()

ft.app(target=main)
