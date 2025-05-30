import flet as ft
from db_connection import get_connection
from datetime import datetime

def main(page: ft.Page):
    page.title = "CRUD de Ventas"
    page.scroll = ft.ScrollMode.AUTO

    # —––––– TextField para ingresar teléfono de cliente, máximo 10 dígitos –––––——
    cliente_field = ft.TextField(
        label="Teléfono Cliente",
        width=180,
        max_length=10,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    cliente_info = ft.Column()  # Aquí se mostrarán los datos del cliente

    empleado_dropdown = ft.Dropdown(label="Empleado", options=[])
    total_text = ft.Text("Total: $0.00", size=16, weight="bold")
    output = ft.Text("")

    venta_items = []
    venta_container = ft.Column()
    ventas_list = ft.Column()

    # Carga empleados (igual que antes)
    def cargar_empleados():
        conn = get_connection(); cursor = conn.cursor()
        cursor.execute("SELECT id_empleado, nombre FROM Empleados")
        empleado_dropdown.options.clear()
        for id_, nombre_ in cursor.fetchall():
            empleado_dropdown.options.append(ft.dropdown.Option(str(id_), nombre_))
        conn.close(); page.update()

    # Artículos (igual que antes)
    def cargar_articulos_dropdown():
        conn = get_connection(); cursor = conn.cursor()
        cursor.execute("SELECT id_articulo, nombre FROM Articulos WHERE stock > 0")
        items = cursor.fetchall(); conn.close()
        return [ft.dropdown.Option(str(id_), nombre_) for id_, nombre_ in items]

    # Al cambiar o enviar el teléfono, carga datos o usa el general
    def on_cliente_change(e):
        tel = cliente_field.value.strip()
        conn = get_connection(); cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clientes WHERE telefono = %s", (tel,))
        row = cursor.fetchone()
        if row:
            cols = [d[0] for d in cursor.description]
            datos = dict(zip(cols, row))
            tel_to_use = tel
        else:
            # cliente general con teléfono fijo
            cursor.execute("SELECT * FROM Clientes WHERE telefono = %s", ("9611560014",))
            row = cursor.fetchone()
            if row:
                cols = [d[0] for d in cursor.description]
                datos = dict(zip(cols, row))
            else:
                datos = {}
            tel_to_use = "9611560014"
        conn.close()

        # Mostrar datos del cliente
        cliente_info.controls.clear()
        cliente_info.controls.append(ft.Text(f"Número usado: {tel_to_use}", weight="bold"))
        for k, v in datos.items():
            cliente_info.controls.append(ft.Text(f"{k}: {v}"))
        page.update()

    cliente_field.on_change = on_cliente_change
    cliente_field.on_submit = on_cliente_change

    # Funciones de venta (idénticas a tu versión, solo adaptando cliente)
    def agregar_articulo_a_venta(e):
        codigo_barras = ft.TextField(label="Código de Barras", width=150)
        dropdown_articulo = ft.Dropdown(label="Artículo", options=cargar_articulos_dropdown(), width=200)
        cantidad = ft.TextField(label="Cantidad", width=80, keyboard_type=ft.KeyboardType.NUMBER)
        precio = ft.TextField(label="Precio Unitario", width=100, disabled=True)
        subtotal = ft.Text("Subtotal: $0.00", width=150)

        def calcular_subtotal(_=None):
            try:
                c = int(cantidad.value); p = float(precio.value)
                subtotal.value = f"Subtotal: ${c * p:.2f}"
            except:
                subtotal.value = "Subtotal: $0.00"
            calcular_total()

        def on_art_change(_):
            if dropdown_articulo.value:
                conn = get_connection(); cursor = conn.cursor()
                cursor.execute(
                    "SELECT codigo_barras, precio_venta FROM Articulos WHERE id_articulo = %s",
                    (dropdown_articulo.value,)
                )
                row = cursor.fetchone(); conn.close()
                if row:
                    codigo_barras.value, precio.value = row[0], f"{float(row[1]):.2f}"
                else:
                    codigo_barras.value, precio.value = "", "0.00"
            else:
                codigo_barras.value, precio.value = "", "0.00"
            calcular_subtotal()

        def on_codigo_change(_):
            if codigo_barras.value:
                conn = get_connection(); cursor = conn.cursor()
                cursor.execute(
                    "SELECT id_articulo, precio_venta FROM Articulos WHERE codigo_barras = %s",
                    (codigo_barras.value,)
                )
                row = cursor.fetchone(); conn.close()
                if row:
                    art_id, unit_price = row
                    dropdown_articulo.value = str(art_id)
                    precio.value = f"{float(unit_price):.2f}"
                else:
                    dropdown_articulo.value, precio.value = None, "0.00"
            else:
                dropdown_articulo.value, precio.value = None, "0.00"
            calcular_subtotal()

        codigo_barras.on_change = on_codigo_change
        dropdown_articulo.on_change = on_art_change
        cantidad.on_change = calcular_subtotal

        fila = ft.Row([
            codigo_barras, dropdown_articulo, cantidad,
            precio, subtotal,
            ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: eliminar_fila(fila))
        ])
        venta_items.append((codigo_barras, dropdown_articulo, cantidad, precio, subtotal))
        venta_container.controls.append(fila)
        page.update()

    def eliminar_fila(fila):
        if fila in venta_container.controls:
            venta_container.controls.remove(fila)
        calcular_total(); page.update()

    def calcular_total():
        total = 0.0
        for _, _, cantidad, precio, _ in venta_items:
            try:
                total += int(cantidad.value) * float(precio.value)
            except:
                pass
        total_text.value = f"Total: ${total:.2f}"
        page.update()

    def cargar_ventas():
        ventas_list.controls.clear()
        conn = get_connection(); cursor = conn.cursor()
        cursor.execute("""
            SELECT v.id_venta,
                   c.nombre AS cliente,
                   e.nombre AS empleado,
                   v.total,
                   DATE_FORMAT(v.fecha_venta, '%Y-%m-%d %H:%i:%s')
            FROM Ventas v
            JOIN Clientes c ON v.telefono_cliente = c.telefono
            JOIN Empleados e ON v.id_empleado = e.id_empleado
            ORDER BY v.fecha_venta DESC
        """)
        for idv, cliente, empleado, total, fecha in cursor.fetchall():
            ventas_list.controls.append(
                ft.Row([
                    ft.Text(f"{idv}", width=40), ft.Text(cliente, expand=1),
                    ft.Text(empleado, expand=1), ft.Text(f"${total:.2f}", width=100),
                    ft.Text(fecha, width=160),
                ])
            )
        conn.close(); page.update()

    def registrar_venta(e):
        if not cliente_field.value or not empleado_dropdown.value:
            output.value = "Ingresa teléfono de cliente y selecciona empleado."
            page.update()
            return
        if not venta_items:
            output.value = "Agrega al menos un artículo."
            page.update()
            return

        # Determinar teléfono a usar
        tel = cliente_field.value.strip()
        conn = get_connection(); cursor = conn.cursor()
        cursor.execute("SELECT telefono FROM Clientes WHERE telefono = %s", (tel,))
        if cursor.fetchone():
            tel_to_use = tel
        else:
            tel_to_use = "9611560014"

        try:
            cursor.execute(
                "INSERT INTO Ventas (telefono_cliente, id_empleado, total, fecha_venta) "
                "VALUES (%s, %s, %s, %s)",
                (
                    tel_to_use,
                    empleado_dropdown.value,
                    float(total_text.value.split('$')[1]),
                    datetime.now()
                )
            )
            id_venta = cursor.lastrowid

            for codigo_barras, dropdown_articulo, cantidad, precio, _ in venta_items:
                art_id = dropdown_articulo.value
                if not art_id and codigo_barras.value:
                    cursor.execute(
                        "SELECT id_articulo FROM Articulos WHERE codigo_barras = %s",
                        (codigo_barras.value,)
                    )
                    row = cursor.fetchone()
                    art_id = row[0] if row else None

                if art_id and cantidad.value:
                    qty = int(cantidad.value)
                    cursor.execute(
                        "SELECT stock FROM Articulos WHERE id_articulo = %s",
                        (art_id,)
                    )
                    available = cursor.fetchone()[0]
                    if qty > available:
                        conn.rollback()
                        output.value = f"Stock insuficiente (quedan {available})."
                        page.update()
                        return

                    cursor.execute(
                        "INSERT INTO Detalles_Venta "
                        "(id_venta, id_articulo, cantidad, subtotal) "
                        "VALUES (%s, %s, %s, %s)",
                        (id_venta, art_id, qty, qty * float(precio.value))
                    )

            conn.commit()
            output.value = "Venta registrada correctamente"
            venta_container.controls.clear(); venta_items.clear()
            total_text.value = "Total: $0.00"
            cargar_ventas()
        except Exception as ex:
            conn.rollback()
            output.value = f"Error: {ex}"
        finally:
            conn.close(); page.update()

    # Construcción de la UI
    page.add(
        ft.Text("Registrar Venta", size=20, weight="bold"),
        ft.Row([cliente_field, cliente_info], alignment=ft.MainAxisAlignment.START),
        empleado_dropdown,
        ft.ElevatedButton("Agregar Artículo", on_click=agregar_articulo_a_venta),
        venta_container,
        total_text,
        ft.Row([
            ft.ElevatedButton("Registrar Venta", on_click=registrar_venta),
            ft.TextButton("Refrescar Ventas", on_click=lambda e: cargar_ventas())
        ]),
        output,
        ft.Divider(),
        ft.Text("Ventas Registradas", size=18, weight="bold"),
        ft.Row([
            ft.Text("ID", width=40, weight="bold"),
            ft.Text("Cliente", expand=1, weight="bold"),
            ft.Text("Empleado", expand=1, weight="bold"),
            ft.Text("Total", width=100, weight="bold"),
            ft.Text("Fecha", width=160, weight="bold"),
        ]),
        ventas_list
    )

    cargar_empleados()
    cargar_ventas()

ft.app(target=main)
