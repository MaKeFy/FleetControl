from datetime import date, datetime

from database.connection import DatabaseConnection


class BackupService:
    @staticmethod
    def exportar_base_datos(ruta_salida):
        db = DatabaseConnection.get_instance()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT DATABASE()")
            database = cursor.fetchone()[0]

            cursor.execute("SHOW TABLES")
            tablas = [fila[0] for fila in cursor.fetchall()]

            lineas = [
                f"-- Respaldo de base de datos: {database}",
                f"-- Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "SET FOREIGN_KEY_CHECKS=0;",
                "",
            ]

            for tabla in tablas:
                cursor.execute(f"SHOW CREATE TABLE `{tabla}`")
                create_sql = cursor.fetchone()[1]
                lineas.extend([
                    f"-- Tabla `{tabla}`",
                    f"DROP TABLE IF EXISTS `{tabla}`;",
                    f"{create_sql};",
                    "",
                ])

                cursor.execute(f"SELECT * FROM `{tabla}`")
                columnas = [desc[0] for desc in cursor.description]
                filas = cursor.fetchall()
                if filas:
                    columnas_sql = ", ".join(f"`{c}`" for c in columnas)
                    for fila in filas:
                        valores_sql = ", ".join(BackupService._sql_literal(v) for v in fila)
                        lineas.append(f"INSERT INTO `{tabla}` ({columnas_sql}) VALUES ({valores_sql});")
                    lineas.append("")

            lineas.append("SET FOREIGN_KEY_CHECKS=1;")
            with open(ruta_salida, "w", encoding="utf-8") as archivo:
                archivo.write("\n".join(lineas))
            return True
        finally:
            cursor.close()

    @staticmethod
    def _sql_literal(valor):
        if valor is None:
            return "NULL"
        if isinstance(valor, bool):
            return "1" if valor else "0"
        if isinstance(valor, (int, float)):
            return str(valor)
        if isinstance(valor, (datetime, date)):
            return f"'{valor.isoformat(sep=' ') if isinstance(valor, datetime) else valor.isoformat()}'"
        texto = str(valor).replace("\\", "\\\\").replace("'", "''")
        return f"'{texto}'"
