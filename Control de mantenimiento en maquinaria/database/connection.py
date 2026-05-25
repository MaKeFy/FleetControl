import sys
from pathlib import Path

import mysql.connector
from mysql.connector import Error


class DatabaseConnection:
    _instance = None
    CONFIG_FILE = "mysql_config.txt"

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            try:
                cls._instance = mysql.connector.connect(**cls._leer_configuracion())
            except (Error, OSError, ValueError) as e:
                print(f"Error crítico de conexión: {e}")
        return cls._instance

    @classmethod
    def _leer_configuracion(cls):
        ruta_config = cls._ruta_configuracion()
        if not ruta_config.exists():
            raise FileNotFoundError(
                f"No se encontro el archivo de configuracion MySQL: {ruta_config}"
            )

        configuracion = {}
        with ruta_config.open("r", encoding="utf-8") as archivo:
            for numero_linea, linea in enumerate(archivo, start=1):
                linea = linea.strip()
                if not linea or linea.startswith("#"):
                    continue
                if "=" not in linea:
                    raise ValueError(
                        f"Linea invalida en {ruta_config} ({numero_linea}): {linea}"
                    )

                clave, valor = linea.split("=", 1)
                configuracion[clave.strip()] = valor.strip().strip("\"'")

        requeridos = {"host", "user", "password", "database"}
        faltantes = requeridos - set(configuracion)
        if faltantes:
            raise ValueError(
                f"Faltan datos en {ruta_config}: {', '.join(sorted(faltantes))}"
            )

        return {clave: configuracion[clave] for clave in requeridos}

    @classmethod
    def _ruta_configuracion(cls):
        if getattr(sys, "frozen", False):
            return Path(sys.executable).resolve().parent / cls.CONFIG_FILE
        return Path(__file__).resolve().parent.parent / cls.CONFIG_FILE
