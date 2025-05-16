import flet as ft
import mysql.connector
import datetime

# =================== CONEXIÓN BASE DE DATOS ===================
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Juanjose/11",  # Cambia tu contraseña
        database="super_uno",
        port=3310
    )

# =================== FUNCIONES CLIENTES ===================
def agregar_cliente(telefono, nombre, correo, direccion):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO Clientes (telefono, nombre, correo, direccion) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(sql, (telefono, nombre, correo, direccion))
        conn.commit()
        return True
    except mysql.connector.Error as e:
        print("Error al agregar cliente:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def eliminar_cliente(telefono):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM Clientes WHERE telefono = %s"
    try:
        cursor.execute(sql, (telefono,))
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as e:
        print("Error al eliminar cliente:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def buscar_cliente(telefono):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT nombre, correo, direccion FROM Clientes WHERE telefono = %s"
    try:
        cursor.execute(sql, (telefono,))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        print("Error al buscar cliente:", e)
        return None
    finally:
        cursor.close()
        conn.close()

# =================== FUNCIONES EMPLEADOS ===================
def agregar_empleado(nombre, puesto, salario, fecha_contratacion, turno):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO Empleados (nombre, puesto, salario, fecha_contratacion, turno) VALUES (%s, %s, %s, %s, %s)"
    try:
        cursor.execute(sql, (nombre, puesto, salario, fecha_contratacion, turno))
        conn.commit()
        return True
    except mysql.connector.Error as e:
        print("Error al agregar empleado:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def eliminar_empleado(id_empleado):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM Empleados WHERE id_empleado = %s"
    try:
        cursor.execute(sql, (id_empleado,))
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as e:
        print("Error al eliminar empleado:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def buscar_empleado(id_empleado):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT nombre, puesto, salario, fecha_contratacion, turno FROM Empleados WHERE id_empleado = %s"
    try:
        cursor.execute(sql, (id_empleado,))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        print("Error al buscar empleado:", e)
        return None
    finally:
        cursor.close()
        conn.close()

# =================== FUNCIONES PROVEEDORES ===================
def agregar_proveedor(nombre, telefono, contacto):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO Proveedores (nombre, telefono, contacto) VALUES (%s, %s, %s)"
    try:
        cursor.execute(sql, (nombre, telefono, contacto))
        conn.commit()
        return True
    except mysql.connector.Error as e:
        print("Error al agregar proveedor:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def eliminar_proveedor(id_proveedor):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM Proveedores WHERE id_proveedor = %s"
    try:
        cursor.execute(sql, (id_proveedor,))
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as e:
        print("Error al eliminar proveedor:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def buscar_proveedor(id_proveedor):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT nombre, telefono, contacto FROM Proveedores WHERE id_proveedor = %s"
    try:
        cursor.execute(sql, (id_proveedor,))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        print("Error al buscar proveedor:", e)
        return None
    finally:
        cursor.close()
        conn.close()

# =================== INTERFAZ PRINCIPAL ===================
def main(page: ft.Page):
    page.title = "Sistema Super Uno"
    page.window_width = 700
    page.window_height = 550

    # =================== INTERFAZ CLIENTES ===================
    def interfaz_clientes():
        telefono = ft.TextField(label="Teléfono", width=300)
        nombre = ft.TextField(label="Nombre", width=300)
        correo = ft.TextField(label="Correo", width=300)
        direccion = ft.TextField(label="Dirección", width=300, multiline=True)

        def guardar(e):
            if agregar_cliente(telefono.value, nombre.value, correo.value, direccion.value):
                page.snack_bar = ft.SnackBar(ft.Text("Cliente guardado"))
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Error al guardar cliente"))
            page.snack_bar.open = True
            page.update()

        def eliminar(e):
            if eliminar_cliente(telefono.value):
                nombre.value = correo.value = direccion.value = ""
                page.snack_bar = ft.SnackBar(ft.Text("Cliente eliminado"))
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Cliente no encontrado"))
            page.snack_bar.open = True
            page.update()

        def buscar(e):
            cliente = buscar_cliente(telefono.value)
            if cliente:
                nombre.value, correo.value, direccion.value = cliente
                page.snack_bar = ft.SnackBar(ft.Text("Cliente encontrado"))
            else:
                nombre.value = correo.value = direccion.value = ""
                page.snack_bar = ft.SnackBar(ft.Text("Cliente no encontrado"))
            page.snack_bar.open = True
            page.update()

        page.clean()
        page.add(
            ft.Column([
                ft.Text("Gestión de Clientes", size=24, weight="bold"),
                telefono, nombre, correo, direccion,
                ft.Row([
                    ft.ElevatedButton("Guardar", icon=ft.icons.SAVE, on_click=guardar),
                    ft.ElevatedButton("Eliminar", icon=ft.icons.DELETE, on_click=eliminar),
                    ft.ElevatedButton("Buscar", icon=ft.icons.SEARCH, on_click=buscar),
                    ft.ElevatedButton("Limpiar", icon=ft.icons.CLEAR, on_click=lambda e: [telefono.update(value=""), nombre.update(value=""), correo.update(value=""), direccion.update(value=""), page.update()])
                ])
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    # =================== INTERFAZ EMPLEADOS ===================
    def interfaz_empleados():
        id_empleado = ft.TextField(label="ID Empleado", width=300)
        nombre = ft.TextField(label="Nombre", width=300)
        puesto = ft.TextField(label="Puesto", width=300)
        salario = ft.TextField(label="Salario", width=300)
        turno = ft.Dropdown(label="Turno", width=300, options=[ft.dropdown.Option("Matutino"), ft.dropdown.Option("Vespertino"), ft.dropdown.Option("Nocturno")])

        def guardar(e):
            fecha_hoy = datetime.date.today().strftime('%Y-%m-%d')
            if agregar_empleado(nombre.value, puesto.value, salario.value, fecha_hoy, turno.value):
                page.snack_bar = ft.SnackBar(ft.Text("Empleado guardado"))
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Error al guardar empleado"))
            page.snack_bar.open = True
            page.update()

        def eliminar(e):
            if eliminar_empleado(id_empleado.value):
                nombre.value = puesto.value = salario.value = turno.value = ""
                page.snack_bar = ft.SnackBar(ft.Text("Empleado eliminado"))
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Empleado no encontrado"))
            page.snack_bar.open = True
            page.update()

        def buscar(e):
            empleado = buscar_empleado(id_empleado.value)
            if empleado:
                nombre.value, puesto.value, salario.value, fecha, turno.value = empleado
                page.snack_bar = ft.SnackBar(ft.Text("Empleado encontrado"))
            else:
                nombre.value = puesto.value = salario.value = turno.value = ""
                page.snack_bar = ft.SnackBar(ft.Text("Empleado no encontrado"))
            page.snack_bar.open = True
            page.update()

        page.clean()
        page.add(
            ft.Column([
                ft.Text("Gestión de Empleados", size=24, weight="bold"),
                id_empleado, nombre, puesto, salario, turno,
                ft.Row([
                    ft.ElevatedButton("Guardar", icon=ft.icons.SAVE, on_click=guardar),
                    ft.ElevatedButton("Eliminar", icon=ft.icons.DELETE, on_click=eliminar),
                    ft.ElevatedButton("Buscar", icon=ft.icons.SEARCH, on_click=buscar),
                    ft.ElevatedButton("Limpiar", icon=ft.icons.CLEAR, on_click=lambda e: [id_empleado.update(value=""), nombre.update(value=""), puesto.update(value=""), salario.update(value=""), turno.update(value=""), page.update()])
                ])
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    # =================== INTERFAZ PROVEEDORES ===================
    def interfaz_proveedores():
        id_proveedor = ft.TextField(label="ID Proveedor", width=300)
        nombre = ft.TextField(label="Nombre", width=300)
        telefono = ft.TextField(label="Teléfono", width=300)
        contacto = ft.TextField(label="Contacto", width=300)

        def guardar(e):
            if agregar_proveedor(nombre.value, telefono.value, contacto.value):
                page.snack_bar = ft.SnackBar(ft.Text("Proveedor guardado"))
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Error al guardar proveedor"))
            page.snack_bar.open = True
            page.update()

        def eliminar(e):
            if eliminar_proveedor(id_proveedor.value):
                nombre.value = telefono.value = contacto.value = ""
                page.snack_bar = ft.SnackBar(ft.Text("Proveedor eliminado"))
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Proveedor no encontrado"))
            page.snack_bar.open = True
            page.update()

        def buscar(e):
            proveedor = buscar_proveedor(id_proveedor.value)
            if proveedor:
                nombre.value, telefono.value, contacto.value = proveedor
                page.snack_bar = ft.SnackBar(ft.Text("Proveedor encontrado"))
            else:
                nombre.value = telefono.value = contacto.value = ""
                page.snack_bar = ft.SnackBar(ft.Text("Proveedor no encontrado"))
            page.snack_bar.open = True
            page.update()

        page.clean()
        page.add(
            ft.Column([
                ft.Text("Gestión de Proveedores", size=24, weight="bold"),
                id_proveedor, nombre, telefono, contacto,
                ft.Row([
                    ft.ElevatedButton("Guardar", icon=ft.icons.SAVE, on_click=guardar),
                    ft.ElevatedButton("Eliminar", icon=ft.icons.DELETE, on_click=eliminar),
                    ft.ElevatedButton("Buscar", icon=ft.icons.SEARCH, on_click=buscar),
                    ft.ElevatedButton("Limpiar", icon=ft.icons.CLEAR, on_click=lambda e: [id_proveedor.update(value=""), nombre.update(value=""), telefono.update(value=""), contacto.update(value=""), page.update()])
                ])
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    # =================== MENU PRINCIPAL ===================
    page.add(
        ft.Column([
            ft.Text("Sistema de Gestión Super Uno", size=28, weight="bold"),
            ft.ElevatedButton("Clientes", on_click=lambda e: interfaz_clientes()),
            ft.ElevatedButton("Empleados", on_click=lambda e: interfaz_empleados()),
            ft.ElevatedButton("Proveedores", on_click=lambda e: interfaz_proveedores())
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)
    )

ft.app(target=main)
