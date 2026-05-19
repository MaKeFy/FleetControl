import mysql.connector
from database.connection import DatabaseConnection
from database.calendario_dao import CalendarioDAO

class PlanesDAO:
    def __init__(self):
        self.db = DatabaseConnection.get_instance()
        
        if self.db is None:
            raise Exception("No se pudo establecer conexión con la base de datos.")

    def guardar_plan_completo(self, nombre, intervalo, id_maquina, lista_tareas):
        cursor = self.db.cursor()
        try:
            # En lugar de start_transaction, nos aseguramos de que no haya basura previa
            self.db.rollback() 

            # 1. Insertar el Plan Maestro
            sql_plan = "INSERT INTO Planes (nombre_plan, intervalo_horas) VALUES (%s, %s)"
            cursor.execute(sql_plan, (nombre, intervalo))
            id_nuevo_plan = cursor.lastrowid

            # 2. Insertar las Tareas
            if lista_tareas:
                sql_tarea = "INSERT INTO Tareas_Plan (id_plan, descripcion) VALUES (%s, %s)"
                # Preparamos los datos para un executemany (más eficiente)
                tareas_data = [(id_nuevo_plan, t.strip()) for t in lista_tareas if t.strip()]
                if tareas_data:
                    cursor.executemany(sql_tarea, tareas_data)

            # 3. VINCULACIÓN M:N en la tabla intermedia
            # Esto permite que una máquina tenga muchos planes
            sql_vinculo = "INSERT INTO Maquinaria_Planes (id_maquina, id_plan) VALUES (%s, %s)"
            cursor.execute(sql_vinculo, (id_maquina, id_nuevo_plan))

            # 4. Finalizar
            self.db.commit()
            CalendarioDAO().registrar_evento(
                "Creación de plan",
                f"Plan creado: {nombre} cada {intervalo} h",
                "planes",
                id_nuevo_plan
            )
            print(f"DEBUG: Plan {id_nuevo_plan} vinculado exitosamente a Máquina {id_maquina}")
            return True

        except Exception as e:
            self.db.rollback()
            print(f"Error al crear plan múltiple: {e}")
            return False
        finally:
            cursor.close()

    def obtener_todos_los_planes(self):
        cursor = self.db.cursor(dictionary=True)
        try:
            # Usamos 'modelo_maquina' como alias para mantener compatibilidad con la vista
            sql = """
                SELECT 
                    p.id_plan, 
                    p.nombre_plan as nombre, 
                    p.intervalo_horas as intervalo,
                    GROUP_CONCAT(DISTINCT CONCAT(m.marca, ' ', m.modelo) SEPARATOR ', ') as modelo_maquina,
                    GROUP_CONCAT(DISTINCT t.descripcion SEPARATOR '|') as tareas_raw
                FROM Planes p
                JOIN Maquinaria_Planes mp ON p.id_plan = mp.id_plan
                JOIN Maquinaria m ON mp.id_maquina = m.id_maquina
                LEFT JOIN Tareas_Plan t ON p.id_plan = t.id_plan
                GROUP BY p.id_plan
            """
            cursor.execute(sql)
            resultados = cursor.fetchall()

            for r in resultados:
                # Convertir el string de tareas a lista
                r['tareas'] = r['tareas_raw'].split('|') if r['tareas_raw'] else []
                # Si no hay máquinas (aunque por lógica debería haber), ponemos un texto default
                if not r['modelo_maquina']:
                    r['modelo_maquina'] = "Sin maquinaria"
            
            return resultados
        except Exception as e:
            print(f"Error al recuperar planes para la vista: {e}")
            return []

    def obtener_detalle_reporte_plan(self, id_plan):
        cursor = self.db.cursor(dictionary=True, buffered=True)
        try:
            cursor.execute(
                """
                SELECT id_plan, nombre_plan, intervalo_horas
                FROM Planes
                WHERE id_plan = %s
                """,
                (id_plan,)
            )
            plan = cursor.fetchone()
            if not plan:
                return None

            cursor.execute(
                """
                SELECT m.id_maquina, m.marca, m.modelo, m.vin, m.horas_motor_total
                FROM Maquinaria_Planes mp
                JOIN Maquinaria m ON mp.id_maquina = m.id_maquina
                WHERE mp.id_plan = %s
                ORDER BY m.marca, m.modelo
                """,
                (id_plan,)
            )
            maquinas = cursor.fetchall()

            cursor.execute(
                """
                SELECT descripcion
                FROM Tareas_Plan
                WHERE id_plan = %s
                ORDER BY id_tarea
                """,
                (id_plan,)
            )
            tareas = [r["descripcion"] for r in cursor.fetchall()]

            cursor.execute(
                """
                SELECT os.id_orden, os.fecha_creacion, os.descripcion_falla,
                       CONCAT(m.marca, ' ', m.modelo) AS maquinaria
                FROM ordenes_servicio os
                JOIN Maquinaria_Planes mp ON os.id_maquina = mp.id_maquina
                JOIN Maquinaria m ON os.id_maquina = m.id_maquina
                WHERE mp.id_plan = %s
                  AND os.tipo = 'correctivo'
                  AND UPPER(os.estado) != 'CERRADA'
                ORDER BY os.fecha_creacion ASC, os.id_orden ASC
                """,
                (id_plan,)
            )
            incidencias = cursor.fetchall()

            return {
                "plan": plan,
                "maquinas": maquinas,
                "tareas": tareas,
                "incidencias": incidencias,
            }
        except Exception as e:
            print(f"Error al obtener detalle de reporte de plan: {e}")
            return None
        finally:
            cursor.close()

    def eliminar_plan(self, id_plan):
        """
        Elimina un plan. Gracias al ON DELETE CASCADE en la BD, 
        las tareas se borrarán automáticamente.
        """
        cursor = self.db.cursor()
        try:
            sql = "DELETE FROM Planes WHERE id_plan = %s"
            cursor.execute(sql, (id_plan,))
            self.db.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error al eliminar plan: {err}")
            self.db.rollback()
            return False
        finally:
            cursor.close()

    def actualizar_plan(self, id_plan, nuevo_nombre, nuevas_tareas):
        """
        Actualiza un plan existente. La forma más limpia es borrar 
        las tareas viejas y re-insertar las nuevas.
        """
        cursor = self.db.cursor()
        try:
            self.db.start_transaction()

            # 1. Actualizar nombre del plan
            sql_update_plan = "UPDATE Planes SET nombre_plan = %s WHERE id_plan = %s"
            cursor.execute(sql_update_plan, (nuevo_nombre, id_plan))

            # 2. Borrar tareas actuales
            sql_delete_tareas = "DELETE FROM Tareas_Plan WHERE id_plan = %s"
            cursor.execute(sql_delete_tareas, (id_plan,))

            # 3. Insertar las tareas editadas
            sql_insert_tareas = "INSERT INTO Tareas_Plan (id_plan, descripcion) VALUES (%s, %s)"
            for desc in nuevas_tareas:
                if desc.strip():
                    cursor.execute(sql_insert_tareas, (id_plan, desc))

            self.db.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error al actualizar plan: {err}")
            self.db.rollback()
            return False
        finally:
            cursor.close()
