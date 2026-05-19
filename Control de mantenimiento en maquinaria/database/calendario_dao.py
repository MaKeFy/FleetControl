from database.connection import DatabaseConnection


class CalendarioDAO:
    def __init__(self):
        self.db = DatabaseConnection.get_instance()
        self._asegurar_tabla()

    def registrar_evento(self, tipo, descripcion, entidad=None, id_referencia=None):
        cursor = self.db.cursor()
        try:
            self._asegurar_tabla()
            cursor.execute(
                """
                INSERT INTO calendario_eventos (tipo, descripcion, entidad, id_referencia)
                VALUES (%s, %s, %s, %s)
                """,
                (tipo, descripcion, entidad, id_referencia)
            )
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error al registrar evento de calendario: {e}")
            self.db.rollback()
            return False
        finally:
            cursor.close()

    def obtener_resumen_mes(self, anio, mes):
        cursor = self.db.cursor(dictionary=True, buffered=True)
        try:
            self._asegurar_tabla()
            cursor.execute(
                """
                SELECT DAY(fecha_evento) AS dia, COUNT(*) AS total
                FROM calendario_eventos
                WHERE YEAR(fecha_evento) = %s AND MONTH(fecha_evento) = %s
                GROUP BY DAY(fecha_evento)
                """,
                (anio, mes)
            )
            return {int(r["dia"]): int(r["total"]) for r in cursor.fetchall()}
        except Exception as e:
            print(f"Error al obtener resumen de calendario: {e}")
            return {}
        finally:
            cursor.close()

    def obtener_eventos_dia(self, fecha):
        cursor = self.db.cursor(dictionary=True, buffered=True)
        try:
            self._asegurar_tabla()
            cursor.execute(
                """
                SELECT id_evento, tipo, descripcion, entidad, id_referencia, fecha_evento
                FROM calendario_eventos
                WHERE DATE(fecha_evento) = %s
                ORDER BY fecha_evento ASC, id_evento ASC
                """,
                (fecha,)
            )
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener eventos del dia: {e}")
            return []
        finally:
            cursor.close()

    def _asegurar_tabla(self):
        cursor = self.db.cursor()
        try:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS calendario_eventos (
                    id_evento INT AUTO_INCREMENT PRIMARY KEY,
                    tipo VARCHAR(60) NOT NULL,
                    descripcion TEXT NOT NULL,
                    entidad VARCHAR(60),
                    id_referencia INT,
                    fecha_evento TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            self.db.commit()
        finally:
            cursor.close()
