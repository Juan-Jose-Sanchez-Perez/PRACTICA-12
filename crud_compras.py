import flet as ft
from db_connection import get_connection
from datetime import datetime

def main(page: ft.Page):
    page.title = "CRUD de Compras"
    page.scroll = ft.ScrollMode.AUTO

    # Controles de selección
    proveedor_dropdown = ft.Dropdown(label="Proveedor", options=[])
    empleado_dropdown  = ft.Dropdown(label="Empleado",  options=[])
    total_text         = ft.Text("Total: $0.00", size=16, weight="bold")
    output             = ft.Text("")

    # Filas de ítems a comprar y contenedor
    # Ahora almacenamos tuplas (codigo_barras, dropdown_articulo, cantidad, costo, subtotal)
    compra_items     = []
    compra_container = ft.Column()

    # Lista de compras ya registradas
    compras_list = ft.Column()

    # --- Carga de datos para selects ---
    def cargar_proveedores():
        conn = get_connection(); cursor = conn.cursor()
        cursor.execute("SELECT id_proveedor, nombre FROM Proveedores")
        proveedor_dropdown.options.clear()
        for id_, nombre_ in cursor.fetchall():
            proveedor_dropdown.options.append(ft.dropdown.Option(str(id_), nombre_))
        conn.close()
        page.update()

    def cargar_empleados():
        conn = get_connection(); cursor = conn.cursor()
        cursor.execute("SELECT id_empleado, nombre FROM Empleados")
        empleado_dropdown.options.clear()
        for id_, nombre_ in cursor.fetchall():
            empleado_dropdown.options.append(ft.dropdown.Option(str(id_), nombre_))
        conn.close()
        page.update()

    # Devuelve opciones de artículos según categoría->proveedor
    def cargar_articulos_por_proveedor(id_prov):
        conn = get_connection(); cursor = conn.cursor()
        cursor.execute(
            "SELECT a.id_articulo, a.nombre "
            "FROM Articulos a "
            "JOIN Categorias c ON a.id_categoria = c.id_categoria "
            "WHERE c.id_proveedor = %s",
            (id_prov,)
        )
        items = cursor.fetchall()
        conn.close()
        return [ft.dropdown.Option(str(id_), nombre_) for id_, nombre_ in items]

    # Cuando cambia el proveedor, actualizamos cada fila existente:
    def actualizar_articulos_filas(_=None):
        # Si no hay proveedor seleccionado, dejamos todos los dropdown_articulo vacíos
        prov_id = proveedor_dropdown.value
        for codigo_barras, dropdown_articulo, cantidad, costo, subtotal in compra_items:
            # Actualizamos opciones
            if prov_id:
                dropdown_articulo.options = cargar_articulos_por_proveedor(prov_id)
            else:
                dropdown_articulo.options = []
            # Limpiar valor y campos relacionados
            dropdown_articulo.value = None
            codigo_barras.value = ""
            costo.value = "0.00"
            subtotal.value = "Subtotal: $0.00"
        # Recalcular total general (queda en cero si limpiamos filas)
        total_text.value = "Total: $0.00"
        page.update()

    proveedor_dropdown.on_change = actualizar_articulos_filas

    # --- Agregar fila de detalle de compra ---
    def agregar_articulo_a_compra(e):
        if not proveedor_dropdown.value:
            output.value = "Selecciona primero un proveedor."
            page.update()
            return

        codigo_barras = ft.TextField(label="Código de Barras", width=150)
        dropdown_articulo = ft.Dropdown(
            label="Artículo",
            options=cargar_articulos_por_proveedor(proveedor_dropdown.value),
            width=200
        )
        cantidad = ft.TextField(
            label="Cantidad", width=80, keyboard_type=ft.KeyboardType.NUMBER
        )
        costo = ft.TextField(
            label="Costo Unitario",
            width=100,
            disabled=True  # se rellena automáticamente
        )
        subtotal = ft.Text("Subtotal: $0.00", width=150)

        def calcular_subtotal(_=None):
            try:
                c = int(cantidad.value)
                u = float(costo.value)
                subtotal.value = f"Subtotal: ${c * u:.2f}"
            except:
                subtotal.value = "Subtotal: $0.00"
            # recalcular total general
            total = 0.0
            for _, _, ct, cs, _ in compra_items:
                try:
                    total += int(ct.value) * float(cs.value)
                except:
                    pass
            total_text.value = f"Total: ${total:.2f}"
            page.update()

        def on_articulo_change(_):
            if dropdown_articulo.value:
                conn = get_connection(); cursor = conn.cursor()
                cursor.execute(
                    "SELECT codigo_barras, precio_unitario_proveedor "
                    "FROM Articulos WHERE id_articulo = %s",
                    (dropdown_articulo.value,)
                )
                row = cursor.fetchone(); conn.close()
                if row:
                    codigo_barras.value = row[0]
                    costo.value = f"{float(row[1]):.2f}"
                else:
                    codigo_barras.value = ""
                    costo.value = "0.00"
            else:
                codigo_barras.value = ""
                costo.value = "0.00"
            calcular_subtotal()

        def on_codigo_change(_):
            if codigo_barras.value:
                conn = get_connection(); cursor = conn.cursor()
                cursor.execute(
                    "SELECT a.id_articulo, a.precio_unitario_proveedor "
                    "FROM Articulos a "
                    "JOIN Categorias c ON a.id_categoria = c.id_categoria "
                    "WHERE a.codigo_barras = %s AND c.id_proveedor = %s",
                    (codigo_barras.value, proveedor_dropdown.value)
                )
                row = cursor.fetchone(); conn.close()
                if row:
                    art_id, unit_cost = row
                    dropdown_articulo.value = str(art_id)
                    costo.value = f"{float(unit_cost):.2f}"
                else:
                    dropdown_articulo.value = None
                    costo.value = "0.00"
            else:
                dropdown_articulo.value = None
                costo.value = "0.00"
            calcular_subtotal()

        # Asignar handlers
        dropdown_articulo.on_change = on_articulo_change
        codigo_barras.on_change = on_codigo_change
        cantidad.on_change = calcular_subtotal

        fila = ft.Row([
            codigo_barras,
            dropdown_articulo,
            cantidad,
            costo,
            subtotal,
            ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: eliminar_fila(fila))
        ])

        compra_items.append((codigo_barras, dropdown_articulo, cantidad, costo, subtotal))
        compra_container.controls.append(fila)
        page.update()

    def eliminar_fila(fila):
        # Encontrar y remover la tupla correspondiente en compra_items
        for tupla in compra_items:
            if tupla[0] in fila.controls:  # tupla[0] es codigo_barras
                compra_items.remove(tupla)
                break

        compra_container.controls.remove(fila)
        # recalcular total
        total = 0.0
        for _, _, ct, cs, _ in compra_items:
            try:
                total += int(ct.value) * float(cs.value)
            except:
                pass
        total_text.value = f"Total: ${total:.2f}"
        page.update()

    # --- Registro de compra y refresco ---
    def registrar_compra(e):
        if not proveedor_dropdown.value or not empleado_dropdown.value:
            output.value = "Selecciona proveedor y empleado."
            page.update(); return
        if not compra_items:
            output.value = "Agrega al menos un artículo."
            page.update(); return

        conn = get_connection(); cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Compras (id_proveedor, id_empleado, total, fecha_compra) "
                "VALUES (%s, %s, %s, %s)",
                (
                    proveedor_dropdown.value,
                    empleado_dropdown.value,
                    float(total_text.value.split('$')[1]),
                    datetime.now()
                )
            )
            id_compra = cursor.lastrowid

            for codigo_barras, dropdown_articulo, cantidad, costo, subtotal in compra_items:
                art_id = None
                # obtener id_articulo desde código o dropdown
                if codigo_barras.value:
                    cursor.execute(
                        "SELECT id_articulo FROM Articulos WHERE codigo_barras = %s",
                        (codigo_barras.value,)
                    )
                    row = cursor.fetchone()
                    if row:
                        art_id = row[0]
                if art_id and cantidad.value:
                    qty       = int(cantidad.value)
                    unit_cost = float(costo.value)
                    cursor.execute(
                        """INSERT INTO Detalles_Compra
                             (id_compra, id_articulo, cantidad, costo_unitario, subtotal)
                           VALUES (%s, %s, %s, %s, %s)""",
                        (
                            id_compra,
                            art_id,
                            qty,
                            unit_cost,
                            qty * unit_cost
                        )
                    )

            conn.commit()
            output.value = "Compra registrada correctamente"
            compra_container.controls.clear()
            compra_items.clear()
            total_text.value = "Total: $0.00"
            cargar_compras()
        except Exception as ex:
            conn.rollback()
            output.value = f"Error: {ex}"
        finally:
            conn.close()
            page.update()

    # --- Eliminar compra ---
    def eliminar_compra(id_compra):
        conn = get_connection(); cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Detalles_Compra WHERE id_compra = %s", (id_compra,))
            cursor.execute("DELETE FROM Compras         WHERE id_compra = %s", (id_compra,))
            conn.commit()
            output.value = f"Compra {id_compra} eliminada"
            cargar_compras()
        except Exception as ex:
            conn.rollback()
            output.value = f"Error al eliminar compra: {ex}"
        finally:
            conn.close()
            page.update()

    # --- Listado de compras ---
    def cargar_compras():
        compras_list.controls.clear()
        conn = get_connection(); cursor = conn.cursor()
        cursor.execute("""
            SELECT c.id_compra,
                   p.nombre  AS proveedor,
                   e.nombre  AS empleado,
                   c.total,
                   DATE_FORMAT(c.fecha_compra, '%Y-%m-%d %H:%i:%s')
              FROM Compras c
              JOIN Proveedores p ON c.id_proveedor = p.id_proveedor
              JOIN Empleados  e ON c.id_empleado  = e.id_empleado
          ORDER BY c.fecha_compra DESC
        """)
        for idc, prov, emp, tot, fecha in cursor.fetchall():
            compras_list.controls.append(
                ft.Row([
                    ft.Text(str(idc), width=40),
                    ft.Text(prov, expand=1),
                    ft.Text(emp, expand=1),
                    ft.Text(f"${tot:.2f}", width=100),
                    ft.Text(fecha, width=160),
                    ft.IconButton(icon=ft.icons.DELETE, tooltip="Eliminar compra",
                                  on_click=lambda e, i=idc: eliminar_compra(i))
                ], alignment=ft.MainAxisAlignment.START)
            )
        conn.close()
        page.update()

    # --- Construcción de la UI ---
    page.add(
        ft.Text("Registrar Compra", size=20, weight="bold"),
        proveedor_dropdown,
        empleado_dropdown,
        ft.ElevatedButton("Agregar Artículo", on_click=agregar_articulo_a_compra),
        compra_container,
        total_text,
        ft.Row([
            ft.ElevatedButton("Registrar Compra", on_click=registrar_compra),
            ft.TextButton("Refrescar Compras", on_click=lambda e: cargar_compras())
        ]),
        output,
        ft.Divider(),
        ft.Text("Compras Registradas", size=18, weight="bold"),
        ft.Row([
            ft.Text("ID", width=40, weight="bold"),
            ft.Text("Proveedor", expand=1, weight="bold"),
            ft.Text("Empleado", expand=1, weight="bold"),
            ft.Text("Total", width=100, weight="bold"),
            ft.Text("Fecha", width=160, weight="bold"),
            ft.Text("Acciones", width=80, weight="bold"),
        ]),
        compras_list
    )

    # Inicialización
    cargar_proveedores()
    cargar_empleados()
    cargar_compras()

ft.app(target=main)
