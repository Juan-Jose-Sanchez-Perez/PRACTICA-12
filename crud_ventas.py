import flet as ft
from db_connection import get_connection
from datetime import datetime

def main(page: ft.Page):
    page.title = "CRUD de Ventas"
    page.scroll = ft.ScrollMode.AUTO

    # Contenedor principal de tabs
    tabs = ft.Tabs(tabs=[], expand=1)

    def cargar_ventas(lista):
        lista.controls.clear()
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
            lista.controls.append(
                ft.Row([
                    ft.Text(f"{idv}", width=40),
                    ft.Text(cliente, expand=1),
                    ft.Text(empleado, expand=1),
                    ft.Text(f"${total:.2f}", width=100),
                    ft.Text(fecha, width=160),
                ])
            )
        conn.close(); page.update()

    def mostrar_ticket_efectivo(cliente_nombre, empleado_nombre, items, total, pago_efectivo, cambio):
        """Muestra ventana emergente con el ticket de venta en efectivo"""
        
        # Crear contenido del ticket
        ticket_content = ft.Column([
            ft.Text("🧾 TICKET DE VENTA", size=20, weight="bold", text_align=ft.TextAlign.CENTER),
            ft.Divider(),
            ft.Text(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", size=12),
            ft.Text(f"Cliente: {cliente_nombre}", size=12),
            ft.Text(f"Empleado: {empleado_nombre}", size=12),
            ft.Text("Método de Pago: 💰 EFECTIVO", size=12, weight="bold"),
            ft.Divider(),
            ft.Text("PRODUCTOS:", size=14, weight="bold"),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        # Agregar items del ticket
        for item in items:
            ticket_content.controls.append(
                ft.Row([
                    ft.Text(item['nombre'], expand=2),
                    ft.Text(f"{item['cantidad']}", width=40),
                    ft.Text(f"${item['precio']:.2f}", width=60),
                    ft.Text(f"${item['subtotal']:.2f}", width=80),
                ])
            )
        
        # Agregar totales
        ticket_content.controls.extend([
            ft.Divider(),
            ft.Row([ft.Text("TOTAL:", weight="bold"), ft.Text(f"${total:.2f}", weight="bold")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([ft.Text("EFECTIVO RECIBIDO:"), ft.Text(f"${pago_efectivo:.2f}")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([ft.Text("CAMBIO:", weight="bold"), ft.Text(f"${cambio:.2f}", weight="bold")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            ft.Text("¡Gracias por su compra!", size=14, weight="bold", text_align=ft.TextAlign.CENTER),
        ])
        
        # Crear diálogo
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Venta Completada - Efectivo"),
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

    def mostrar_ticket_tarjeta(cliente_nombre, empleado_nombre, items, total, numero_tarjeta):
        """Muestra ventana emergente con el ticket de venta con tarjeta"""
        
        # Enmascarar número de tarjeta (mostrar solo últimos 4 dígitos)
        tarjeta_enmascarada = "**** **** **** " + numero_tarjeta[-4:]
        
        # Crear contenido del ticket
        ticket_content = ft.Column([
            ft.Text("🧾 TICKET DE VENTA", size=20, weight="bold", text_align=ft.TextAlign.CENTER),
            ft.Divider(),
            ft.Text(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", size=12),
            ft.Text(f"Cliente: {cliente_nombre}", size=12),
            ft.Text(f"Empleado: {empleado_nombre}", size=12),
            ft.Text("Método de Pago: 💳 TARJETA", size=12, weight="bold"),
            ft.Text(f"Tarjeta: {tarjeta_enmascarada}", size=12),
            ft.Divider(),
            ft.Text("PRODUCTOS:", size=14, weight="bold"),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        # Agregar items del ticket
        for item in items:
            ticket_content.controls.append(
                ft.Row([
                    ft.Text(item['nombre'], expand=2),
                    ft.Text(f"{item['cantidad']}", width=40),
                    ft.Text(f"${item['precio']:.2f}", width=60),
                    ft.Text(f"${item['subtotal']:.2f}", width=80),
                ])
            )
        
        # Agregar totales (sin cambio para tarjeta)
        ticket_content.controls.extend([
            ft.Divider(),
            ft.Row([ft.Text("TOTAL:", weight="bold"), ft.Text(f"${total:.2f}", weight="bold")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([ft.Text("PAGADO CON TARJETA:", weight="bold"), ft.Text(f"${total:.2f}", weight="bold")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([ft.Text("CAMBIO:", weight="bold"), ft.Text("$0.00", weight="bold")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            ft.Text("TRANSACCIÓN APROBADA ✅", size=12, weight="bold", color=ft.colors.GREEN),
            ft.Text("¡Gracias por su compra!", size=14, weight="bold", text_align=ft.TextAlign.CENTER),
        ])
        
        # Crear diálogo
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Venta Completada - Tarjeta"),
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

    def nueva_venta_tab(e=None):
        tab_index = len(tabs.tabs) + 1

        cliente_field = ft.TextField(label="Teléfono Cliente", width=180, max_length=10, keyboard_type=ft.KeyboardType.NUMBER)
        cliente_info = ft.Column()
        empleado_dropdown = ft.Dropdown(label="Empleado", options=[])
        total_text = ft.Text("Total: $0.00", size=16, weight="bold")
        output = ft.Text("")
        venta_items = []
        venta_container = ft.Column()
        ventas_list = ft.Column()

        # ===== CAMPOS DE MÉTODO DE PAGO =====
        metodo_pago = ft.Dropdown(
            label="Método de Pago",
            options=[
                ft.dropdown.Option("efectivo", "💰 Efectivo"),
                ft.dropdown.Option("tarjeta", "💳 Tarjeta")
            ],
            width=200,
            value="efectivo"
        )
        
        # Campos para tarjeta
        tarjeta_container = ft.Column(visible=False)
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
            password=True,  # Esto hace que se muestren asteriscos automáticamente
            can_reveal_password=False
        )
        
        # Campos para efectivo
        efectivo_container = ft.Column(visible=True)
        monto_efectivo = ft.TextField(
            label="Monto Recibido ($)",
            width=150,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        cambio_text = ft.Text("Cambio: $0.00", size=14, weight="bold", color=ft.colors.GREEN)
        
        # Función para calcular cambio
        def calcular_cambio(e=None):
            try:
                total = float(total_text.value.split('$')[1])
                efectivo = float(monto_efectivo.value) if monto_efectivo.value else 0
                cambio = max(0, efectivo - total)
                cambio_text.value = f"Cambio: ${cambio:.2f}"
                cambio_text.color = ft.colors.GREEN if cambio >= 0 else ft.colors.RED
            except:
                cambio_text.value = "Cambio: $0.00"
                cambio_text.color = ft.colors.GREY
            page.update()
        
        monto_efectivo.on_change = calcular_cambio
        
        # Configurar containers de pago
        tarjeta_container.controls = [
            ft.Text("Datos de Tarjeta:", weight="bold"),
            numero_tarjeta,
            nip_tarjeta
        ]
        
        efectivo_container.controls = [
            ft.Text("Pago en Efectivo:", weight="bold"),
            monto_efectivo,
            cambio_text
        ]
        
        # Función para cambiar método de pago
        def cambiar_metodo_pago(e):
            if metodo_pago.value == "tarjeta":
                tarjeta_container.visible = True
                efectivo_container.visible = False
            else:
                tarjeta_container.visible = False
                efectivo_container.visible = True
            page.update()
        
        metodo_pago.on_change = cambiar_metodo_pago

        def cargar_empleados():
            conn = get_connection(); cursor = conn.cursor()
            cursor.execute("SELECT id_empleado, nombre FROM Empleados")
            empleado_dropdown.options.clear()
            for id_, nombre_ in cursor.fetchall():
                empleado_dropdown.options.append(ft.dropdown.Option(str(id_), nombre_))
            conn.close(); page.update()

        def cargar_articulos_dropdown():
            conn = get_connection(); cursor = conn.cursor()
            cursor.execute("SELECT id_articulo, nombre FROM Articulos WHERE stock > 0")
            items = cursor.fetchall(); conn.close()
            return [ft.dropdown.Option(str(id_), nombre_) for id_, nombre_ in items]

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
                cursor.execute("SELECT * FROM Clientes WHERE telefono = %s", ("9611560014",))
                row = cursor.fetchone()
                if row:
                    cols = [d[0] for d in cursor.description]
                    datos = dict(zip(cols, row))
                else:
                    datos = {}
                tel_to_use = "9611560014"
            conn.close()

            cliente_info.controls.clear()
            cliente_info.controls.append(ft.Text(f"Número usado: {tel_to_use}", weight="bold"))
            for k, v in datos.items():
                cliente_info.controls.append(ft.Text(f"{k}: {v}"))
            page.update()

        cliente_field.on_change = on_cliente_change
        cliente_field.on_submit = on_cliente_change

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
                    cursor.execute("SELECT codigo_barras, precio_venta FROM Articulos WHERE id_articulo = %s", (dropdown_articulo.value,))
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
                    cursor.execute("SELECT id_articulo, precio_venta FROM Articulos WHERE codigo_barras = %s", (codigo_barras.value,))
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

            fila = ft.Row([codigo_barras, dropdown_articulo, cantidad, precio, subtotal, ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: eliminar_fila(fila))])
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
            # Recalcular cambio si es efectivo
            if metodo_pago.value == "efectivo":
                calcular_cambio()
            page.update()

        def registrar_venta(e):
            # Validaciones básicas
            if not cliente_field.value or not empleado_dropdown.value:
                output.value = "Ingresa teléfono de cliente y selecciona empleado."; page.update(); return
            if not venta_items:
                output.value = "Agrega al menos un artículo."; page.update(); return
            
            # Validaciones de método de pago
            total_venta = float(total_text.value.split('$')[1])
            
            if metodo_pago.value == "tarjeta":
                if not numero_tarjeta.value or len(numero_tarjeta.value) < 16:
                    output.value = "Ingresa un número de tarjeta válido (16 dígitos)."; page.update(); return
                if not nip_tarjeta.value or len(nip_tarjeta.value) < 4:
                    output.value = "Ingresa un NIP válido (4 dígitos)."; page.update(); return
            else:  # efectivo
                if not monto_efectivo.value:
                    output.value = "Ingresa el monto recibido en efectivo."; page.update(); return
                efectivo_recibido = float(monto_efectivo.value)
                if efectivo_recibido < total_venta:
                    output.value = "El monto en efectivo es insuficiente."; page.update(); return
            
            tel = cliente_field.value.strip()
            conn = get_connection(); cursor = conn.cursor()
            cursor.execute("SELECT telefono FROM Clientes WHERE telefono = %s", (tel,))
            tel_to_use = tel if cursor.fetchone() else "9611560014"
            
            try:
                cursor.execute("INSERT INTO Ventas (telefono_cliente, id_empleado, total, fecha_venta) VALUES (%s, %s, %s, %s)", 
                             (tel_to_use, empleado_dropdown.value, total_venta, datetime.now()))
                id_venta = cursor.lastrowid
                
                # Preparar datos para el ticket
                items_ticket = []
                
                for codigo_barras, dropdown_articulo, cantidad, precio, _ in venta_items:
                    art_id = dropdown_articulo.value
                    if not art_id and codigo_barras.value:
                        cursor.execute("SELECT id_articulo FROM Articulos WHERE codigo_barras = %s", (codigo_barras.value,))
                        row = cursor.fetchone(); art_id = row[0] if row else None
                    if art_id and cantidad.value:
                        qty = int(cantidad.value)
                        cursor.execute("SELECT stock FROM Articulos WHERE id_articulo = %s", (art_id,))
                        available = cursor.fetchone()[0]
                        if qty > available:
                            conn.rollback(); output.value = f"Stock insuficiente (quedan {available})."; page.update(); return
                        
                        # Obtener nombre del artículo para el ticket
                        cursor.execute("SELECT nombre FROM Articulos WHERE id_articulo = %s", (art_id,))
                        nombre_articulo = cursor.fetchone()[0]
                        
                        subtotal_item = qty * float(precio.value)
                        items_ticket.append({
                            'nombre': nombre_articulo,
                            'cantidad': qty,
                            'precio': float(precio.value),
                            'subtotal': subtotal_item
                        })
                        
                        cursor.execute("INSERT INTO Detalles_Venta (id_venta, id_articulo, cantidad, subtotal) VALUES (%s, %s, %s, %s)", 
                                     (id_venta, art_id, qty, subtotal_item))
                
                conn.commit()
                
                # Obtener nombres para el ticket
                cursor.execute("SELECT nombre FROM Clientes WHERE telefono = %s", (tel_to_use,))
                cliente_nombre = cursor.fetchone()[0]
                cursor.execute("SELECT nombre FROM Empleados WHERE id_empleado = %s", (empleado_dropdown.value,))
                empleado_nombre = cursor.fetchone()[0]
                
                output.value = "Venta registrada correctamente"
                
                # Mostrar ticket según el método de pago
                if metodo_pago.value == "efectivo":
                    efectivo_recibido = float(monto_efectivo.value)
                    cambio = efectivo_recibido - total_venta
                    mostrar_ticket_efectivo(cliente_nombre, empleado_nombre, items_ticket, total_venta, efectivo_recibido, cambio)
                else:  # tarjeta
                    mostrar_ticket_tarjeta(cliente_nombre, empleado_nombre, items_ticket, total_venta, numero_tarjeta.value)
                
                # Limpiar formulario
                venta_container.controls.clear(); venta_items.clear(); total_text.value = "Total: $0.00"
                numero_tarjeta.value = ""; nip_tarjeta.value = ""; monto_efectivo.value = ""
                cambio_text.value = "Cambio: $0.00"
                cargar_ventas(ventas_list)
                
                # Cerrar tab automáticamente
                tabs.tabs.pop(tabs.selected_index)
                tabs.selected_index = max(tabs.selected_index - 1, 0)
                
            except Exception as ex:
                conn.rollback(); output.value = f"Error: {ex}"
            finally:
                conn.close(); page.update()

        cargar_empleados()

        tab_content = ft.Column([
            ft.Text(f"Formulario Venta {tab_index}", size=18, weight="bold"),
            ft.Row([cliente_field, cliente_info], alignment=ft.MainAxisAlignment.START),
            empleado_dropdown,
            ft.ElevatedButton("Agregar Artículo", on_click=agregar_articulo_a_venta),
            venta_container,
            total_text,
            ft.Divider(),
            ft.Text("Método de Pago", size=16, weight="bold"),
            metodo_pago,
            tarjeta_container,
            efectivo_container,
            ft.Row([
                ft.ElevatedButton("Registrar Venta", on_click=registrar_venta),
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
        ])

        cargar_ventas(ventas_list)
        nueva_tab = ft.Tab(text=f"Venta {tab_index}", content=tab_content)
        tabs.tabs.append(nueva_tab)
        tabs.selected_index = len(tabs.tabs) - 1
        page.update()

    page.add(
        ft.Row([
            ft.Text("Módulo de Ventas con Tabs", size=24, weight="bold"),
            ft.ElevatedButton("+ Nueva Venta", on_click=nueva_venta_tab),
            ft.ElevatedButton("Cerrar Venta", on_click=lambda e: (
                tabs.tabs.pop(tabs.selected_index),
                setattr(tabs, 'selected_index', max(tabs.selected_index - 1, 0)),
                page.update()
            ) if tabs.tabs else None)
        ]),
        tabs
    )

    nueva_venta_tab()

ft.app(target=main)