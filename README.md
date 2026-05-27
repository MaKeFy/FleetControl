# FleetControl

FleetControl es una aplicacion de escritorio para el control de mantenimiento de maquinaria agricola. Permite administrar la flota, registrar horas motor, crear planes preventivos, atender incidencias correctivas, consultar eventos en calendario y generar reportes locales.

## Contenido principal

El sistema incluye los modulos descritos en el manual de usuario:

- **Inicio de sesion:** acceso mediante credenciales y roles.
- **Vista de Flota:** tarjetas de maquinaria con ID, marca, modelo, VIN/serie, horas acumuladas y estado visual.
- **Gestion de maquinaria:** alta, consulta, edicion y eliminacion de unidades.
- **Registro de horas motor:** captura de jornadas de uso para actualizar el horometro acumulado.
- **Planes de mantenimiento:** creacion, edicion, eliminacion y exportacion de planes preventivos.
- **Servicio y mantenimiento:** registro de incidencias, gestion de ordenes, cierre de servicios, repuestos y costos.
- **Calendario mensual:** consulta de eventos registrados por el sistema.
- **Reportes y respaldos:** hoja de servicio HTML, reporte Excel, PDF de plan y respaldo SQL.

## Estados de maquinaria

- **Verde:** unidad dentro del rango normal de mantenimiento.
- **Amarillo:** mantenimiento preventivo proximo.
- **Rojo:** mantenimiento preventivo vencido.
- **Negro:** incidencia correctiva abierta.
- **Blanco/Gris:** unidad sin plan asociado o sin estado preventivo calculable.

## Instalacion y ejecucion

La version distribuible se encuentra en la carpeta `dist/`.

1. Instalar y configurar MySQL.
2. Crear o importar la base de datos de prueba.
3. Copiar `mysql_config.example.txt` como `mysql_config.txt`.
4. Editar `mysql_config.txt` con las credenciales locales de MySQL.
5. Colocar `mysql_config.txt` junto al ejecutable en `dist/`.
6. Ejecutar:

```text
dist/FleetControl.exe
```

> `mysql_config.txt` no se sube al repositorio porque contiene credenciales personales de MySQL.

## Requisitos

- Windows.
- MySQL Server instalado y en ejecucion.
- Base de datos local llamada `mantenimiento_maquinaria`.
- Usuario MySQL con permisos sobre esa base de datos.
- Archivo `mysql_config.txt` junto al ejecutable.

## Base de datos de prueba

El repositorio incluye un respaldo SQL de prueba en:

```text
dist/respaldo_mantenimiento_maquinaria.sql
```

Puede importarse en MySQL para crear/cargar datos de prueba. Ejemplo:

```bash
mysql -u root -p mantenimiento_maquinaria < dist/respaldo_mantenimiento_maquinaria.sql
```

Si la base de datos aun no existe, crearla antes:

```sql
CREATE DATABASE mantenimiento_maquinaria;
```

## Configuracion de MySQL

El archivo de configuracion debe llamarse exactamente:

```text
mysql_config.txt
```

Cuando se ejecuta desde codigo fuente, debe estar en la raiz de `Control de mantenimiento en maquinaria`. Cuando se ejecuta el `.exe`, debe estar junto a `FleetControl.exe` dentro de `dist/`.

Formato esperado (se recomienda utilizar un usuario con permisos en la BD en vez del usuario root):

```text
host='localhost'
user='root'
password='TU_CONTRASENA_MYSQL'
database='mantenimiento_maquinaria'
```

Tambien se incluye una plantilla:

```text
mysql_config.example.txt
```

## Credenciales de aplicacion

En los datos de prueba, se incluyen dos usuarios. El administrador y un usuario normal con rol de Encargado:

Administrador:
```text
Usuario: admin
Contraseña: A7adm.56
```

Usuario normal:
```text
Usuario: encargado_01
Contraseña: E7ecr.99
```

Si la tabla `usuarios` esta vacia, la aplicacion crea automaticamente el usuario inicial:

```text
Usuario: admin
Contrasena: admin123
Rol: Administrador
```

El respaldo SQL de prueba incluye usuarios de ejemplo, entre ellos `admin` y `encargado_01`. Las contrasenas de usuarios se almacenan como hash SHA-256 en la tabla `usuarios`.

## Ejecucion desde codigo fuente

Para ejecutar el proyecto sin el `.exe`:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Antes de ejecutar, crear `mysql_config.txt` en la raiz del proyecto con la configuracion de MySQL.

## Manual de usuario.
Para pasos más detallados acerca del uso de la aplicación, véase el Manual de Usuario - FleetControl:

- https://drive.google.com/file/d/1Dl_kDqRZbYGm2QFZF6eSh3ZVGPjNvxGH/view?usp=sharing
