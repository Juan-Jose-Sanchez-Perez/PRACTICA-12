import flet as ft
from db_connection import get_connection

def main(page: ft.Page):
    page.title = "CRUD Artículos"
    page.scroll = ft.ScrollMode.AUTO

    # Estado de edición: None = modo registro, sino = id del artículo a editar
    editing_id = None

    # Controles del formulario
    nombre = ft.TextField(label="Nombre del Artículo")
    codigo_barras = ft.TextField(
        label="Código de Barras",
        hint_text="Máx. 14 caracteres",
        max_length=14,
        width=200
    )
    descripcion = ft.TextField(label="Descripción")
    precio = ft.TextField(label="Precio de venta", keyboard_type=ft.KeyboardType.NUMBER)
    precio_unitario_proveedor = ft.TextField(
        label="Precio Unitario Proveedor",
        keyboard_type=ft.KeyboardType.NUMBER
    )
    stock = ft.TextField(label="Stock", keyboard_type=ft.KeyboardType.NUMBER)
    fecha_caducidad = ft.TextField(label="Fecha de caducidad (YYYY-MM-DD)")
    categoria_dropdown = ft.Dropdown(label="Categoría", options=[])
    output = ft.Text("")
    articulos_list = ft.Column()
    botones = ft.Row()  # Registrar / Guardar+Cancelar

    def limpiar_campos():
        nombre.value = codigo_barras.value = descripcion.value = ""
        precio.value = precio_unitario_proveedor.value = stock.value = ""
        fecha_caducidad.value = ""
        categoria_dropdown.value = None
        output.value = ""

    def actualizar_botones():
        botones.controls.clear()
        if editing_id is None:
            botones.controls.append(ft.ElevatedButton("Registrar", on_click=registrar_articulo))
        else:
            botones.controls.append(ft.ElevatedButton("Guardar cambios", on_click=guardar_cambios))
            botones.controls.append(ft.ElevatedButton("Cancelar", on_click=cancelar_edicion))
        page.update()

    def cargar_categorias():
        categoria_dropdown.options.clear()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_categoria, nombre FROM Categorias")
        for id_cat, nombre_cat in cursor.fetchall():
            categoria_dropdown.options.append(
                ft.dropdown.Option(key=str(id_cat), text=nombre_cat)
            )
        conn.close()
        page.update()

    def cargar_articulos():
        articulos_list.controls.clear()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id_articulo,
                   a.nombre,
                   a.codigo_barras,
                   a.precio_venta,
                   a.precio_unitario_proveedor,
                   a.stock,
                   c.nombre,
                   a.fecha_caducidad
              FROM Articulos a
              JOIN Categorias c ON a.id_categoria = c.id_categoria
        """)
        for (id_art, nom, cb, pv, puprov, stk, cat_nombre, cad) in cursor.fetchall():
            articulos_list.controls.append(
                ft.Row([
                    ft.Text(
                        f"{id_art} – {nom} – [{cb}] – "
                        f"Venta: ${pv:.2f} – Prov: ${puprov:.2f} – "
                        f"Stock: {stk}u – {cat_nombre} – {cad}",
                        expand=True
                    ),
                    ft.IconButton(icon=ft.icons.EDIT,   on_click=lambda e, i=id_art: editar_articulo(i)),
                    ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, i=id_art: eliminar_articulo(i))
                ])
            )
        conn.close()
        page.update()

    def registrar_articulo(e):
        # Validaciones básicas
        if not codigo_barras.value:
            output.value = "El código de barras es obligatorio."
            page.update()
            return
        if not categoria_dropdown.value:
            output.value = "Selecciona una categoría."
            page.update()
            return

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Articulos
                  (nombre,
                   codigo_barras,
                   descripcion,
                   precio_venta,
                   precio_unitario_proveedor,
                   stock,
                   id_categoria,
                   fecha_caducidad)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                nombre.value,
                codigo_barras.value,
                descripcion.value,
                float(precio.value),
                float(precio_unitario_proveedor.value),
                int(stock.value),
                categoria_dropdown.value,
                fecha_caducidad.value
            ))
            conn.commit()
            output.value = "Artículo registrado"
            limpiar_campos()
        except Exception as ex:
            output.value = f"Error: {ex}"
        finally:
            conn.close()
            cargar_articulos()

    def eliminar_articulo(id_art):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Articulos WHERE id_articulo = %s", (id_art,))
            conn.commit()
            output.value = "Artículo eliminado"
        except Exception as ex:
            output.value = f"Error al eliminar: {ex}"
        finally:
            conn.close()
            cargar_articulos()

    def editar_articulo(id_art):
        nonlocal editing_id
        editing_id = id_art
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nombre,
                   codigo_barras,
                   descripcion,
                   precio_venta,
                   precio_unitario_proveedor,
                   stock,
                   id_categoria,
                   fecha_caducidad
              FROM Articulos
             WHERE id_articulo = %s
        """, (id_art,))
        result = cursor.fetchone()
        conn.close()
        if result:
            nombre.value, codigo_barras.value, descripcion.value = result[0], result[1], result[2]
            precio.value = str(result[3])
            precio_unitario_proveedor.value = str(result[4])
            stock.value = str(result[5])
            categoria_dropdown.value = str(result[6])
            fecha_caducidad.value = str(result[7])
        actualizar_botones()

    def guardar_cambios(e):
        nonlocal editing_id
        # Validaciones
        if not codigo_barras.value:
            output.value = "El código de barras es obligatorio."
            page.update()
            return
        if not categoria_dropdown.value:
            output.value = "Selecciona una categoría."
            page.update()
            return

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE Articulos
                   SET nombre=%s,
                       codigo_barras=%s,
                       descripcion=%s,
                       precio_venta=%s,
                       precio_unitario_proveedor=%s,
                       stock=%s,
                       id_categoria=%s,
                       fecha_caducidad=%s
                 WHERE id_articulo=%s
            """, (
                nombre.value,
                codigo_barras.value,
                descripcion.value,
                float(precio.value),
                float(precio_unitario_proveedor.value),
                int(stock.value),
                categoria_dropdown.value,
                fecha_caducidad.value,
                editing_id
            ))
            conn.commit()
            output.value = "Artículo actualizado"
            limpiar_campos()
            editing_id = None
        except Exception as ex:
            output.value = f"Error al actualizar: {ex}"
        finally:
            conn.close()
            actualizar_botones()
            cargar_articulos()

    def cancelar_edicion(e):
        nonlocal editing_id
        limpiar_campos()
        editing_id = None
        output.value = "Edición cancelada"
        actualizar_botones()

    # Configuración de la UI
    page.add(
        ft.Text("Registrar / Editar Artículo", size=20, weight="bold"),
        nombre,
        codigo_barras,
        descripcion,
        precio,
        precio_unitario_proveedor,
        stock,
        fecha_caducidad,
        categoria_dropdown,
        botones,
        output,
        ft.Divider(),
        ft.Text("Lista de Artículos", size=20),
        articulos_list
    )

    # Inicialización
    cargar_categorias()
    actualizar_botones()
    cargar_articulos()

ft.app(target=main)
