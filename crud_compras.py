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

    # Campos para pago con tarjeta (solo tarjeta)
    numero_tarjeta = ft.TextField(
        label="Número de Tarjeta",
        width=200,
        max_length=16,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    nip_tarjeta = ft.TextField(
        label="NIP",
        width=150,
        max_length=4,
        keyboard_type=ft.KeyboardType.NUMBER,
        password=True,
        can_reveal_password=False
    )

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
        prov_id = proveedor_dropdown.value
        for codigo_barras, dropdown_articulo, cantidad, costo, subtotal in compra_items:
            if prov_id:
                dropdown_articulo.options = cargar_articulos_por_proveedor(prov_id)
            else:
                dropdown_articulo.options = []
            dropdown_articulo.value = None
            codigo_barras.value = ""
            costo.value = "0.00"
            subtotal.value = "Subtotal: $0.00"
        total_text.value = "Total: $0.00"
        page.update()

    proveedor_dropdown.on_change = actualizar_articulos_filas

    # --- Función para mostrar ticket de compra con tarjeta ---
    def mostrar_ticket_tarjeta_compra(proveedor_nombre, empleado_nombre, items, total, numero_tarjeta):
        tarjeta_enmascarada = "**** **** **** " + numero_tarjeta[-4:]
        ticket_content = ft.Column([
            ft.Text("🧾 TICKET DE COMPRA", size=20, weight="bold", text_align=ft.TextAlign.CENTER),
            ft.Divider(),
            ft.Text(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", size=12),
            ft.Text(f"Proveedor: {proveedor_nombre}", size=12),
            ft.Text(f"Empleado: {empleado_nombre}", size=12),
            ft.Text("Método de Pago: 💳 TARJETA", size=12, weight="bold"),
            ft.Text(f"Tarjeta: {tarjeta_enmascarada}", size=12),
            ft.Divider(),
            ft.Text("PRODUCTOS COMPRADOS:", size=14, weight="bold"),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        for item in items:
            ticket_content.controls.append(
                ft.Row([
                    ft.Text(item['nombre'], expand=2),
                    ft.Text(f"{item['cantidad']}", width=40),
                    ft.Text(f"${item['precio']:.2f}", width=60),
                    ft.Text(f"${item['subtotal']:.2f}", width=80),
                ])
            )

        ticket_content.controls.extend([
            ft.Divider(),
            ft.Row([ft.Text("TOTAL:", weight="bold"), ft.Text(f"${total:.2f}", weight="bold")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([ft.Text("PAGADO CON TARJETA:", weight="bold"), ft.Text(f"${total:.2f}", weight="bold")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([ft.Text("CAMBIO:", weight="bold"), ft.Text("$0.00", weight="bold")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            ft.Text("TRANSACCIÓN APROBADA ✅", size=12, weight="bold", color=ft.colors.GREEN),
            ft.Text("¡Compra registrada con éxito!", size=14, weight="bold", text_align=ft.TextAlign.CENTER),
        ])

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Compra Completada - Tarjeta"),
            content=ft.Container(
                content=ticket_content,
                width=350,
                height=450,
                padding=10,
                bgcolor=ft.colors.WHITE,
                border=ft.border.all(1, ft.colors.GREY_400)
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: page.close(dlg))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(dlg)

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
            disabled=True
        )
        subtotal = ft.Text("Subtotal: $0.00", width=150)

        def calcular_subtotal(_=None):
            try:
                c = int(cantidad.value)
                u = float(costo.value)
                subtotal.value = f"Subtotal: ${c * u:.2f}"
            except:
                subtotal.value = "Subtotal: $0.00"
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
        for tupla in compra_items:
            if tupla[0] in fila.controls:
                compra_items.remove(tupla)
                break
        compra_container.controls.remove(fila)
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

        # Validación de tarjeta
        if not numero_tarjeta.value or len(numero_tarjeta.value) < 16:
            output.value = "Ingresa un número de tarjeta válido (16 dígitos)."
            page.update(); return
        if not nip_tarjeta.value or len(nip_tarjeta.value) < 4:
            output.value = "Ingresa un NIP válido (4 dígitos)."
            page.update(); return

        total_compra = float(total_text.value.split('$')[1])
        conn = get_connection(); cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Compras (id_proveedor, id_empleado, total, fecha_compra) "
                "VALUES (%s, %s, %s, %s)",
                (
                    proveedor_dropdown.value,
                    empleado_dropdown.value,
                    total_compra,
                    datetime.now()
                )
            )
            id_compra = cursor.lastrowid

            # Preparar datos para el ticket
            items_ticket = []

            for codigo_barras, dropdown_articulo, cantidad, costo, subtotal in compra_items:
                art_id = dropdown_articulo.value
                if not art_id and codigo_barras.value:
                    cursor.execute("SELECT id_articulo FROM Articulos WHERE codigo_barras = %s", (codigo_barras.value,))
                    row = cursor.fetchone()
                    art_id = row[0] if row else None
                if art_id and cantidad.value:
                    qty = int(cantidad.value)
                    cursor.execute("SELECT nombre FROM Articulos WHERE id_articulo = %s", (art_id,))
                    nombre_articulo = cursor.fetchone()[0]
                    unit_cost = float(costo.value)
                    subtotal_item = qty * unit_cost
                    items_ticket.append({
                        'nombre': nombre_articulo,
                        'cantidad': qty,
                        'precio': unit_cost,
                        'subtotal': subtotal_item
                    })
                    cursor.execute(
                        "INSERT INTO Detalles_Compra (id_compra, id_articulo, cantidad, costo_unitario, subtotal) "
                        "VALUES (%s, %s, %s, %s, %s)",
                        (id_compra, art_id, qty, unit_cost, subtotal_item)
                    )

            conn.commit()

            # Obtener nombres para el ticket
            cursor.execute("SELECT nombre FROM Proveedores WHERE id_proveedor = %s", (proveedor_dropdown.value,))
            proveedor_nombre = cursor.fetchone()[0]
            cursor.execute("SELECT nombre FROM Empleados WHERE id_empleado = %s", (empleado_dropdown.value,))
            empleado_nombre = cursor.fetchone()[0]

            output.value = "Compra registrada correctamente"
            mostrar_ticket_tarjeta_compra(proveedor_nombre, empleado_nombre, items_ticket, total_compra, numero_tarjeta.value)

            # Limpiar formulario
            compra_container.controls.clear()
            compra_items.clear()
            total_text.value = "Total: $0.00"
            numero_tarjeta.value = ""
            nip_tarjeta.value = ""
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
        ft.Divider(),
        ft.Text("Pago con Tarjeta", size=16, weight="bold"),
        numero_tarjeta,
        nip_tarjeta,
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
