from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtCore import Qt

class DialogoDetalleMaquinaria(QDialog):
    def __init__(self, parent=None, datos=None):
        super().__init__(parent)
        self.setWindowTitle("Detalle de Maquinaria")
        self.setMinimumWidth(450)
        self.datos = datos
        
        # Fondo oscuro refinado para el diálogo
        self.setStyleSheet("background-color: #0f172a; color: #f8fafc;")
        
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(25, 25, 25, 25)
        layout_principal.setSpacing(20)

        # 1. Cabecera con Título y Subtítulo
        header_layout = QVBoxLayout()
        titulo = QLabel(f"{datos.get('marca', 'S/M')} {datos.get('modelo', 'S/M')}")
        titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #38bdf8;")
        
        subtitulo = QLabel(f"ID Unidad: {datos.get('id', 'N/A')}")
        subtitulo.setStyleSheet("font-size: 12px; color: #94a3b8; font-weight: bold;")
        
        header_layout.addWidget(titulo)
        header_layout.addWidget(subtitulo)
        layout_principal.addLayout(header_layout)

        # 2. Tarjeta de Datos Técnicos
        card_datos = QFrame()
        card_datos.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        card_layout = QVBoxLayout(card_datos)
        card_layout.setSpacing(12)

        def crear_fila_dato(label, valor, color_valor="#f1f5f9", bold=False):
            fila = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setStyleSheet("color: #94a3b8; font-weight: bold; font-size: 13px;")
            val = QLabel(str(valor))
            font_weight = "bold" if bold else "normal"
            val.setStyleSheet(f"color: {color_valor}; font-size: 14px; font-weight: {font_weight};")
            fila.addWidget(lbl)
            fila.addStretch()
            fila.addWidget(val)
            return fila

        # RF05: Cálculo automático del próximo servicio
        ultimo_servicio = datos.get('ultimo_mantenimiento_horas', 0)
        intervalo = datos.get('intervalo_horas', 0)
        proximo_servicio = ultimo_servicio + intervalo

        # Agregamos los datos a la tarjeta
        card_layout.addLayout(crear_fila_dato("Número de Serie:", datos.get('vin', 'N/A')))
        card_layout.addLayout(crear_fila_dato("Horas de Uso:", f"{datos.get('horas_motor_total', 0)} h"))
        card_layout.addLayout(crear_fila_dato("Último Servicio:", f"{ultimo_servicio} h"))
        
        # Fila resaltada para el RF05
        card_layout.addLayout(crear_fila_dato(
            "PRÓXIMO SERVICIO A LAS:", 
            f"{proximo_servicio} h", 
            color_valor="#38bdf8", 
            bold=True
        ))
        
        layout_principal.addWidget(card_datos)

        # 3. Indicador de Estado (Estilo Badge)
        estado = datos.get('estado_color', 'Blanco')
        color_estado = {"Verde": "#10b981", "Amarillo": "#f59e0b", "Rojo": "#ef4444"}.get(estado, "#94a3b8")
        
        lbl_estado_badge = QLabel(estado.upper())
        lbl_estado_badge.setAlignment(Qt.AlignCenter)
        lbl_estado_badge.setFixedWidth(120)
        lbl_estado_badge.setStyleSheet(f"""
            background-color: {color_estado}20; 
            color: {color_estado}; 
            border: 1px solid {color_estado};
            border-radius: 15px;
            padding: 5px;
            font-weight: bold;
            font-size: 11px;
        """)
        
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("ESTADO DE MANTENIMIENTO:"))
        status_layout.addStretch()
        status_layout.addWidget(lbl_estado_badge)
        layout_principal.addLayout(status_layout)

        layout_principal.addStretch()

        # 4. Botonera
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(15)
        
        self.btn_editar = QPushButton("EDITAR DATOS")
        self.btn_editar.setStyleSheet("""
            QPushButton {
                background-color: #2563eb; color: white; border: none; 
                padding: 12px; border-radius: 6px; font-weight: bold;
            }
            QPushButton:hover { background-color: #1d4ed8; }
        """)
        self.btn_editar.clicked.connect(self.solicitar_edicion)

        self.btn_eliminar = QPushButton("ELIMINAR UNIDAD")
        self.btn_eliminar.setStyleSheet("""
            QPushButton {
                background-color: #ef4444; color: white; border: none;
                padding: 12px; border-radius: 6px; font-weight: bold;
            }
            QPushButton:hover { background-color: #dc2626; }
        """)
        self.btn_eliminar.clicked.connect(self.solicitar_eliminacion)
        if not parent or getattr(parent, "rol_actual", None) != "Administrador":
            self.btn_eliminar.hide()
        
        self.btn_cerrar = QPushButton("CERRAR")
        self.btn_cerrar.setStyleSheet("""
            QPushButton {
                background-color: #334155; color: white; border: none; 
                padding: 12px; border-radius: 6px; font-weight: bold;
            }
            QPushButton:hover { background-color: #475569; }
        """)
        self.btn_cerrar.clicked.connect(self.reject)

        botones_layout.addWidget(self.btn_editar)
        botones_layout.addWidget(self.btn_eliminar)
        botones_layout.addWidget(self.btn_cerrar)
        layout_principal.addLayout(botones_layout)

    def solicitar_edicion(self):
        self.done(20)

    def solicitar_eliminacion(self):
        self.done(30)
