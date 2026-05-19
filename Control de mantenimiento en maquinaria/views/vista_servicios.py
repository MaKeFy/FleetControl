from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QPushButton, QLabel, QScrollArea, QComboBox, QFrame)
from PySide6.QtCore import Qt

class VistaServicios(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.controlador = None
        self.setup_ui()

    def setup_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(25, 25, 25, 25)

        # Contenedor para que el fondo no se pierda
        self.setStyleSheet("background-color: #f8fafc;") 

        header = QHBoxLayout()
        titulo = QLabel("Gestión de Servicio y Mantenimiento")
        # Forzamos color blanco/claro para que no sea invisible
        titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #1e293b;")
        
        self.combo_filtro = QComboBox()
        self.combo_filtro.addItems(["Todos los Estados", "Abierta", "En Proceso", "Cerrada"])
        self.combo_filtro.currentTextChanged.connect(self.solicitar_filtro)
        # Estilo explícito para el Filtro
        self.combo_filtro.setStyleSheet("""
            QComboBox {
                background-color: #ffffff;
                color: #1e293b;
                border: 1px solid #cbd5e1;
                padding: 8px;
                border-radius: 6px;
                min-width: 150px;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                color: #1e293b;
                selection-background-color: #dbeafe;
            }
        """)
        
        lbl_filtro = QLabel("Filtrar por estado:")
        lbl_filtro.setStyleSheet("color: #475569; font-weight: bold;")

        header.addWidget(titulo)
        header.addStretch()
        header.addWidget(lbl_filtro)
        header.addWidget(self.combo_filtro)
        layout_principal.addLayout(header)

        # Área de Scroll para las tarjetas
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background: transparent;")
        
        self.contenedor_tarjetas = QWidget()
        self.grid = QGridLayout(self.contenedor_tarjetas)
        self.grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.grid.setSpacing(20)
        
        self.scroll.setWidget(self.contenedor_tarjetas)
        layout_principal.addWidget(self.scroll)
        
    def solicitar_filtro(self, texto):
        """Envía la solicitud de filtrado al controlador."""
        if self.controlador:
            self.controlador.cargar_ordenes(texto)

    def actualizar_grid(self, ordenes):
        # Limpiar grid previo
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Dibujar nuevas tarjetas
        for i, orden in enumerate(ordenes):
            tarjeta = TarjetaServicio(orden)
            self.grid.addWidget(tarjeta, i // 3, i % 3)

    def filtrar_por_estado(self, texto):
        estado = None if "Todos" in texto else texto
        if self.controlador:
            self.controlador.cargar_ordenes(estado)

class TarjetaServicio(QFrame):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.setFixedSize(300, 220)
        self.setup_ui()

    def setup_ui(self):
        tipo = self.data.get('tipo', 'preventivo')
        color_borde = "#ef4444" if tipo == 'correctivo' else "#3b82f6"
        
        self.setStyleSheet(f"""
            TarjetaServicio {{
                background-color: #ffffff;
                border-radius: 10px;
                border: 1px solid #e2e8f0;
                border-top: 5px solid {color_borde};
            }}
            TarjetaServicio:hover {{ background-color: #f8fafc; }}
            QLabel {{ color: #1e293b; }}
        """)
        
        layout = QVBoxLayout(self)
        
        lbl_folio = QLabel(f"FOLIO: {self.data.get('id_orden')}")
        lbl_folio.setStyleSheet("font-weight: bold; color: #64748b;")
        
        lbl_unidad = QLabel(f"{self.data.get('marca')} {self.data.get('modelo')}")
        lbl_unidad.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        lbl_desc = QLabel(self.data.get('descripcion_falla', 'Sin descripción'))
        lbl_desc.setWordWrap(True)
        lbl_desc.setStyleSheet("color: #475569; font-size: 11px;")

        lbl_estado = QLabel(f"ESTADO: {self.data.get('estado')}")
        lbl_estado.setStyleSheet("color: #2563eb; font-weight: bold;")

        layout.addWidget(lbl_folio)
        layout.addWidget(lbl_unidad)
        layout.addWidget(lbl_desc)
        layout.addStretch()
        layout.addWidget(lbl_estado)

        if self.data.get('estado') != 'Cerrada':
            btn_gestionar = QPushButton("GESTIONAR ORDEN")
            btn_gestionar.setStyleSheet("""
                QPushButton {
                    background-color: #10b981;
                    color: white;
                    padding: 8px;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover { background-color: #059669; }
            """)
            btn_gestionar.clicked.connect(self.abrir_gestion)
            layout.addWidget(btn_gestionar)
        else:
            btn_detalle = QPushButton("VER DETALLE")
            btn_detalle.setStyleSheet("""
                QPushButton {
                    background-color: #2563eb;
                    color: white;
                    padding: 8px;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover { background-color: #1d4ed8; }
            """)
            btn_detalle.clicked.connect(self.abrir_detalle)
            layout.addWidget(btn_detalle)

    def abrir_gestion(self):
        # Aquí conectaremos con el diálogo de cierre que ya diseñamos
        from views.dialogo_cierre_orden import DialogoCierreOrden
        from PySide6.QtWidgets import QMessageBox
        ventana_principal = self.window()
        if not ventana_principal.autorizar_cierre_orden():
            return
        
        dialogo = DialogoCierreOrden(
            ventana_principal,
            self.data,
            puede_eliminar=getattr(ventana_principal, "rol_actual", None) == "Administrador"
        )
        if dialogo.exec():
            if dialogo.accion == "eliminar":
                ventana_principal.eliminar_orden_con_motivo(self.data["id_orden"])
                return

            datos_cierre = dialogo.get_datos_cierre()
            # Llamamos al controlador de servicios a través de la ventana principal
            exito = ventana_principal.controlador_servicios.procesar_cierre_orden(
                self.data['id_orden'],
                self.data['id_maquina'],
                self.data.get('id_plan_preventivo'),
                datos_cierre
            )
            if exito:
                QMessageBox.information(ventana_principal, "Orden cerrada", "La orden fue cerrada correctamente.")
                # Refrescamos la flota para que el color negro desaparezca
                ventana_principal.controlador_flota.refrescar_dashboard()
            else:
                QMessageBox.warning(ventana_principal, "Error", "No se pudo cerrar la orden.")

    def abrir_detalle(self):
        from views.dialogo_detalle_orden import DialogoDetalleOrden

        ventana_principal = self.window()
        orden = ventana_principal.controlador_servicios.dao.obtener_detalle_orden_servicio(self.data["id_orden"])
        repuestos = ventana_principal.controlador_servicios.dao.obtener_repuestos_orden(self.data["id_orden"])
        dialogo = DialogoDetalleOrden(
            ventana_principal,
            orden,
            repuestos,
            puede_eliminar=getattr(ventana_principal, "rol_actual", None) == "Administrador"
        )
        if dialogo.exec() and dialogo.accion == "eliminar":
            ventana_principal.eliminar_orden_con_motivo(self.data["id_orden"])
