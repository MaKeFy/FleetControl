from PySide6.QtWidgets import QWidget, QScrollArea, QGridLayout, QVBoxLayout, QFrame, QLabel
from PySide6.QtCore import Qt

class VistaFlota(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.controlador = None
        self.setStyleSheet("background-color: transparent;") 
        
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20) 
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")
        
        self.contenedor_grid = QWidget()
        self.contenedor_grid.setStyleSheet("background: transparent;")
        
        self.grid = QGridLayout(self.contenedor_grid)
        self.grid.setSpacing(25) 
        self.grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        scroll.setWidget(self.contenedor_grid)
        layout_principal.addWidget(scroll)

    def set_controlador(self, controlador):
        self.controlador = controlador

    def actualizar_grid(self, lista_maquinaria=None):
        """Punto de entrada para refrescar las tarjetas en pantalla"""
        # Validación de seguridad: si self no es una instancia, esto fallará antes de romper el app
        if not isinstance(self, VistaFlota):
            print("ERROR CRÍTICO: actualizar_grid llamado sin instancia de objeto.")
            return

        # Normalizar datos
        datos = lista_maquinaria if lista_maquinaria is not None else []
        
        self.limpiar_grid()
        
        for i, m in enumerate(datos):
            if isinstance(m, dict):
                tarjeta = TarjetaMaquinaria(m, parent_vista=self)
                fila, columna = i // 3, i % 3
                self.grid.addWidget(tarjeta, fila, columna)

    def limpiar_grid(self):
        """Elimina físicamente todos los widgets del layout actual"""
        while self.grid.count():
            child = self.grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

class TarjetaMaquinaria(QFrame):
    def __init__(self, data, parent_vista=None):
        super().__init__()
        self.data = data
        self.parent_vista = parent_vista
        self.es_seleccionada = False 
        self.setFixedSize(280, 160)
        
        self.actualizar_estilo()
        layout = QVBoxLayout(self)
        
        id_display = data.get('id_maquina') or data.get('id', 'N/A')
        lbl_id = QLabel(f"ID: {id_display}")
        lbl_id.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold;")
        
        lbl_modelo = QLabel(f"{data.get('marca', '')} {data.get('modelo', '')}")
        lbl_modelo.setStyleSheet("font-size: 16px; font-weight: bold; color: #1e293b;")
        
        lbl_vin = QLabel(f"Serie: {data.get('serie') or data.get('vin', 'S/N')}")
        lbl_vin.setStyleSheet("color: #475569; font-size: 12px;")
        
        horas = data.get('horas_motor_total') or data.get('horas', 0)
        lbl_horas = QLabel(f"Uso: {horas} h")
        lbl_horas.setStyleSheet("color: #1e293b; font-size: 13px; font-weight: bold; margin-top: 5px;")

        estado_txt = str(data.get('estado_color', 'Blanco')).upper()
        lbl_estado = QLabel(estado_txt)
        
        colores_map = {"Verde": "#10b981", "Amarillo": "#f59e0b", "Rojo": "#ef4444", "Blanco": "#64748b"}
        color_texto = colores_map.get(data.get('estado_color', 'Blanco'), "#64748b")
        lbl_estado.setStyleSheet(f"color: {color_texto}; font-weight: bold; font-size: 12px; margin-top: 5px;")

        layout.addWidget(lbl_id)
        layout.addWidget(lbl_modelo)
        layout.addWidget(lbl_vin)
        layout.addWidget(lbl_horas)
        layout.addStretch()
        layout.addWidget(lbl_estado)

    def actualizar_estilo(self):
        colores = {"Verde": "#10b981", "Amarillo": "#f59e0b", "Rojo": "#ef4444", "Blanco": "#e2e8f0", "Negro":"#000000"}
        estado = self.data.get('estado_color', 'Blanco')
        color_borde = colores.get(estado, "#e2e8f0")
        
        borde_seleccion = "2px solid #2563eb" if self.es_seleccionada else "none"
        fondo = "#eff6ff" if self.es_seleccionada else "white"

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {fondo};
                border-radius: 12px;
                border-left: 10px solid {color_borde};
                border-top: {borde_seleccion};
                border-right: {borde_seleccion};
                border-bottom: {borde_seleccion};
            }}
            QFrame:hover {{ background-color: #f1f5f9; }}
        """)
        
    def set_seleccionada(self, estado):
        self.es_seleccionada = estado
        self.actualizar_estilo()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            ventana = self.window()
            if ventana and hasattr(ventana, 'seleccionar_maquinaria'):
                ventana.seleccionar_maquinaria(self)
            event.accept()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            ventana = self.window()
            if ventana and hasattr(ventana, 'abrir_detalle_maquinaria'):
                ventana.abrir_detalle_maquinaria(self.data)
            event.accept()