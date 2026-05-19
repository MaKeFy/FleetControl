from database.connection import DatabaseConnection
from database.calendario_dao import CalendarioDAO

class MaquinariaDAO:
    def __init__(self):
        self.db = DatabaseConnection.get_instance()

    def obtener_todos(self):
        """Recupera toda la flota para el Dashboard (RF09)"""
        cursor = self.db.cursor(dictionary=True) # Retorna diccionarios
        sql = "SELECT id_maquina, vin, marca, modelo, horas_motor_total, estado_color FROM Maquinaria"
        cursor.execute(sql)
        resultado = cursor.fetchall()
        cursor.close()
        return resultado
    
    def obtener_estado_detallado_planes(self, id_maquina):
        cursor = self.db.cursor(dictionary=True, buffered=True)
        sql = """
            SELECT 
                p.id_plan,                  -- <--- ESTA LÍNEA ES LA SOLUCIÓN
                p.nombre_plan,
                p.intervalo_horas,
                mp.ultima_ejecucion_horas,
                m.horas_motor_total
            FROM maquinaria_planes mp
            JOIN planes p ON mp.id_plan = p.id_plan
            JOIN maquinaria m ON mp.id_maquina = m.id_maquina
            WHERE mp.id_maquina = %s
        """
        cursor.execute(sql, (id_maquina,))
        return cursor.fetchall()
        
    def obtener_maquina_con_plan(self, id_maquina):
        """Obtiene los datos de una sola máquina incluyendo su plan."""
        cursor = self.db.cursor(dictionary=True, buffered=True)
        sql = """
            SELECT m.id_maquina AS id, m.marca, m.modelo, m.horas_motor_total, 
                m.ultimo_mantenimiento_horas, m.estado_color,
                MIN(p.intervalo_horas) AS intervalo_horas
            FROM Maquinaria m
            LEFT JOIN Maquinaria_Planes mp ON m.id_maquina = mp.id_maquina
            LEFT JOIN Planes p ON mp.id_plan = p.id_plan
            WHERE m.id_maquina = %s
            GROUP BY m.id_maquina
        """
        try:
            cursor.execute(sql, (id_maquina,))
            return cursor.fetchone() # Retorna un solo dict o None
        except Exception as e:
            print(f"ERROR SQL en obtener_maquina_con_plan: {e}")
            return None
        finally:
            cursor.close()
    
    def obtener_maquina_con_proyeccion(self, id_maquina):
        cursor = self.db.cursor(dictionary=True, buffered=True)
        sql = """
            SELECT 
                m.id_maquina,
                m.horas_motor_total,
                m.ultimo_mantenimiento_horas,
                p.intervalo_horas,
                (m.ultimo_mantenimiento_horas + p.intervalo_horas) AS meta_proximo_servicio
            FROM Maquinaria m
            JOIN Maquinaria_Planes mp ON m.id_maquina = mp.id_maquina
            JOIN Planes p ON mp.id_plan = p.id_plan
            WHERE m.id_maquina = %s
        """
        cursor.execute(sql, (id_maquina,))
        return cursor.fetchone()
    
    def obtener_todos_con_plan(self):
        cursor = self.db.cursor(dictionary=True, buffered=True)
        # Seleccionamos las columnas necesarias y el mínimo del intervalo
        # Agrupamos solo por la llave primaria para evitar errores de ambigüedad
        sql = """
            SELECT 
                m.id_maquina AS id, 
                m.marca, m.modelo, m.vin, 
                m.horas_motor_total, m.ultimo_mantenimiento_horas, m.estado_color,
                MIN(p.intervalo_horas) AS intervalo_horas,
                (SELECT COUNT(*) FROM ordenes_servicio 
                WHERE id_maquina = m.id_maquina 
                AND tipo = 'correctivo' 
                AND estado != 'Cerrada') AS tiene_falla_activa
            FROM Maquinaria m
            LEFT JOIN Maquinaria_Planes mp ON m.id_maquina = mp.id_maquina
            LEFT JOIN Planes p ON mp.id_plan = p.id_plan
            GROUP BY m.id_maquina
        """
        try:
            cursor.execute(sql)
            resultados = cursor.fetchall()
            return resultados if resultados is not None else []
        except Exception as e:
            print(f"ERROR CRÍTICO SQL: {e}")
            return []
        finally:
            cursor.close()
            
    def registrar_incidencia_correctiva(self, id_maquina, falla, mecanico="Pendiente"):
        cursor = self.db.cursor()
        sql = """
            INSERT INTO ordenes_servicio 
            (id_maquina, fecha_creacion, tipo, descripcion_falla, mecanico, estado)
            VALUES (%s, CURDATE(), 'correctivo', %s, %s, 'Abierta')
        """
        try:
            cursor.execute(sql, (id_maquina, falla, mecanico))
            id_orden = cursor.lastrowid
            self.db.commit()
            CalendarioDAO().registrar_evento(
                "Incidencia",
                f"Incidencia registrada: {falla}",
                "ordenes_servicio",
                id_orden
            )
            return True
        except Exception as e:
            print(f"Error al registrar incidencia: {e}")
            return False
        
    def registrar_cumplimiento_plan(self, id_maquina, id_plan, horas_actuales):
        """
        Actualiza el registro de ejecución de un plan específico 
        sin afectar el horómetro total de la máquina.
        """
        cursor = self.db.cursor()
        sql = """
            UPDATE maquinaria_planes 
            SET ultima_ejecucion_horas = %s 
            WHERE id_maquina = %s AND id_plan = %s
        """
        try:
            cursor.execute(sql, (horas_actuales, id_maquina, id_plan))
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar cumplimiento de plan: {e}")
            return False
        finally:
            cursor.close()
                
    def buscar_por_filtro(self, texto):
        """Lógica para la barra de búsqueda superior"""
        cursor = self.db.cursor(dictionary=True)
        sql = "SELECT * FROM Maquinaria WHERE id_maquina LIKE %s OR marca LIKE %s OR modelo LIKE %s"
        val = (f"%{texto}%", f"%{texto}%", f"%{texto}%")
        cursor.execute(sql, val)
        return cursor.fetchall()
    
    # En database/maquinaria_dao.py

    def registrar_nueva(self, datos):
        cursor = self.db.cursor()
        try:
            sql = """
                INSERT INTO Maquinaria (marca, modelo, vin, horas_motor_total, ultimo_mantenimiento_horas)
                VALUES (%s, %s, %s, %s, %s)
            """
            horas = float(datos.get('horas', datos.get('horas_totales', 0)) or 0)
            valores = (
                datos['marca'], datos['modelo'], datos.get('vin') or datos.get('serie'),
                horas, datos.get('ultima_atencion', horas)
            )
            cursor.execute(sql, valores)
            id_generado = cursor.lastrowid
            self.db.commit()
            CalendarioDAO().registrar_evento(
                "Nueva unidad",
                f"Nueva unidad registrada: {datos['marca']} {datos['modelo']} ({datos.get('vin') or datos.get('serie')})",
                "maquinaria",
                id_generado
            )
            return id_generado
        except Exception as e:
            self.db.rollback()
            print(f"Error al guardar unidad: {e}")
            return False
        finally:
            cursor.close()
        
        
    def actualizar_maquinaria(self, id_maquina, datos):
        cursor = self.db.cursor()
        try:
            sql = """
                UPDATE Maquinaria 
                SET marca = %s, modelo = %s, vin = %s, horas_motor_total = %s 
                WHERE id_maquina = %s
            """
            valores = (datos['marca'], datos['modelo'], datos['vin'], datos['horas'], id_maquina)
            cursor.execute(sql, valores)
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar: {e}")
            return False
        
    def acumular_horas(self, id_maq, horas_nuevas):
        try:
            cursor = self.db.cursor(dictionary=True, buffered=True)
            cursor.execute(
                "SELECT marca, modelo FROM Maquinaria WHERE id_maquina = %s",
                (id_maq,)
            )
            maquina = cursor.fetchone() or {}
            # Lógica de acumulación: horas_actuales + horas_ingresadas
            sql = "UPDATE Maquinaria SET horas_motor_total = horas_motor_total + %s WHERE id_maquina = %s"
            cursor.execute(sql, (horas_nuevas, id_maq))
            self.db.commit()
            CalendarioDAO().registrar_evento(
                "Registro de unidad",
                f"Registro de uso: {horas_nuevas} h en {maquina.get('marca', '')} {maquina.get('modelo', '')}".strip(),
                "maquinaria",
                id_maq
            )
            return True
        except Exception as e:
            print(f"Error al acumular: {e}")
            return False
        
    # database/maquinaria_dao.py

    def actualizar_estado_color(self, id_maquina, nuevo_color):
        """Actualiza físicamente el color en la BD tras el cálculo lógico."""
        cursor = self.db.cursor()
        try:
            sql = "UPDATE Maquinaria SET estado_color = %s WHERE id_maquina = %s"
            cursor.execute(sql, (nuevo_color, id_maquina))
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar color en BD: {e}")
            return False
        finally:
            cursor.close()
    
    def eliminar_maquinaria(self, id_maquina):
        cursor = self.db.cursor()
        try:
            # Nota: La base de datos debe tener ON DELETE CASCADE en Maquinaria_Planes
            sql = "DELETE FROM Maquinaria WHERE id_maquina = %s"
            cursor.execute(sql, (id_maquina,))
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar: {e}")
            return False
        
    def obtener_ordenes_servicio(self, estado_filtro=None):
        cursor = self.db.cursor(dictionary=True, buffered=True)
        sql = """
            SELECT 
                os.*, 
                m.marca, m.modelo, m.vin, m.horas_motor_total,
                p.nombre_plan
            FROM ordenes_servicio os
            JOIN maquinaria m ON os.id_maquina = m.id_maquina
            LEFT JOIN planes p ON os.id_plan_preventivo = p.id_plan
        """
        
        # Si hay un filtro, añadimos la cláusula WHERE
        if estado_filtro:
            sql += " WHERE os.estado = %s"
        
        sql += " ORDER BY os.fecha_creacion DESC"
        
        try:
            # Pasamos el parámetro solo si existe
            params = (estado_filtro,) if estado_filtro else ()
            cursor.execute(sql, params)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error DAO Ordenes: {e}")
            return []
        finally:
            cursor.close()
    
    def cerrar_orden_servicio(self, id_orden, costo, notas):
        """Cierra la orden y registra los datos finales."""
        cursor = self.db.cursor(dictionary=True, buffered=True)
        sql = """
            UPDATE ordenes_servicio 
            SET estado = 'Cerrada', fecha_cierre = CURDATE(), 
                costo_total = %s, descripcion_falla = CONCAT(descripcion_falla, '\nNotas Cierre: ', %s)
            WHERE id_orden = %s
        """
        try:
            cursor.execute(sql, (costo, notas, id_orden))
            self.db.commit()
            cursor.execute(
                """
                SELECT os.id_orden, os.tipo, m.marca, m.modelo
                FROM ordenes_servicio os
                JOIN maquinaria m ON os.id_maquina = m.id_maquina
                WHERE os.id_orden = %s
                """,
                (id_orden,)
            )
            orden = cursor.fetchone() or {}
            CalendarioDAO().registrar_evento(
                "Finalización de orden",
                f"Orden #{id_orden} finalizada ({orden.get('tipo', '')}) - {orden.get('marca', '')} {orden.get('modelo', '')}".strip(),
                "ordenes_servicio",
                id_orden
            )
            return True
        except Exception as e:
            print(f"Error al cerrar orden: {e}")
            return False
        finally:
            cursor.close()

    def eliminar_orden_servicio(self, id_orden, motivo, usuario):
        cursor = self.db.cursor(dictionary=True, buffered=True)
        try:
            self._asegurar_tabla_auditoria_eliminacion()
            cursor.execute(
                """
                SELECT id_orden, folio, id_maquina, tipo, estado, fecha_creacion,
                       fecha_cierre, descripcion_falla, costo_total
                FROM ordenes_servicio
                WHERE id_orden = %s
                """,
                (id_orden,)
            )
            orden = cursor.fetchone()
            if not orden:
                return False

            cursor.execute(
                """
                INSERT INTO auditoria_eliminacion_ordenes
                (id_orden_original, folio, id_maquina, tipo, estado, fecha_creacion,
                 fecha_cierre, descripcion_falla, costo_total, motivo, usuario)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    orden.get("id_orden"), orden.get("folio"), orden.get("id_maquina"),
                    orden.get("tipo"), orden.get("estado"), orden.get("fecha_creacion"),
                    orden.get("fecha_cierre"), orden.get("descripcion_falla"),
                    orden.get("costo_total"), motivo, usuario
                )
            )

            cursor.execute("DELETE FROM repuestos WHERE id_orden = %s", (id_orden,))
            cursor.execute("DELETE FROM ordenes_servicio WHERE id_orden = %s", (id_orden,))
            eliminadas = cursor.rowcount
            self.db.commit()
            return eliminadas > 0
        except Exception as e:
            print(f"Error al eliminar orden de servicio: {e}")
            self.db.rollback()
            return False
        finally:
            cursor.close()

    def _asegurar_tabla_auditoria_eliminacion(self):
        cursor = self.db.cursor()
        try:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS auditoria_eliminacion_ordenes (
                    id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
                    id_orden_original INT NOT NULL,
                    folio VARCHAR(20),
                    id_maquina INT,
                    tipo VARCHAR(20),
                    estado VARCHAR(20),
                    fecha_creacion DATE,
                    fecha_cierre DATE,
                    descripcion_falla TEXT,
                    costo_total FLOAT,
                    motivo TEXT NOT NULL,
                    usuario VARCHAR(100) NOT NULL,
                    fecha_eliminacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            self.db.commit()
        finally:
            cursor.close()

    def obtener_detalle_orden_servicio(self, id_orden):
        cursor = self.db.cursor(dictionary=True, buffered=True)
        sql = """
            SELECT 
                os.*,
                m.marca, m.modelo, m.vin, m.horas_motor_total,
                p.nombre_plan
            FROM ordenes_servicio os
            JOIN maquinaria m ON os.id_maquina = m.id_maquina
            LEFT JOIN planes p ON os.id_plan_preventivo = p.id_plan
            WHERE os.id_orden = %s
        """
        try:
            cursor.execute(sql, (id_orden,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener detalle de orden: {e}")
            return None
        finally:
            cursor.close()

    def obtener_repuestos_orden(self, id_orden):
        cursor = self.db.cursor(dictionary=True, buffered=True)
        try:
            cursor.execute(
                """
                SELECT nombre, costo_unitario AS costo
                FROM repuestos
                WHERE id_orden = %s
                ORDER BY nombre
                """,
                (id_orden,)
            )
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener repuestos de orden: {e}")
            return []
        finally:
            cursor.close()

    def obtener_ordenes_para_reporte(self):
        cursor = self.db.cursor(dictionary=True, buffered=True)
        sql = """
            SELECT 
                os.id_orden, os.folio, os.tipo, os.estado, os.fecha_creacion,
                os.fecha_cierre, os.descripcion_falla, os.costo_total,
                m.marca, m.modelo, m.vin,
                COALESCE(SUM(r.costo_unitario), 0) AS costo_repuestos
            FROM ordenes_servicio os
            JOIN maquinaria m ON os.id_maquina = m.id_maquina
            LEFT JOIN repuestos r ON os.id_orden = r.id_orden
            GROUP BY os.id_orden
            ORDER BY os.fecha_creacion DESC, os.id_orden DESC
        """
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener ordenes para reporte: {e}")
            return []
        finally:
            cursor.close()

    def actualizar_ultimo_servicio_maquina(self, id_maquina, horas_cierre):
        """Actualiza la última lectura en la que la unidad recibió servicio."""
        cursor = self.db.cursor()
        try:
            sql = """
                UPDATE Maquinaria
                SET ultimo_mantenimiento_horas = %s
                WHERE id_maquina = %s
            """
            cursor.execute(sql, (horas_cierre, id_maquina))
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar último servicio de máquina: {e}")
            self.db.rollback()
            return False
        finally:
            cursor.close()
        
    def existe_orden_abierta(self, id_maquina, id_plan, nombre_plan=None):
        cursor = self.db.cursor()
        # Usamos UPPER para ignorar problemas de mayúsculas/minúsculas en el estado y tipo
        sql = """
            SELECT id_orden FROM ordenes_servicio 
            WHERE id_maquina = %s 
            AND tipo = 'preventivo'
            AND UPPER(estado) != 'CERRADA'
            AND (
                id_plan_preventivo = %s
                OR descripcion_falla LIKE %s
            )
            LIMIT 1
        """
        plan_texto = f"%{nombre_plan}%" if nombre_plan else "__SIN_NOMBRE_DE_PLAN__"
        try:
            cursor.execute(sql, (id_maquina, id_plan, plan_texto))
            result = cursor.fetchone()
            return result is not None
        finally:
            cursor.close()

    def crear_orden_automatica(self, id_maquina, id_plan, descripcion):
        cursor = self.db.cursor()
        sql = """
            INSERT INTO ordenes_servicio 
            (id_maquina, id_plan_preventivo, fecha_creacion, tipo, descripcion_falla, estado)
            VALUES (%s, %s, CURDATE(), 'preventivo', %s, 'Abierta')
        """
        try:
            if self.existe_orden_abierta(id_maquina, id_plan):
                return True
            cursor.execute(sql, (id_maquina, id_plan, descripcion))
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error en orden automática: {e}")
            return False
        
    def registrar_repuestos_orden(self, id_orden, lista_repuestos):
        cursor = self.db.cursor()
        sql = "INSERT INTO repuestos (id_orden, nombre, costo_unitario) VALUES (%s, %s, %s)"
        try:
            for r in lista_repuestos:
                cursor.execute(sql, (id_orden, r['nombre'], r['costo']))
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error al registrar repuestos: {e}")
            return False
        
    def crear_orden_manual(self, id_maquina, tipo, descripcion):
        """
        Crea una orden de servicio manual (correctiva).
        No requiere id_plan_preventivo.
        """
        cursor = self.db.cursor()
        # Generamos un folio único simple o puedes usar uno basado en fecha
        import datetime
        folio = f"MAN-{datetime.datetime.now().strftime('%M%S')}"
        
        sql = """
            INSERT INTO ordenes_servicio 
            (id_maquina, folio, fecha_creacion, tipo, descripcion_falla, estado)
            VALUES (%s, %s, CURDATE(), %s, %s, 'Abierta')
        """
        try:
            cursor.execute(sql, (id_maquina, folio, tipo, descripcion))
            id_orden = cursor.lastrowid
            self.db.commit()
            CalendarioDAO().registrar_evento(
                "Incidencia",
                f"Incidencia registrada: {descripcion}",
                "ordenes_servicio",
                id_orden
            )
            return True
        except Exception as e:
            print(f"Error al crear orden manual: {e}")
            self.db.rollback()
            return False
        
    def tiene_orden_correctiva_abierta(self, id_maquina):
        """Verifica si hay reportes manuales/correctivos sin cerrar."""
        cursor = self.db.cursor()
        sql = """
            SELECT COUNT(*) FROM ordenes_servicio 
            WHERE id_maquina = %s AND tipo = 'correctivo' AND estado != 'Cerrada'
        """
        cursor.execute(sql, (id_maquina,))
        result = cursor.fetchone()
        return result[0] > 0
