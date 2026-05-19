from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QPushButton, QFrame, QLabel, QStackedWidget, QLineEdit, QSpacerItem, QSizePolicy,
                             QDialog, QMessageBox, QInputDialog, QFileDialog, QApplication)
from PySide6.QtCore import Qt
# Importamos la Vista y el Controlador
from controllers.servicio_controller import ServicioController
from views import vista_servicios
from views.vista_flota import VistaFlota
from controllers.flota_controller import FlotaController
from views.vista_planes import VistaPlanes
from controllers.planes_controller import PlanesController
from controllers.planes_controller import PlanesDAO
from views.dialogo_detalle import DialogoDetalleMaquinaria
from views.dialogo_maquinaria import DialogoMaquinaria
from PySide6.QtWidgets import QInputDialog

from views.vista_servicios import VistaServicios
from views.vista_calendario import VistaCalendario
from controllers.servicio_controller import ServicioController
from services.reportes_service import ReportesService
from services.backup_service import BackupService
from database.auth_dao import AuthDAO

class MainWindow(QMainWindow):
    def __init__(self, usuario=None):
        super().__init__()
        self.usuario = usuario or {"usuario": "local", "rol": "Administrador"}
        self.rol_actual = self.usuario.get("rol", "Administrador")
        self.setWindowTitle("FleetControl - Sistema de Gestión Agrícola")
        self.resize(1200, 800)
        
        # 1. Configurar UI Base
        self.central_widget = QWidget()
        # Forzamos fondo oscuro en el contenedor base para evitar destellos
        self.central_widget.setStyleSheet("background-color: #1e293b;") 
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.vista_planes = VistaPlanes()
        self.controlador_planes = PlanesController(self.vista_planes)
        
        self.vista_flota = VistaFlota()
        self.controlador_flota = FlotaController(self.vista_flota)
        self.vista_flota.set_controlador(self.controlador_flota)
        
        self.vista_servicios = VistaServicios()
        self.controlador_servicios = ServicioController(self.vista_servicios)
        self.vista_servicios.controlador = self.controlador_servicios

        self.vista_calendario = VistaCalendario()
        
        # 2. Setup de Componentes Visuales
        self.setup_sidebar()
        self.setup_content_area()
        
        # 4. Cargar datos iniciales desde la BD
        self.controlador_flota.refrescar_dashboard()

        
        self.maquina_seleccionada = None 
        self.plan_seleccionado = None
        self.tarjeta_plan_seleccionada_widget = None
        # Conectamos el botón de la toolbar superior
        self.btn_registrar_uso.clicked.connect(self.registrar_uso_seleccionado)
        self.btn_flota.clicked.connect(lambda: self.navegar_a(0))
        self.btn_config.clicked.connect(lambda: self.navegar_a(1))
        # Usar el nombre que tienes en tu botón de servicio
        self.btn_service.clicked.connect(self.mostrar_servicios)
        self.btn_calendario.clicked.connect(lambda: self.navegar_a(3))
        self.btn_imprimir.clicked.connect(self.generar_hoja_servicio)
        self.btn_exportar.clicked.connect(self.exportar_reportes_excel)
        
        self.controlador_planes.refrescar_contenido()
        self.aplicar_permisos()
        
        
    def setup_sidebar(self):
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(250)
        self.sidebar.setStyleSheet("background-color: #1e293b; border: none;")
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        
        lbl_logo = QLabel("FleetControl")
        lbl_logo.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 25px; color: #10b981; padding-left: 5px;")
        sidebar_layout.addWidget(lbl_logo)

        self.lbl_usuario = QLabel(f"{self.usuario.get('usuario')} - {self.rol_actual}")
        self.lbl_usuario.setStyleSheet("color: #94a3b8; font-size: 12px; padding-left: 5px; margin-bottom: 12px;")
        sidebar_layout.addWidget(self.lbl_usuario)

        self.btn_flota = QPushButton(" Vista de Flota")
        self.btn_service = QPushButton(" Servicio y Mantenimiento")
        self.btn_calendario = QPushButton(" Calendario Mensual")
        self.btn_config = QPushButton(" Configuración de Planes")
        self.btn_exportar_bd = QPushButton(" Exportar Base de Datos")
        self.btn_cambiar_usuario = QPushButton(" Cerrar Sesión")
        self.btn_salir = QPushButton(" Salir")

        for btn in [self.btn_flota, self.btn_service, self.btn_calendario, self.btn_config]:
            btn.setStyleSheet("""
                QPushButton { 
                    text-align: left; padding: 12px; border: none; font-size: 14px; 
                    border-radius: 5px; color: #cbd5e1; font-weight: 500;
                }
                QPushButton:hover { background-color: #334155; color: white; }
                QPushButton:pressed { background-color: #0f172a; }
            """)
            sidebar_layout.addWidget(btn)
            
        sidebar_layout.addStretch()
        self.btn_exportar_bd.setStyleSheet("""
            QPushButton {
                text-align: left; padding: 12px; border: 1px solid #0f766e;
                font-size: 14px; border-radius: 5px; color: #99f6e4; font-weight: 500;
            }
            QPushButton:hover { background-color: #0f766e; color: white; }
        """)
        self.btn_exportar_bd.clicked.connect(self.exportar_base_datos)
        sidebar_layout.addWidget(self.btn_exportar_bd)

        self.btn_cambiar_usuario.setStyleSheet("""
            QPushButton {
                text-align: left; padding: 12px; border: 1px solid #334155;
                font-size: 14px; border-radius: 5px; color: #cbd5e1; font-weight: 500;
            }
            QPushButton:hover { background-color: #334155; color: white; }
        """)
        self.btn_cambiar_usuario.clicked.connect(self.cerrar_sesion)
        sidebar_layout.addWidget(self.btn_cambiar_usuario)

        self.btn_salir.setStyleSheet("""
            QPushButton {
                text-align: left; padding: 12px; border: 1px solid #7f1d1d;
                font-size: 14px; border-radius: 5px; color: #fecaca; font-weight: 600;
            }
            QPushButton:hover { background-color: #dc2626; color: white; }
        """)
        self.btn_salir.clicked.connect(self.salir_aplicacion)
        sidebar_layout.addWidget(self.btn_salir)
        self.main_layout.addWidget(self.sidebar)
        

    def setup_content_area(self):
        right_container = QWidget()
        right_container.setStyleSheet("background-color: #f8fafc;") 
        
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # --- TOOLBAR COMPLETA ---
        self.toolbar = QFrame()
        self.toolbar.setFixedHeight(70)
        self.toolbar.setStyleSheet("background-color: white; border-bottom: 1px solid #e2e8f0;")
        
        toolbar_layout = QHBoxLayout(self.toolbar)
        toolbar_layout.setContentsMargins(20, 0, 20, 0)
        
        # Botones de acción (Estilo Figma)
        self.btn_registrar = QPushButton("Registrar Uso")
        self.btn_registrar.setStyleSheet("""
            background-color: #2563eb; color: white; padding: 10px 18px; 
            border-radius: 6px; font-weight: bold; font-size: 13px;
        """)
   
        # Boton de registro de nueva maquinaria     
        self.btn_accion_principal = QPushButton("+ Añadir Unidad")
        self.btn_accion_principal.setStyleSheet("""
            background-color: #10b981; color: white; padding: 10px 18px; 
            border-radius: 6px; font-weight: bold; font-size: 13px;
        """)
        
        self.btn_accion_principal.clicked.connect(self.abrir_registro_maquinaria)
        


        # El botón "Registrar Uso" lo mantenemos para el UPDATE de horas
        self.btn_registrar_uso = QPushButton("Registrar Horas") 
        self.btn_registrar_uso.setStyleSheet("""
            background-color: #2563eb; color: white; padding: 10px 18px; 
            border-radius: 6px; font-weight: bold; font-size: 13px;
        """)
        # Otros botones (Outline style)
        btn_outline = "background-color: white; border: 1px solid #cbd5e1; color: #475569; padding: 10px 15px; border-radius: 6px; font-weight: 500;"
        
        self.btn_imprimir = QPushButton("Imprimir Hoja")
        self.btn_imprimir.setStyleSheet(btn_outline)
        
        self.btn_exportar = QPushButton("Exportar Reportes")
        self.btn_exportar.setStyleSheet(btn_outline)

        # Barra de Búsqueda
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Buscar maquinaria por ID, marca o modelo...")
        self.search_bar.setFixedWidth(350)
        self.search_bar.setStyleSheet("""
            QLineEdit {
                padding: 10px; 
                border: 1px solid #e2e8f0; 
                border-radius: 8px; 
                background-color: #f9fafb; 
                color: #1e293b;            /* <--- ESTA LÍNEA CORRIGE EL TEXTO INVISIBLE */
                selection-background-color: #2563eb;
            }
            QLineEdit:focus { 
                border: 1px solid #2563eb; 
                background-color: white; 
                color: #0f172a;           /* Texto aún más oscuro al escribir */
            }
        """)
        # Organizar Toolbar
        toolbar_layout.addWidget(self.btn_accion_principal) # El nuevo botón verde
        toolbar_layout.addSpacing(10)
        toolbar_layout.addWidget(self.btn_registrar_uso) # El botón azul de horas
        toolbar_layout.addSpacing(10)
        toolbar_layout.addWidget(self.btn_imprimir)
        toolbar_layout.addSpacing(10)
        toolbar_layout.addWidget(self.btn_exportar)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.search_bar)

        # --- ÁREA DE CONTENIDO DINÁMICO ---
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background-color: #f8fafc; border: none;")
        
        # Inicializamos la Vista de Flota
        self.content_stack.addWidget(self.vista_flota)    # Index 0
        self.content_stack.addWidget(self.vista_planes)   # Index 1
        self.content_stack.addWidget(self.vista_servicios) # Index 2
        self.content_stack.addWidget(self.vista_calendario) # Index 3
        
        # Ensamblaje final
        right_layout.addWidget(self.toolbar)
        right_layout.addWidget(self.content_stack)
        
        self.main_layout.addWidget(right_container)

        # Conectamos el botón de la sidebar
        self.btn_config.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.vista_planes))
        self.btn_service.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.vista_servicios))

        
        
        self.content_stack.currentChanged.connect(self.al_cambiar_vista)
        self.al_cambiar_vista(0)

    def navegar_a(self, indice):
        if indice == 1 and self.rol_actual != "Administrador":
            QMessageBox.warning(self, "Acceso restringido", "Solo el Administrador puede modificar planes.")
            return
        self.content_stack.setCurrentIndex(indice)
        self.al_cambiar_vista(indice)
        
    def filtrar_busqueda(self):
        """Llama al controlador para filtrar las tarjetas según el texto ingresado"""
        texto = self.search_bar.text()
        self.controlador_flota.refrescar_dashboard(filtro=texto)
        
    def abrir_registro_maquinaria(self):
        if self.rol_actual != "Administrador":
            QMessageBox.warning(self, "Acceso restringido", "Solo el Administrador puede registrar maquinaria.")
            return
        dialogo = DialogoMaquinaria(self)
        if dialogo.exec(): # Si el usuario presiona "Guardar"
            datos = dialogo.obtener_datos()
            datos["horas"] = float(datos.get("horas") or 0)
            
            # Validación de longitud máxima compatible con la BD: varchar(17)
            if len(datos['vin']) > 17:
                QMessageBox.warning(self, "Error", "El VIN debe tener máximo 17 caracteres.")
                return
                
            exito = self.controlador_flota.registrar_unidad_automatica(datos)
            
            if exito:
                QMessageBox.information(self, "Éxito", "Maquinaria registrada correctamente.")
                self.controlador_flota.refrescar_dashboard() # Actualiza el Grid automáticamente
                
    # views/main_window.py

    def mostrar_servicios(self):
        """Cambia a la vista de servicios y actualiza el listado de órdenes."""
        self.controlador_servicios.cargar_ordenes()
        self.content_stack.setCurrentWidget(self.vista_servicios)
        self.al_cambiar_vista(2)

    def generar_hoja_servicio(self):
        if self.content_stack.currentIndex() == 1:
            self.exportar_plan_pdf_seleccionado()
            return

        id_orden, ok = QInputDialog.getInt(
            self,
            "Hoja de Servicio",
            "Ingrese el ID de la orden de servicio:",
            1,
            1,
            999999999,
            1
        )
        if not ok:
            return

        orden = self.controlador_servicios.dao.obtener_detalle_orden_servicio(id_orden)
        if not orden:
            QMessageBox.warning(self, "Sin resultados", "No se encontro una orden con ese ID.")
            return

        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Hoja de Servicio",
            f"hoja_servicio_{id_orden}.html",
            "Documento HTML (*.html)"
        )
        if not ruta:
            return

        repuestos = self.controlador_servicios.dao.obtener_repuestos_orden(id_orden)
        ReportesService.generar_hoja_servicio_html(orden, repuestos, ruta)
        QMessageBox.information(self, "Hoja generada", f"Hoja de servicio guardada en:\n{ruta}")

    def exportar_reportes_excel(self):
        if self.rol_actual != "Administrador":
            QMessageBox.warning(self, "Acceso restringido", "Solo el Administrador puede exportar reportes.")
            return
        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar Reportes",
            "reporte_servicios.xlsx",
            "Excel (*.xlsx)"
        )
        if not ruta:
            return
        if not ruta.lower().endswith(".xlsx"):
            ruta += ".xlsx"

        ordenes = self.controlador_servicios.dao.obtener_ordenes_para_reporte()
        if not ordenes:
            QMessageBox.warning(self, "Sin datos", "No hay ordenes de servicio para exportar.")
            return

        ReportesService.exportar_ordenes_xlsx(ordenes, ruta)
        QMessageBox.information(self, "Reporte exportado", f"Reporte Excel guardado en:\n{ruta}")

    def seleccionar_plan(self, tarjeta_widget):
        if self.tarjeta_plan_seleccionada_widget == tarjeta_widget:
            tarjeta_widget.set_seleccionada(False)
            self.tarjeta_plan_seleccionada_widget = None
            self.plan_seleccionado = None
            return

        if self.tarjeta_plan_seleccionada_widget:
            self.tarjeta_plan_seleccionada_widget.set_seleccionada(False)

        self.tarjeta_plan_seleccionada_widget = tarjeta_widget
        self.plan_seleccionado = tarjeta_widget.data
        tarjeta_widget.set_seleccionada(True)

    def exportar_plan_pdf_seleccionado(self):
        if self.rol_actual != "Administrador":
            QMessageBox.warning(self, "Acceso restringido", "Solo el Administrador puede exportar planes.")
            return

        if not self.plan_seleccionado:
            QMessageBox.warning(self, "Plan requerido", "Selecciona un plan con un click antes de exportar.")
            return

        id_plan = self.plan_seleccionado.get("id_plan")
        detalle = self.controlador_planes.obtener_detalle_reporte_plan(id_plan)
        if not detalle:
            QMessageBox.warning(self, "Sin datos", "No se pudo obtener la información del plan seleccionado.")
            return

        nombre = str(self.plan_seleccionado.get("nombre", "plan")).replace(" ", "_")
        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar Plan a PDF",
            f"reporte_plan_{nombre}.pdf",
            "PDF (*.pdf)"
        )
        if not ruta:
            return
        if not ruta.lower().endswith(".pdf"):
            ruta += ".pdf"

        ReportesService.generar_reporte_plan_pdf(detalle, ruta)
        QMessageBox.information(self, "PDF generado", f"Reporte PDF guardado en:\n{ruta}")
        
    def abrir_detalle_maquinaria(self, datos):
        """Punto de entrada: Abre la vista de consulta (Lectura)"""
        detalle = DialogoDetalleMaquinaria(parent=self, datos=datos)
        
        # Si el usuario presiona "Editar Datos", el diálogo devuelve el código 20
        resultado = detalle.exec()
        if resultado == 20:
            self.ejecutar_flujo_edicion(datos)
        elif resultado == 30:
            self.eliminar_unidad_con_credenciales(datos)
                
                
    def seleccionar_maquinaria(self, tarjeta_widget):
        """Maneja la selección única y el toggle (deseleccionar)"""
        
        # Caso 1: El usuario hace clic en la tarjeta que YA ESTABA seleccionada
        if hasattr(self, 'tarjeta_seleccionada_widget') and self.tarjeta_seleccionada_widget == tarjeta_widget:
            self.deseleccionar_todo()
            return

        # Caso 2: Hay otra tarjeta seleccionada previamente, hay que "apagarla"
        if hasattr(self, 'tarjeta_seleccionada_widget') and self.tarjeta_seleccionada_widget:
            self.tarjeta_seleccionada_widget.set_seleccionada(False)

        # Caso 3: Seleccionar la nueva tarjeta
        self.tarjeta_seleccionada_widget = tarjeta_widget
        self.maquina_seleccionada = tarjeta_widget.data
        self.tarjeta_seleccionada_widget.set_seleccionada(True)
        print(f"Seleccionada: {self.maquina_seleccionada['id']}")
        
            
    
    def deseleccionar_todo(self):
        """Limpia el estado de selección"""
        if hasattr(self, 'tarjeta_seleccionada_widget') and self.tarjeta_seleccionada_widget:
            self.tarjeta_seleccionada_widget.set_seleccionada(False)
        
        self.tarjeta_seleccionada_widget = None
        self.maquina_seleccionada = None
        print("Selección limpiada")
    
    def registrar_uso_seleccionado(self):
        """Acción al presionar el botón de la barra superior"""
        if hasattr(self, 'maquina_seleccionada') and self.maquina_seleccionada:
            self.ejecutar_acumulacion_horas(self.maquina_seleccionada)
        else:
            QMessageBox.warning(self, "Selección Requerida", 
                                "Por favor, selecciona una máquina haciendo clic en su tarjeta.")

    def ejecutar_acumulacion_horas(self, datos=None):
        """
        Registra el uso de horas motor. 
        Puede recibir datos directamente o usar la selección global.
        """
        # 1. Priorizar datos recibidos o buscar la selección actual
        maquina = datos if datos else self.maquina_seleccionada

        if not maquina:
            QMessageBox.warning(self, "Aviso", "Por favor, seleccione una unidad primero.")
            return

        from PySide6.QtWidgets import QInputDialog
        
        # 2. Configuración balanceada: Jornadas de 0.1 a 500h (para acumulados semanales)
        num, ok = QInputDialog.getDouble(
            self, 
            "Registrar Jornada", 
            f"Unidad: {maquina.get('marca')} {maquina.get('modelo')}\nIngrese horas a sumar:",
            0.0,      # Valor inicial
            0.1,      # minValue: Evitamos registros de 0 o negativos
            500.0,    # maxValue: Un límite razonable para evitar errores de dedo masivos
            1         # Decimales
        )
        
        if ok and num > 0:
            id_maquina = maquina.get('id')
            # 3. Delegar la lógica de suma al controlador
            if self.controlador_flota.sumar_uso(id_maquina, num):
                QMessageBox.information(self, "Éxito", f"Se registraron {num}h adicionales.")
                
                # El controlador ya debería encargarse de refrescar_dashboard y actualizar_color_por_plan
                # Pero forzamos el refresco para asegurar la actualización visual inmediata
                self.controlador_flota.refrescar_dashboard()
                
                # Limpieza de selección visual si aplica
                if hasattr(self, 'deseleccionar_todo'):
                    self.deseleccionar_todo()
                
    def ejecutar_flujo_edicion(self, datos):
        if self.rol_actual != "Administrador":
            QMessageBox.warning(self, "Acceso restringido", "Solo el Administrador puede modificar maquinaria.")
            return
        """Orquesta la modificación o eliminación de la maquinaria"""
        dialogo = DialogoMaquinaria(parent=self, datos=datos)
        resultado = dialogo.exec()
        
        # Extraemos el ID una sola vez (usando el alias 'id' que pusimos en el SQL)
        id_maquina = datos.get('id')

        if resultado == QDialog.Accepted:
            # CASO: MODIFICAR
            nuevos_datos = dialogo.obtener_datos()
            if self.controlador_flota.modificar_unidad(id_maquina, nuevos_datos):
                print(f"Éxito: Unidad {id_maquina} actualizada.")
                
        elif resultado == 10: 
            # CASO: ELIMINAR (Código 10 enviado desde el diálogo)
            if self.controlador_flota.borrar_unidad(id_maquina):
                print(f"Éxito: Unidad {id_maquina} eliminada.")           
                
    def abrir_nuevo_plan(self):
        if self.rol_actual != "Administrador":
            QMessageBox.warning(self, "Acceso restringido", "Solo el Administrador puede crear planes.")
            return
        """Lógica para el botón '+ Nuevo Plan'"""
        from views.dialogo_nuevo_plan import DialogoNuevoPlan
        
        # 1. Obtenemos las máquinas para el ComboBox
        maquinas = self.controlador_planes.cargar_lista_maquinaria()
        
        dialogo = DialogoNuevoPlan(maquinas, self)
        if dialogo.exec():
            datos = dialogo.obtener_datos()
            
            # 2. Mandamos los datos al controlador para insertar en BD
            if self.controlador_planes.crear_nuevo_plan(datos):
                QMessageBox.information(self, "Éxito", "El plan se ha registrado correctamente.")
                # El controlador ya refresca la vista automáticamente
                
    # views/main_window.py

    def abrir_nueva_incidencia(self):
        from views.dialogo_incidencia import DialogoIncidencia
        
        # Obtenemos la lista de máquinas
        maquinas = self.controlador_planes.cargar_lista_maquinaria()
        
        # Pasamos (lista, self) porque así lo definimos en el __init__ del diálogo
        dialogo = DialogoIncidencia(maquinas, self) 
        if dialogo.exec():
            datos = dialogo.obtener_datos()
            if self.controlador_servicios.crear_incidencia_manual(datos):
                # Refrescar para ver el cambio a NEGRO
                self.controlador_flota.refrescar_dashboard()
                self.controlador_servicios.cargar_ordenes()
    
    def abrir_edicion_plan(self, datos_plan):
        if self.rol_actual != "Administrador":
            QMessageBox.warning(self, "Acceso restringido", "Solo el Administrador puede editar planes.")
            return
        """Se activa desde la TarjetaPlan (Botón Editar)"""
        from views.dialogo_editar_plan import DialogoEditarPlan
        
        maquinas = self.controlador_planes.cargar_lista_maquinaria()
        dialogo = DialogoEditarPlan(datos_plan, maquinas, self)
        
        if dialogo.exec():
            nuevos_datos = dialogo.obtener_datos()
            
            # Llamamos al controlador para el UPDATE (usando el método que hicimos en el DAO)
            if self.controlador_planes.actualizar_plan(nuevos_datos):
                QMessageBox.information(self, "Actualizado", "El plan ha sido modificado.")

    def confirmar_eliminacion_plan(self, id_plan):
        if self.rol_actual != "Administrador":
            QMessageBox.warning(self, "Acceso restringido", "Solo el Administrador puede eliminar planes.")
            return
        respuesta = QMessageBox.question(
            self,
            "Eliminar plan",
            "¿Seguro que deseas eliminar este plan?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes and self.controlador_planes.eliminar_plan(id_plan):
            QMessageBox.information(self, "Eliminado", "El plan fue eliminado.")

    def validar_credencial_admin(self, titulo="Credenciales de administrador"):
        password, ok = QInputDialog.getText(
            self,
            titulo,
            "Ingrese la contraseña del administrador:",
            QLineEdit.Password
        )
        if not ok:
            return False
        if AuthDAO().validar_password_administrador(password):
            return True
        QMessageBox.warning(self, "Acceso denegado", "La contraseña del administrador no es correcta.")
        return False

    def eliminar_unidad_con_credenciales(self, datos):
        if self.rol_actual != "Administrador":
            QMessageBox.warning(self, "Acceso restringido", "Solo el Administrador puede eliminar unidades.")
            return
        if not self.validar_credencial_admin("Eliminar unidad"):
            return
        respuesta = QMessageBox.question(
            self,
            "Eliminar unidad",
            "¿Seguro que deseas eliminar esta unidad?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes and self.controlador_flota.borrar_unidad(datos.get("id")):
            QMessageBox.information(self, "Unidad eliminada", "La unidad fue eliminada correctamente.")

    def autorizar_cierre_orden(self):
        if self.rol_actual == "Administrador":
            return True

        return self.validar_credencial_admin("Autorizacion de Administrador")

    def cerrar_sesion(self):
        from views.login_view import LoginView

        respuesta = QMessageBox.question(
            self,
            "Cerrar sesión",
            "¿Seguro que quieres cerrar tu sesión?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta != QMessageBox.Yes:
            return

        app = QApplication.instance()
        app.setQuitOnLastWindowClosed(False)
        self.hide()

        login = LoginView()
        if login.exec() != QDialog.Accepted:
            app.quit()
            return

        nueva_ventana = MainWindow(usuario=login.usuario_autenticado)
        app.ventana_actual = nueva_ventana
        nueva_ventana.showFullScreen()
        app.setQuitOnLastWindowClosed(True)
        self.close()

    def salir_aplicacion(self):
        respuesta = QMessageBox.question(
            self,
            "Salir",
            "¿Seguro que quieres salir de la aplicación?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            QApplication.instance().quit()

    def exportar_base_datos(self):
        if self.rol_actual != "Administrador":
            QMessageBox.warning(self, "Acceso restringido", "Solo el Administrador puede exportar la base de datos.")
            return
        if not self.validar_credencial_admin("Exportar base de datos"):
            return
        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar Base de Datos",
            "respaldo_mantenimiento_maquinaria.sql",
            "SQL (*.sql)"
        )
        if not ruta:
            return
        if not ruta.lower().endswith(".sql"):
            ruta += ".sql"
        try:
            BackupService.exportar_base_datos(ruta)
            QMessageBox.information(self, "Respaldo generado", f"Base de datos exportada en:\n{ruta}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo exportar la base de datos:\n{e}")

    def eliminar_orden_con_motivo(self, id_orden):
        if self.rol_actual != "Administrador":
            QMessageBox.warning(self, "Acceso restringido", "Solo el Administrador puede eliminar ordenes.")
            return False

        respuesta = QMessageBox.question(
            self,
            "Eliminar orden",
            "¿Seguro que deseas eliminar esta orden de servicio?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta != QMessageBox.Yes:
            return False

        motivo, ok = QInputDialog.getMultiLineText(
            self,
            "Motivo de eliminación",
            "Describe el motivo de eliminación de la orden:"
        )
        motivo = motivo.strip()
        if not ok:
            return False
        if len(motivo) < 10:
            QMessageBox.warning(self, "Motivo requerido", "El motivo debe tener al menos 10 caracteres.")
            return False

        usuario = self.usuario.get("usuario", "desconocido")
        if self.controlador_servicios.eliminar_orden(id_orden, motivo, usuario):
            QMessageBox.information(self, "Orden eliminada", "La orden fue eliminada y el motivo quedó registrado.")
            return True

        QMessageBox.warning(self, "Error", "No se pudo eliminar la orden.")
        return False
                
                
    def al_cambiar_vista(self, index):
        try:
            self.btn_accion_principal.clicked.disconnect()
            self.search_bar.textChanged.disconnect()
        except:
            pass

        self.btn_accion_principal.hide()
        self.btn_registrar_uso.hide()
        self.btn_imprimir.hide()
        self.btn_exportar.hide()
        self.search_bar.hide()
        
        if index == 0: # FLOTA
            self.btn_accion_principal.setText("+ Añadir Unidad")
            self.btn_accion_principal.setVisible(self.rol_actual == "Administrador")
            self.btn_registrar_uso.setVisible(self.rol_actual in ("Administrador", "Encargado"))
            self.search_bar.show()
            self.btn_accion_principal.clicked.connect(self.abrir_registro_maquinaria)
            self.search_bar.textChanged.connect(self.controlador_flota.filtrar_busqueda)
        elif index == 1: # PLANES
            self.btn_accion_principal.setText("+ Nuevo Plan de Mantenimiento")
            self.btn_imprimir.setText("Exportar Plan")
            self.btn_registrar_uso.hide()
            self.btn_accion_principal.setVisible(self.rol_actual == "Administrador")
            self.btn_imprimir.setVisible(self.rol_actual == "Administrador")
            self.search_bar.show()
            self.btn_accion_principal.clicked.connect(self.abrir_nuevo_plan)
            self.search_bar.textChanged.connect(self.controlador_planes.filtrar_busqueda)
        elif index == 2:
            self.btn_accion_principal.setText("+ Registrar incidencia")
            self.btn_registrar_uso.hide()
            self.btn_accion_principal.setVisible(self.rol_actual in ("Administrador", "Encargado"))
            self.btn_exportar.setVisible(self.rol_actual == "Administrador")
            self.search_bar.show()
            self.btn_accion_principal.clicked.connect(self.abrir_nueva_incidencia)
            self.search_bar.textChanged.connect(self.controlador_servicios.filtrar_ordenes)
        elif index == 3:
            self.vista_calendario.refrescar()

    def aplicar_permisos(self):
        es_admin = self.rol_actual == "Administrador"
        self.btn_config.setEnabled(es_admin)
        self.btn_exportar_bd.setVisible(es_admin)
        self.btn_config.setVisible(es_admin)
        self.btn_calendario.setEnabled(True)
        self.btn_service.setEnabled(True)
        if self.content_stack.currentIndex() == 1 and not es_admin:
            self.navegar_a(0)
        else:
            self.al_cambiar_vista(self.content_stack.currentIndex())
