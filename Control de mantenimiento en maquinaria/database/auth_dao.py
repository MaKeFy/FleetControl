import hashlib

from database.connection import DatabaseConnection


class AuthDAO:
    def __init__(self):
        self.db = DatabaseConnection.get_instance()
        if self.db is None:
            raise Exception("No se pudo establecer conexion con la base de datos.")
        self._asegurar_tabla_usuarios()
        self._crear_admin_inicial()

    def autenticar(self, usuario, password):
        cursor = self.db.cursor(dictionary=True, buffered=True)
        try:
            cursor.execute(
                """
                SELECT id_usuario, nombre, password_hash, rol
                FROM usuarios
                WHERE nombre = %s
                """,
                (usuario,)
            )
            fila = cursor.fetchone()
            if not fila:
                return None

            if self._hash_password(password) != fila["password_hash"]:
                return None

            return {
                "id_usuario": fila["id_usuario"],
                "usuario": fila["nombre"],
                "rol": self._normalizar_rol(fila["rol"]),
            }
        finally:
            cursor.close()

    def validar_password_administrador(self, password):
        cursor = self.db.cursor(dictionary=True, buffered=True)
        try:
            cursor.execute(
                """
                SELECT password_hash
                FROM usuarios
                WHERE rol = 'administrador'
                """
            )
            for fila in cursor.fetchall():
                if self._hash_password(password) == fila["password_hash"]:
                    return True
            return False
        finally:
            cursor.close()

    def _asegurar_tabla_usuarios(self):
        cursor = self.db.cursor()
        try:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS usuarios (
                    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    rol ENUM('administrador', 'encargado') NOT NULL DEFAULT 'encargado'
                )
                """
            )
            self.db.commit()
        finally:
            cursor.close()

    def _crear_admin_inicial(self):
        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            total = cursor.fetchone()[0]
            if total:
                return

            cursor.execute(
                """
                INSERT INTO usuarios (nombre, password_hash, rol)
                VALUES (%s, %s, 'administrador')
                """,
                ("admin", self._hash_password("admin123"))
            )
            self.db.commit()
        finally:
            cursor.close()

    @staticmethod
    def _hash_password(password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    @staticmethod
    def _normalizar_rol(rol):
        roles = {
            "administrador": "Administrador",
            "encargado": "Encargado",
        }
        return roles.get(str(rol).lower(), "Encargado")
