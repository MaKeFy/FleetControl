-- Respaldo de base de datos: mantenimiento_maquinaria
-- Generado: 2026-05-27 01:21:02
SET FOREIGN_KEY_CHECKS=0;

-- Tabla `auditoria_eliminacion_ordenes`
DROP TABLE IF EXISTS `auditoria_eliminacion_ordenes`;
CREATE TABLE `auditoria_eliminacion_ordenes` (
  `id_auditoria` int NOT NULL AUTO_INCREMENT,
  `id_orden_original` int NOT NULL,
  `folio` varchar(20) DEFAULT NULL,
  `id_maquina` int DEFAULT NULL,
  `tipo` varchar(20) DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `fecha_creacion` date DEFAULT NULL,
  `fecha_cierre` date DEFAULT NULL,
  `descripcion_falla` text,
  `costo_total` float DEFAULT NULL,
  `motivo` text NOT NULL,
  `usuario` varchar(100) NOT NULL,
  `fecha_eliminacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_auditoria`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `auditoria_eliminacion_ordenes` (`id_auditoria`, `id_orden_original`, `folio`, `id_maquina`, `tipo`, `estado`, `fecha_creacion`, `fecha_cierre`, `descripcion_falla`, `costo_total`, `motivo`, `usuario`, `fecha_eliminacion`) VALUES (1, 37, NULL, 3, 'Preventivo', 'Abierta', '2026-04-20', NULL, 'SISTEMA: Mantenimiento preventivo alcanzado para el plan ''test 100 h id 3''.', 0.0, 'Duplicacion', 'admin', '2026-04-20 11:21:50');
INSERT INTO `auditoria_eliminacion_ordenes` (`id_auditoria`, `id_orden_original`, `folio`, `id_maquina`, `tipo`, `estado`, `fecha_creacion`, `fecha_cierre`, `descripcion_falla`, `costo_total`, `motivo`, `usuario`, `fecha_eliminacion`) VALUES (2, 35, NULL, 6, 'Preventivo', 'Abierta', '2026-04-20', NULL, 'SISTEMA: Mantenimiento preventivo alcanzado para el plan ''test 250h id 3''.', 0.0, 'duplicacion', 'admin', '2026-04-20 11:27:36');
INSERT INTO `auditoria_eliminacion_ordenes` (`id_auditoria`, `id_orden_original`, `folio`, `id_maquina`, `tipo`, `estado`, `fecha_creacion`, `fecha_cierre`, `descripcion_falla`, `costo_total`, `motivo`, `usuario`, `fecha_eliminacion`) VALUES (3, 34, NULL, 6, 'Preventivo', 'Abierta', '2026-04-20', NULL, 'SISTEMA: Mantenimiento preventivo alcanzado para el plan ''test 250h id 3''.', 0.0, 'duplicacion', 'admin', '2026-04-20 11:27:50');

-- Tabla `calendario_eventos`
DROP TABLE IF EXISTS `calendario_eventos`;
CREATE TABLE `calendario_eventos` (
  `id_evento` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(60) NOT NULL,
  `descripcion` text NOT NULL,
  `entidad` varchar(60) DEFAULT NULL,
  `id_referencia` int DEFAULT NULL,
  `fecha_evento` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_evento`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `calendario_eventos` (`id_evento`, `tipo`, `descripcion`, `entidad`, `id_referencia`, `fecha_evento`) VALUES (1, 'Creación de plan', 'Plan creado: Mantenimiento prueba cada 250 h', 'planes', 4, '2026-04-20 11:55:16');
INSERT INTO `calendario_eventos` (`id_evento`, `tipo`, `descripcion`, `entidad`, `id_referencia`, `fecha_evento`) VALUES (2, 'Nueva unidad', 'Nueva unidad registrada: Unidad prueba 2020 (12345678901234567)', 'maquinaria', 7, '2026-04-20 11:55:51');
INSERT INTO `calendario_eventos` (`id_evento`, `tipo`, `descripcion`, `entidad`, `id_referencia`, `fecha_evento`) VALUES (3, 'Finalización de orden', 'Orden #31 finalizada (Preventivo) - Caterpillar 320 GC', 'ordenes_servicio', 31, '2026-04-20 11:56:11');
INSERT INTO `calendario_eventos` (`id_evento`, `tipo`, `descripcion`, `entidad`, `id_referencia`, `fecha_evento`) VALUES (4, 'Incidencia', 'Incidencia registrada: hgvjhbn', 'ordenes_servicio', 40, '2026-04-20 12:47:52');
INSERT INTO `calendario_eventos` (`id_evento`, `tipo`, `descripcion`, `entidad`, `id_referencia`, `fecha_evento`) VALUES (5, 'Finalización de orden', 'Orden #40 finalizada (Correctivo) - JONH DEEREEh 2026', 'ordenes_servicio', 40, '2026-04-20 12:49:10');
INSERT INTO `calendario_eventos` (`id_evento`, `tipo`, `descripcion`, `entidad`, `id_referencia`, `fecha_evento`) VALUES (6, 'Registro de unidad', 'Registro de uso: 10.0 h en CATOS 2003', 'maquinaria', 4, '2026-04-27 12:05:10');
INSERT INTO `calendario_eventos` (`id_evento`, `tipo`, `descripcion`, `entidad`, `id_referencia`, `fecha_evento`) VALUES (7, 'Finalización de orden', 'Orden #38 finalizada (Preventivo) - JONH DEEREEh 2026', 'ordenes_servicio', 38, '2026-04-27 12:07:50');
INSERT INTO `calendario_eventos` (`id_evento`, `tipo`, `descripcion`, `entidad`, `id_referencia`, `fecha_evento`) VALUES (8, 'Incidencia', 'Incidencia registrada: No prende', 'ordenes_servicio', 41, '2026-04-27 12:08:58');
INSERT INTO `calendario_eventos` (`id_evento`, `tipo`, `descripcion`, `entidad`, `id_referencia`, `fecha_evento`) VALUES (9, 'Nueva unidad', 'Nueva unidad registrada: kjvkjv jhchcjcjhcj (1234567891234578)', 'maquinaria', 8, '2026-04-27 12:09:44');
INSERT INTO `calendario_eventos` (`id_evento`, `tipo`, `descripcion`, `entidad`, `id_referencia`, `fecha_evento`) VALUES (10, 'Creación de plan', 'Plan creado: test 320 cada 320 h', 'planes', 5, '2026-04-27 12:10:49');
INSERT INTO `calendario_eventos` (`id_evento`, `tipo`, `descripcion`, `entidad`, `id_referencia`, `fecha_evento`) VALUES (11, 'Registro de unidad', 'Registro de uso: 319.0 h en CATOS 2003', 'maquinaria', 4, '2026-04-27 12:11:13');
INSERT INTO `calendario_eventos` (`id_evento`, `tipo`, `descripcion`, `entidad`, `id_referencia`, `fecha_evento`) VALUES (12, 'Creación de plan', 'Plan creado: jdhgd cada 250 h', 'planes', 6, '2026-04-27 12:11:38');
INSERT INTO `calendario_eventos` (`id_evento`, `tipo`, `descripcion`, `entidad`, `id_referencia`, `fecha_evento`) VALUES (13, 'Registro de unidad', 'Registro de uso: 200.0 h en Unidad prueba 2020', 'maquinaria', 7, '2026-04-27 12:11:54');

-- Tabla `mantenimiento_planes`
DROP TABLE IF EXISTS `mantenimiento_planes`;
CREATE TABLE `mantenimiento_planes` (
  `id_plan` int NOT NULL AUTO_INCREMENT,
  `id_maquina` int DEFAULT NULL,
  `nombre_componente` varchar(100) DEFAULT NULL,
  `frecuencia_horas` float DEFAULT NULL,
  `descripcion` text,
  PRIMARY KEY (`id_plan`),
  KEY `fk_maquina_plan` (`id_maquina`),
  CONSTRAINT `fk_maquina_plan` FOREIGN KEY (`id_maquina`) REFERENCES `maquinaria` (`id_maquina`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Tabla `maquinaria`
DROP TABLE IF EXISTS `maquinaria`;
CREATE TABLE `maquinaria` (
  `id_maquina` int NOT NULL AUTO_INCREMENT,
  `vin` varchar(17) NOT NULL,
  `marca` varchar(50) DEFAULT NULL,
  `modelo` varchar(50) DEFAULT NULL,
  `horas_motor_total` float DEFAULT '0',
  `estado_color` varchar(20) DEFAULT 'Blanco',
  `ultimo_mantenimiento_horas` float DEFAULT '0',
  PRIMARY KEY (`id_maquina`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `maquinaria` (`id_maquina`, `vin`, `marca`, `modelo`, `horas_motor_total`, `estado_color`, `ultimo_mantenimiento_horas`) VALUES (3, '1234567890-=12345', 'JONH DEEREEh', '2026', 106.0, 'Negro', 106.0);
INSERT INTO `maquinaria` (`id_maquina`, `vin`, `marca`, `modelo`, `horas_motor_total`, `estado_color`, `ultimo_mantenimiento_horas`) VALUES (4, '12345678901234567', 'CATOS', '2003', 625.0, 'Rojo', 0.0);
INSERT INTO `maquinaria` (`id_maquina`, `vin`, `marca`, `modelo`, `horas_motor_total`, `estado_color`, `ultimo_mantenimiento_horas`) VALUES (6, 'TEST-VIN-2026', 'Caterpillar', '320 GC', 1250.0, 'Verde', 1250.0);
INSERT INTO `maquinaria` (`id_maquina`, `vin`, `marca`, `modelo`, `horas_motor_total`, `estado_color`, `ultimo_mantenimiento_horas`) VALUES (7, '12345678901234567', 'Unidad prueba', '2020', 200.0, 'Verde', 0.0);
INSERT INTO `maquinaria` (`id_maquina`, `vin`, `marca`, `modelo`, `horas_motor_total`, `estado_color`, `ultimo_mantenimiento_horas`) VALUES (8, '1234567891234578', 'kjvkjv', 'jhchcjcjhcj', 0.0, 'Blanco', 0.0);

-- Tabla `maquinaria_planes`
DROP TABLE IF EXISTS `maquinaria_planes`;
CREATE TABLE `maquinaria_planes` (
  `id_maquina` int NOT NULL,
  `id_plan` int NOT NULL,
  `ultima_ejecucion_horas` float DEFAULT '0' COMMENT 'Horómetro de la máquina la última vez que se completó este plan específico',
  `fecha_suscripcion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_maquina`,`id_plan`),
  KEY `id_plan` (`id_plan`),
  CONSTRAINT `maquinaria_planes_ibfk_1` FOREIGN KEY (`id_maquina`) REFERENCES `maquinaria` (`id_maquina`) ON DELETE CASCADE,
  CONSTRAINT `maquinaria_planes_ibfk_2` FOREIGN KEY (`id_plan`) REFERENCES `planes` (`id_plan`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `maquinaria_planes` (`id_maquina`, `id_plan`, `ultima_ejecucion_horas`, `fecha_suscripcion`) VALUES (3, 1, 0.0, '2026-04-14 09:29:47');
INSERT INTO `maquinaria_planes` (`id_maquina`, `id_plan`, `ultima_ejecucion_horas`, `fecha_suscripcion`) VALUES (3, 3, 106.0, '2026-04-14 09:49:42');
INSERT INTO `maquinaria_planes` (`id_maquina`, `id_plan`, `ultima_ejecucion_horas`, `fecha_suscripcion`) VALUES (3, 4, 0.0, '2026-04-20 11:55:16');
INSERT INTO `maquinaria_planes` (`id_maquina`, `id_plan`, `ultima_ejecucion_horas`, `fecha_suscripcion`) VALUES (4, 2, 0.0, '2026-04-14 09:34:22');
INSERT INTO `maquinaria_planes` (`id_maquina`, `id_plan`, `ultima_ejecucion_horas`, `fecha_suscripcion`) VALUES (4, 5, 0.0, '2026-04-27 12:10:49');
INSERT INTO `maquinaria_planes` (`id_maquina`, `id_plan`, `ultima_ejecucion_horas`, `fecha_suscripcion`) VALUES (6, 1, 1250.0, '2026-04-20 05:18:07');
INSERT INTO `maquinaria_planes` (`id_maquina`, `id_plan`, `ultima_ejecucion_horas`, `fecha_suscripcion`) VALUES (7, 6, 0.0, '2026-04-27 12:11:38');

-- Tabla `ordenes_servicio`
DROP TABLE IF EXISTS `ordenes_servicio`;
CREATE TABLE `ordenes_servicio` (
  `id_orden` int NOT NULL AUTO_INCREMENT,
  `id_maquina` int DEFAULT NULL,
  `folio` varchar(20) DEFAULT NULL,
  `fecha_creacion` date DEFAULT NULL,
  `fecha_cierre` date DEFAULT NULL,
  `tipo` enum('Preventivo','Correctivo') DEFAULT NULL,
  `descripcion_falla` text,
  `costo_total` float DEFAULT '0',
  `mecanico` varchar(100) DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `id_plan_preventivo` int DEFAULT NULL,
  PRIMARY KEY (`id_orden`),
  KEY `fk_maquina_orden` (`id_maquina`),
  KEY `fk_orden_plan` (`id_plan_preventivo`),
  CONSTRAINT `fk_maquina_orden` FOREIGN KEY (`id_maquina`) REFERENCES `maquinaria` (`id_maquina`) ON DELETE CASCADE,
  CONSTRAINT `fk_orden_plan` FOREIGN KEY (`id_plan_preventivo`) REFERENCES `planes` (`id_plan`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `ordenes_servicio` (`id_orden`, `id_maquina`, `folio`, `fecha_creacion`, `fecha_cierre`, `tipo`, `descripcion_falla`, `costo_total`, `mecanico`, `estado`, `id_plan_preventivo`) VALUES (26, 3, NULL, '2026-04-20', '2026-04-20', 'Preventivo', 'SISTEMA: Mantenimiento preventivo alcanzado para el plan ''test 100 h id 3''.
Notas Cierre: Se realizo cambio de aceite', 700.0, NULL, 'Cerrada', NULL);
INSERT INTO `ordenes_servicio` (`id_orden`, `id_maquina`, `folio`, `fecha_creacion`, `fecha_cierre`, `tipo`, `descripcion_falla`, `costo_total`, `mecanico`, `estado`, `id_plan_preventivo`) VALUES (27, 6, NULL, '2026-04-20', '2026-04-20', 'Preventivo', 'SISTEMA: Mantenimiento preventivo alcanzado para el plan ''test 250h id 3''.
Notas Cierre: Prueba de repuestos', 5200.0, NULL, 'Cerrada', NULL);
INSERT INTO `ordenes_servicio` (`id_orden`, `id_maquina`, `folio`, `fecha_creacion`, `fecha_cierre`, `tipo`, `descripcion_falla`, `costo_total`, `mecanico`, `estado`, `id_plan_preventivo`) VALUES (28, 3, 'MAN-0023', '2026-04-20', '2026-04-20', 'Correctivo', 'in
Notas Cierre: cambio bujia', 200.0, NULL, 'Cerrada', NULL);
INSERT INTO `ordenes_servicio` (`id_orden`, `id_maquina`, `folio`, `fecha_creacion`, `fecha_cierre`, `tipo`, `descripcion_falla`, `costo_total`, `mecanico`, `estado`, `id_plan_preventivo`) VALUES (29, 6, NULL, '2026-04-20', '2026-04-20', 'Preventivo', 'SISTEMA: Mantenimiento preventivo alcanzado para el plan ''test 250h id 3''.
Notas Cierre: Prueba de servicio', 20300.0, NULL, 'Cerrada', NULL);
INSERT INTO `ordenes_servicio` (`id_orden`, `id_maquina`, `folio`, `fecha_creacion`, `fecha_cierre`, `tipo`, `descripcion_falla`, `costo_total`, `mecanico`, `estado`, `id_plan_preventivo`) VALUES (30, 6, NULL, '2026-04-20', '2026-04-20', 'Preventivo', 'SISTEMA: Mantenimiento preventivo alcanzado para el plan ''test 250h id 3''.
Notas Cierre: Prueba test', 2030.0, NULL, 'Cerrada', NULL);
INSERT INTO `ordenes_servicio` (`id_orden`, `id_maquina`, `folio`, `fecha_creacion`, `fecha_cierre`, `tipo`, `descripcion_falla`, `costo_total`, `mecanico`, `estado`, `id_plan_preventivo`) VALUES (31, 6, NULL, '2026-04-20', '2026-04-20', 'Preventivo', 'SISTEMA: Mantenimiento preventivo alcanzado para el plan ''test 250h id 3''.
Notas Cierre: Motivo: test 250h id 3', 0.0, NULL, 'Cerrada', NULL);
INSERT INTO `ordenes_servicio` (`id_orden`, `id_maquina`, `folio`, `fecha_creacion`, `fecha_cierre`, `tipo`, `descripcion_falla`, `costo_total`, `mecanico`, `estado`, `id_plan_preventivo`) VALUES (32, 6, NULL, '2026-04-20', NULL, 'Preventivo', 'SISTEMA: Mantenimiento preventivo alcanzado para el plan ''test 250h id 3''.', 0.0, NULL, 'Abierta', NULL);
INSERT INTO `ordenes_servicio` (`id_orden`, `id_maquina`, `folio`, `fecha_creacion`, `fecha_cierre`, `tipo`, `descripcion_falla`, `costo_total`, `mecanico`, `estado`, `id_plan_preventivo`) VALUES (33, 6, NULL, '2026-04-20', '2026-04-20', 'Preventivo', 'SISTEMA: Mantenimiento preventivo alcanzado para el plan ''test 250h id 3''.
Notas Cierre: something happend', 2040.0, NULL, 'Cerrada', NULL);
INSERT INTO `ordenes_servicio` (`id_orden`, `id_maquina`, `folio`, `fecha_creacion`, `fecha_cierre`, `tipo`, `descripcion_falla`, `costo_total`, `mecanico`, `estado`, `id_plan_preventivo`) VALUES (38, 3, NULL, '2026-04-20', '2026-04-27', 'Preventivo', 'SISTEMA: Mantenimiento preventivo alcanzado para el plan ''test 100 h id 3''.
Notas Cierre: Motivo: test 100 h id 3', 130.0, NULL, 'Cerrada', 3);
INSERT INTO `ordenes_servicio` (`id_orden`, `id_maquina`, `folio`, `fecha_creacion`, `fecha_cierre`, `tipo`, `descripcion_falla`, `costo_total`, `mecanico`, `estado`, `id_plan_preventivo`) VALUES (39, 6, NULL, '2026-04-20', '2026-04-20', 'Preventivo', 'SISTEMA: Mantenimiento preventivo alcanzado para el plan ''test 250h id 3''.
Notas Cierre: Motivo: test 250h id 3', 5000.0, NULL, 'Cerrada', 1);
INSERT INTO `ordenes_servicio` (`id_orden`, `id_maquina`, `folio`, `fecha_creacion`, `fecha_cierre`, `tipo`, `descripcion_falla`, `costo_total`, `mecanico`, `estado`, `id_plan_preventivo`) VALUES (40, 3, 'MAN-4752', '2026-04-20', '2026-04-20', 'Correctivo', 'hgvjhbn
Notas Cierre: Motivo: incidencia', 0.0, NULL, 'Cerrada', NULL);
INSERT INTO `ordenes_servicio` (`id_orden`, `id_maquina`, `folio`, `fecha_creacion`, `fecha_cierre`, `tipo`, `descripcion_falla`, `costo_total`, `mecanico`, `estado`, `id_plan_preventivo`) VALUES (41, 3, 'MAN-0858', '2026-04-27', NULL, 'Correctivo', 'No prende', 0.0, NULL, 'Abierta', NULL);
INSERT INTO `ordenes_servicio` (`id_orden`, `id_maquina`, `folio`, `fecha_creacion`, `fecha_cierre`, `tipo`, `descripcion_falla`, `costo_total`, `mecanico`, `estado`, `id_plan_preventivo`) VALUES (42, 4, NULL, '2026-04-27', NULL, 'Preventivo', 'SISTEMA: Mantenimiento preventivo alcanzado para el plan ''test 400h id 4''.', 0.0, NULL, 'Abierta', 2);
INSERT INTO `ordenes_servicio` (`id_orden`, `id_maquina`, `folio`, `fecha_creacion`, `fecha_cierre`, `tipo`, `descripcion_falla`, `costo_total`, `mecanico`, `estado`, `id_plan_preventivo`) VALUES (43, 4, NULL, '2026-04-27', NULL, 'Preventivo', 'SISTEMA: Mantenimiento preventivo alcanzado para el plan ''test 320''.', 0.0, NULL, 'Abierta', 5);

-- Tabla `planes`
DROP TABLE IF EXISTS `planes`;
CREATE TABLE `planes` (
  `id_plan` int NOT NULL AUTO_INCREMENT,
  `nombre_plan` varchar(100) NOT NULL,
  `intervalo_horas` int NOT NULL,
  PRIMARY KEY (`id_plan`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `planes` (`id_plan`, `nombre_plan`, `intervalo_horas`) VALUES (1, 'test 250h id 3', 250);
INSERT INTO `planes` (`id_plan`, `nombre_plan`, `intervalo_horas`) VALUES (2, 'test 400h id 4', 400);
INSERT INTO `planes` (`id_plan`, `nombre_plan`, `intervalo_horas`) VALUES (3, 'test 100 h id 3', 100);
INSERT INTO `planes` (`id_plan`, `nombre_plan`, `intervalo_horas`) VALUES (4, 'Mantenimiento prueba', 250);
INSERT INTO `planes` (`id_plan`, `nombre_plan`, `intervalo_horas`) VALUES (5, 'test 320', 320);
INSERT INTO `planes` (`id_plan`, `nombre_plan`, `intervalo_horas`) VALUES (6, 'jdhgd', 250);

-- Tabla `registro_uso`
DROP TABLE IF EXISTS `registro_uso`;
CREATE TABLE `registro_uso` (
  `id_registro` int NOT NULL AUTO_INCREMENT,
  `id_maquina` int DEFAULT NULL,
  `fecha_registro` date DEFAULT NULL,
  `lectura_horas` float DEFAULT NULL,
  PRIMARY KEY (`id_registro`),
  KEY `fk_maquina_uso` (`id_maquina`),
  CONSTRAINT `fk_maquina_uso` FOREIGN KEY (`id_maquina`) REFERENCES `maquinaria` (`id_maquina`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Tabla `repuestos`
DROP TABLE IF EXISTS `repuestos`;
CREATE TABLE `repuestos` (
  `id_repuesto` int NOT NULL AUTO_INCREMENT,
  `id_orden` int DEFAULT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `costo_unitario` float DEFAULT NULL,
  PRIMARY KEY (`id_repuesto`),
  KEY `fk_orden_repuesto` (`id_orden`),
  CONSTRAINT `fk_orden_repuesto` FOREIGN KEY (`id_orden`) REFERENCES `ordenes_servicio` (`id_orden`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `repuestos` (`id_repuesto`, `id_orden`, `nombre`, `costo_unitario`) VALUES (1, 29, 'refa 1', 20000.0);
INSERT INTO `repuestos` (`id_repuesto`, `id_orden`, `nombre`, `costo_unitario`) VALUES (2, 30, 'rf', 2000.0);
INSERT INTO `repuestos` (`id_repuesto`, `id_orden`, `nombre`, `costo_unitario`) VALUES (3, 33, 'añadir', 2000.0);
INSERT INTO `repuestos` (`id_repuesto`, `id_orden`, `nombre`, `costo_unitario`) VALUES (4, 39, 'w200', 5000.0);
INSERT INTO `repuestos` (`id_repuesto`, `id_orden`, `nombre`, `costo_unitario`) VALUES (5, 38, 'repuesto 1', 50.0);

-- Tabla `tareas_plan`
DROP TABLE IF EXISTS `tareas_plan`;
CREATE TABLE `tareas_plan` (
  `id_tarea` int NOT NULL AUTO_INCREMENT,
  `id_plan` int DEFAULT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_tarea`),
  KEY `id_plan` (`id_plan`),
  CONSTRAINT `tareas_plan_ibfk_1` FOREIGN KEY (`id_plan`) REFERENCES `planes` (`id_plan`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `tareas_plan` (`id_tarea`, `id_plan`, `descripcion`) VALUES (1, 1, 'oiha');
INSERT INTO `tareas_plan` (`id_tarea`, `id_plan`, `descripcion`) VALUES (2, 1, 'oinonokn');
INSERT INTO `tareas_plan` (`id_tarea`, `id_plan`, `descripcion`) VALUES (3, 2, 'ioog');
INSERT INTO `tareas_plan` (`id_tarea`, `id_plan`, `descripcion`) VALUES (4, 2, 'kjboubo');
INSERT INTO `tareas_plan` (`id_tarea`, `id_plan`, `descripcion`) VALUES (5, 3, 'qwoihoih');
INSERT INTO `tareas_plan` (`id_tarea`, `id_plan`, `descripcion`) VALUES (6, 4, 'check fecha');
INSERT INTO `tareas_plan` (`id_tarea`, `id_plan`, `descripcion`) VALUES (7, 5, 'Cambio de aceite');
INSERT INTO `tareas_plan` (`id_tarea`, `id_plan`, `descripcion`) VALUES (8, 6, 'lig');

-- Tabla `usuarios`
DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE `usuarios` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `rol` enum('Administrador','Encargado') NOT NULL,
  PRIMARY KEY (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `usuarios` (`id_usuario`, `nombre`, `password_hash`, `rol`) VALUES (1, 'admin', '5bd965c84954b3b9fb902d863b83496ee0df854b8657233687bce503212312ca', 'Administrador');
INSERT INTO `usuarios` (`id_usuario`, `nombre`, `password_hash`, `rol`) VALUES (2, 'encargado_01', 'd12cedaa9d713eb0ec3a3069e1f047abdb352a7ac72fc07e2d382cb29796e7bf', 'Encargado');

SET FOREIGN_KEY_CHECKS=1;