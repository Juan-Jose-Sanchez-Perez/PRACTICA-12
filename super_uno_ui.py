import flet as ft
import mysql.connector

# Conexión a la base de datos
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",        # Cambia por tu usuario de MySQL
        password="Juanjose/11", # Cambia por tu contraseña
        database="super_uno",
        port=3310
    )

def main(page: ft.Page):
    page.title = "Gestión de Super_Uno"
    page.window_width = 800
    page.window_height = 600

    # -------------------------
    # CLIENTES
    # -------------------------
    nombre_cliente = ft.TextField(label="Nombre")
    telefono_cliente = ft.TextField(label="Teléfono")
    correo_cliente = ft.TextField(label="Correo")
    direccion_cliente = ft.TextField(label="Dirección")

    clientes_output = ft.Column()

    def agregar_cliente(e):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Clientes (telefono, nombre, correo, direccion) VALUES (%s, %s, %s, %s)",
                (telefono_cliente.value, nombre_cliente.value, correo_cliente.value, direccion_cliente.value)
            )
            conn.commit()
            clientes_output.controls.append(ft.Text(f"✅ Cliente {nombre_cliente.value} agregado."))
            nombre_cliente.value = telefono_cliente.value = correo_cliente.value = direccion_cliente.value = ""
            page.update()
            listar_clientes()
        except mysql.connector.Error as err:
            clientes_output.controls.append(ft.Text(f"❌ Error: {err}"))
        finally:
            cursor.close()
            conn.close()

    def listar_clientes():
        conn = get_connection()
        cursor = conn.cursor()
        clientes_output.controls.clear()
        cursor.execute("SELECT * FROM Clientes")
        for row in cursor.fetchall():
            clientes_output.controls.append(ft.Text(f"{row}"))
        cursor.close()
        conn.close()
        page.update()

    cliente_tab = ft.Column([
        nombre_cliente,
        telefono_cliente,
        correo_cliente,
        direccion_cliente,
        ft.ElevatedButton("Agregar Cliente", on_click=agregar_cliente),
        ft.Text("Listado de Clientes:"),
        clientes_output
    ])

    listar_clientes()

    # -------------------------
    # EMPLEADOS
    # -------------------------
    nombre_empleado = ft.TextField(label="Nombre")
    puesto_empleado = ft.TextField(label="Puesto")
    salario_empleado = ft.TextField(label="Salario")
    fecha_contratacion = ft.TextField(label="Fecha Contratación (YYYY-MM-DD)")
    turno_empleado = ft.Dropdown(
        label="Turno",
        options=[ft.dropdown.Option("Matutino"), ft.dropdown.Option("Vespertino"), ft.dropdown.Option("Nocturno")]
    )

    empleados_output = ft.Column()

    def agregar_empleado(e):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Empleados (nombre, puesto, salario, fecha_contratacion, turno) VALUES (%s, %s, %s, %s, %s)",
                (nombre_empleado.value, puesto_empleado.value, salario_empleado.value, fecha_contratacion.value, turno_empleado.value)
            )
            conn.commit()
            empleados_output.controls.append(ft.Text(f"✅ Empleado {nombre_empleado.value} agregado."))
            nombre_empleado.value = puesto_empleado.value = salario_empleado.value = fecha_contratacion.value = ""
            turno_empleado.value = None
            page.update()
            listar_empleados()
        except mysql.connector.Error as err:
            empleados_output.controls.append(ft.Text(f"❌ Error: {err}"))
        finally:
            cursor.close()
            conn.close()

    def listar_empleados():
        conn = get_connection()
        cursor = conn.cursor()
        empleados_output.controls.clear()
        cursor.execute("SELECT * FROM Empleados")
        for row in cursor.fetchall():
            empleados_output.controls.append(ft.Text(f"{row}"))
        cursor.close()
        conn.close()
        page.update()

    empleado_tab = ft.Column([
        nombre_empleado,
        puesto_empleado,
        salario_empleado,
        fecha_contratacion,
        turno_empleado,
        ft.ElevatedButton("Agregar Empleado", on_click=agregar_empleado),
        ft.Text("Listado de Empleados:"),
        empleados_output
    ])

    listar_empleados()

    # -------------------------
    # PROVEEDORES
    # -------------------------
    nombre_proveedor = ft.TextField(label="Nombre")
    telefono_proveedor = ft.TextField(label="Teléfono")
    contacto_proveedor = ft.TextField(label="Contacto")

    proveedores_output = ft.Column()

    def agregar_proveedor(e):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Proveedores (nombre, telefono, contacto) VALUES (%s, %s, %s)",
                (nombre_proveedor.value, telefono_proveedor.value, contacto_proveedor.value)
            )
            conn.commit()
            proveedores_output.controls.append(ft.Text(f"✅ Proveedor {nombre_proveedor.value} agregado."))
            nombre_proveedor.value = telefono_proveedor.value = contacto_proveedor.value = ""
            page.update()
            listar_proveedores()
        except mysql.connector.Error as err:
            proveedores_output.controls.append(ft.Text(f"❌ Error: {err}"))
        finally:
            cursor.close()
            conn.close()

    def listar_proveedores():
        conn = get_connection()
        cursor = conn.cursor()
        proveedores_output.controls.clear()
        cursor.execute("SELECT * FROM Proveedores")
        for row in cursor.fetchall():
            proveedores_output.controls.append(ft.Text(f"{row}"))
        cursor.close()
        conn.close()
        page.update()

    proveedor_tab = ft.Column([
        nombre_proveedor,
        telefono_proveedor,
        contacto_proveedor,
        ft.ElevatedButton("Agregar Proveedor", on_click=agregar_proveedor),
        ft.Text("Listado de Proveedores:"),
        proveedores_output
    ])

    listar_proveedores()

    # -------------------------
    # TABS
    # -------------------------
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="Clientes", content=cliente_tab),
            ft.Tab(text="Empleados", content=empleado_tab),
            ft.Tab(text="Proveedores", content=proveedor_tab),
        ],
        expand=1
    )

    page.add(tabs)

ft.app(target=main)
