from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, 
                             QFrame, QLabel, QPushButton, QGridLayout)
from PySide6.QtCore import Qt

class VistaPlanes(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(20, 20, 20, 20)
        

        # Área de Scroll para los planes
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")
        
        self.contenedor_grid = QWidget()
        self.grid = QGridLayout(self.contenedor_grid)
        self.grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.grid.setSpacing(20)
        
        scroll.setWidget(self.contenedor_grid)
        self.layout_principal.addWidget(scroll)

    def limpiar_grid(self):
        while self.grid.count():
            child = self.grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def agregar_tarjeta_plan(self, datos_plan, posicion):
        tarjeta = TarjetaPlan(datos_plan)
        self.grid.addWidget(tarjeta, posicion[0], posicion[1])

class TarjetaPlan(QFrame):
    
    def __init__(self, data):
        super().__init__()
        self.data = data # id_plan, nombre, id_maquina, modelo_maquina, tareas[]
        self.es_seleccionada = False
        self.setFixedWidth(350)
        self.setMinimumHeight(200)
        self.actualizar_estilo()
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Encabezado: Icono + Título
        header = QHBoxLayout()
        lbl_icon = QLabel("⚙️") # Podrías usar un QIcon real aquí
        lbl_titulo = QLabel(data['nombre'])
        lbl_titulo.setStyleSheet("font-size: 16px; font-weight: bold; color: #1e293b;")
        lbl_maq = QLabel(f"Asociado a: {data['modelo_maquina']}")
        lbl_maq.setWordWrap(True) # Por si la lista de máquinas es larga
        header.addWidget(lbl_icon)
        header.addWidget(lbl_titulo)
        header.addStretch()
        
        # Botones de Acción (Editar/Eliminar)
        btn_edit = QPushButton("✎")
        btn_edit.setToolTip("Editar Plan")
        btn_edit.setStyleSheet("color: #64748b; border: none; font-size: 16px;")
        
        btn_delete = QPushButton("🗑")
        btn_delete.setToolTip("Eliminar Plan")
        btn_delete.setStyleSheet("color: #ef4444; border: none; font-size: 16px;")
        
        header.addWidget(btn_edit)
        header.addWidget(btn_delete)
        layout.addLayout(header)

        # Info Maquinaria Asociada
        lbl_maq = QLabel(f"Asociado a: {data['modelo_maquina']}")
        lbl_maq.setStyleSheet("color: #64748b; font-size: 12px; font-weight: 500;")
        layout.addWidget(lbl_maq)

        # Lista de Tareas (Lectura)
        lbl_tareas_title = QLabel("Tareas del Plan:")
        lbl_tareas_title.setStyleSheet("font-size: 13px; font-weight: bold; color: #475569; margin-top: 5px;")
        layout.addWidget(lbl_tareas_title)

        for tarea in data['tareas']:
            item_tarea = QLabel(f"✓ {tarea}")
            item_tarea.setStyleSheet("color: #475569; font-size: 12px; padding-left: 5px;")
            item_tarea.setWordWrap(True)
            layout.addWidget(item_tarea)
        
        layout.addStretch()

        # Conexiones
        btn_edit.clicked.connect(self.solicitar_edicion)
        btn_delete.clicked.connect(self.solicitar_eliminacion)

    def actualizar_estilo(self):
        borde = "#2563eb" if self.es_seleccionada else "#e2e8f0"
        fondo = "#eff6ff" if self.es_seleccionada else "#ffffff"
        self.setStyleSheet(f"""
            TarjetaPlan {{
                background-color: {fondo};
                border: 2px solid {borde};
                border-radius: 8px;
            }}
            TarjetaPlan:hover {{
                background-color: #f8fafc;
            }}
        """)

    def set_seleccionada(self, estado):
        self.es_seleccionada = estado
        self.actualizar_estilo()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            ventana = self.window()
            if ventana and hasattr(ventana, "seleccionar_plan"):
                ventana.seleccionar_plan(self)
            event.accept()

    def solicitar_edicion(self):
        ventana = self.window()
        if hasattr(ventana, 'abrir_edicion_plan'):
            ventana.abrir_edicion_plan(self.data)

    def solicitar_eliminacion(self):
        ventana = self.window()
        if hasattr(ventana, 'confirmar_eliminacion_plan'):
            ventana.confirmar_eliminacion_plan(self.data['id_plan'])
