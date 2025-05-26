import flet as ft
from db_connection import get_connection

def main(page: ft.Page):
    page.title = "CRUD Empleados"
    page.scroll = ft.ScrollMode.AUTO

    
    editing_id = None

    # Campos del formulario
    nombre = ft.TextField(label="Nombre")
    puesto = ft.TextField(label="Puesto")
    salario = ft.TextField(label="Salario", keyboard_type=ft.KeyboardType.NUMBER)
    fecha_contratacion = ft.TextField(label="Fecha de Contratación (YYYY-MM-DD)")
    turno_dropdown = ft.Dropdown(
        label="Turno",
        options=[
            ft.dropdown.Option("Matutino"),
            ft.dropdown.Option("Vespertino"),
            ft.dropdown.Option("Nocturno")
        ]
    )
    output = ft.Text("")
    empleados_list = ft.Column()
    botones = ft.Row()  # aquí alternarán Registrar / Guardar+Cancelar

    def limpiar_campos():
        nombre.value = puesto.value = salario.value = fecha_contratacion.value = ""
        turno_dropdown.value = None
        output.value = ""

    def actualizar_botones():
        botones.controls.clear()
        if editing_id is None:
            botones.controls.append(
                ft.ElevatedButton("Registrar", on_click=registrar_empleado)
            )
        else:
            botones.controls.append(
                ft.ElevatedButton("Guardar cambios", on_click=guardar_cambios)
            )
            botones.controls.append(
                ft.ElevatedButton("Cancelar", on_click=cancelar_edicion)
            )
        page.update()

    # Carga la lista de empleados
    def cargar_empleados():
        empleados_list.controls.clear()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_empleado, nombre, puesto, salario, fecha_contratacion, turno
            FROM Empleados
        """)
        for id_emp, nom, pst, sal, fecha, turno in cursor.fetchall():
            empleados_list.controls.append(
                ft.Row([
                    ft.Text(f"{id_emp} – {nom} – {pst} – ${sal:.2f} – {fecha} – {turno}", expand=True),
                    ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, i=id_emp: editar_empleado(i)),
                    ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, i=id_emp: eliminar_empleado(i))
                ])
            )
        conn.close()
        page.update()

    # Inserta un nuevo empleado
    def registrar_empleado(e):
        if not turno_dropdown.value:
            output.value = "Selecciona un turno."
            page.update()
            return
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Empleados (nombre, puesto, salario, fecha_contratacion, turno) "
                "VALUES (%s, %s, %s, %s, %s)",
                (nombre.value, puesto.value, float(salario.value), fecha_contratacion.value, turno_dropdown.value)
            )
            conn.commit()
            output.value = "Empleado registrado"
            limpiar_campos()
        except Exception as ex:
            output.value = f"Error: {ex}"
        finally:
            conn.close()
            cargar_empleados()

    # Borra un empleado
    def eliminar_empleado(id_emp):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Empleados WHERE id_empleado = %s", (id_emp,))
            conn.commit()
            output.value = "Empleado eliminado"
        except Exception as ex:
            output.value = f"Error al eliminar: {ex}"
        finally:
            conn.close()
            cargar_empleados()

    # Pasa a modo edición: carga datos en el formulario
    def editar_empleado(id_emp):
        nonlocal editing_id
        editing_id = id_emp
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT nombre, puesto, salario, fecha_contratacion, turno "
            "FROM Empleados WHERE id_empleado = %s",
            (id_emp,)
        )
        result = cursor.fetchone()
        conn.close()
        if result:
            nombre.value, puesto.value = result[0], result[1]
            salario.value, fecha_contratacion.value = str(result[2]), str(result[3])
            turno_dropdown.value = result[4]
        output.value = ""
        actualizar_botones()

    # Guarda los cambios de la edición
    def guardar_cambios(e):
        nonlocal editing_id
        if not turno_dropdown.value:
            output.value = "Selecciona un turno."
            page.update()
            return
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE Empleados "
                "SET nombre=%s, puesto=%s, salario=%s, fecha_contratacion=%s, turno=%s "
                "WHERE id_empleado=%s",
                (nombre.value, puesto.value, float(salario.value),
                 fecha_contratacion.value, turno_dropdown.value, editing_id)
            )
            conn.commit()
            output.value = "Empleado actualizado"
            limpiar_campos()
            editing_id = None
        except Exception as ex:
            output.value = f"Error al actualizar: {ex}"
        finally:
            conn.close()
            actualizar_botones()
            cargar_empleados()

    # Cancela la edición y vuelve al modo registro
    def cancelar_edicion(e):
        nonlocal editing_id
        limpiar_campos()
        editing_id = None
        output.value = "Edición cancelada"
        actualizar_botones()

    
    page.add(
        ft.Text("Registrar / Editar Empleado", size=20, weight="bold"),
        nombre,
        puesto,
        salario,
        fecha_contratacion,
        turno_dropdown,
        botones,           # Aquí aparecerán Registrar ó Guardar+Cancelar
        output,
        ft.Divider(),
        ft.Text("Lista de Empleados", size=20),
        empleados_list
    )

    # Inicialización
    actualizar_botones()
    cargar_empleados()

ft.app(target=main)
