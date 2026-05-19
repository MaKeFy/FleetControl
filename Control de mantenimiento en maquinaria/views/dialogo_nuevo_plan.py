from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QLabel, QComboBox, QScrollArea, QWidget, QMessageBox, QSpinBox)
from PySide6.QtCore import Qt

class DialogoNuevoPlan(QDialog):
    def __init__(self, lista_maquinaria, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuevo Plan de Mantenimiento")
        self.setFixedWidth(500)
        self.setMinimumHeight(500)
        
        # FORZAMOS ESTILO GLOBAL DEL DIÁLOGO
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
            }
            QLabel {
                color: #1e293b;         /* Azul muy oscuro, casi negro */
                font-size: 13px;
                font-weight: bold;
                margin-top: 5px;
            }
            QLineEdit, QComboBox {
                border: 1px solid #94a3b8;
                border-radius: 5px;
                padding: 8px;
                background-color: #ffffff;
                color: #0f172a;
            }
            QLineEdit:focus {
                border: 2px solid #2563eb;
            }
            QScrollArea {
                border: 1px solid #e2e8f0;
                background-color: #f8fafc;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #1e293b;
                selection-background-color: #2563eb;
                selection-color: white;
                border: 1px solid #cbd5e1;
                outline: none;
            }
            
            /* Asegura que el texto del item seleccionado sea visible */
            QComboBox {
                color: #1e293b;
                padding-left: 10px;
            }
        """)
        
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(25, 25, 25, 25)
        self.layout_principal.setSpacing(10)
        
        
        # 1. Información General
        # Ahora los QLabel deberían ser visibles por el estilo definido arriba
        self.layout_principal.addWidget(QLabel("Nombre del Plan:"))
        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText("Ej: Mantenimiento Preventivo 250h")
        self.layout_principal.addWidget(self.txt_nombre)
        
        self.layout_principal.addWidget(QLabel("Intervalo de Mantenimiento (Horas):"))
        self.spin_horas = QSpinBox()
        self.spin_horas.setRange(1, 10000)  # De 1 a 10,000 horas
        self.spin_horas.setSuffix(" hrs")
        self.spin_horas.setValue(250)       # Valor por defecto común
        self.spin_horas.setStyleSheet("""
            QSpinBox {
                border: 1px solid #94a3b8;
                border-radius: 5px;
                padding: 8px;
                background-color: #ffffff;
                color: #0f172a;
            }
        """)
        self.layout_principal.addWidget(self.spin_horas)

        self.layout_principal.addWidget(QLabel("Asociar a Maquinaria:"))
        self.combo_maquina = QComboBox()
        # Llenamos el combo con el ID y Modelo (lista_maquinaria viene del controlador)
        for maq in lista_maquinaria:
            texto_display = f"ID: {maq['id_maquina']} - {maq['marca']} {maq['modelo']}"
            self.combo_maquina.addItem(texto_display, maq['id_maquina']) # Guardamos el ID como userData
        

        self.layout_principal.addWidget(self.combo_maquina)

        # 2. Área Dinámica de Tareas
        self.layout_principal.addWidget(QLabel("Tareas del Plan:"))
        
        # Scroll area para cuando haya muchas tareas
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { 
                border: 1px solid #e2e8f0; 
                background-color: #f8fafc; 
                border-radius: 5px; 
            }
        """)

        
        self.contenedor_tareas = QWidget()
        self.contenedor_tareas.setStyleSheet("background-color: #f8fafc;")
        self.layout_tareas = QVBoxLayout(self.contenedor_tareas)
        self.layout_tareas.setAlignment(Qt.AlignTop)
        
        scroll.setWidget(self.contenedor_tareas)
        self.layout_principal.addWidget(scroll)

        # Botón para agregar fila de tarea
        self.btn_add_tarea = QPushButton("+ Agregar Tarea")
        self.btn_add_tarea.setStyleSheet("""
            QPushButton { background-color: #f1f5f9; border: 1px dashed #64748b; padding: 8px; color: #475569; font-weight: bold; }
            QPushButton:hover { background-color: #e2e8f0; }
        """)
        self.btn_add_tarea.clicked.connect(self.agregar_fila_tarea)
        self.layout_principal.addWidget(self.btn_add_tarea)

        # 3. Botones de Acción
        layout_acciones = QHBoxLayout()
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.clicked.connect(self.reject)
        
        self.btn_guardar = QPushButton("Crear Plan")
        self.btn_guardar.setStyleSheet("background-color: #10b981; color: white; padding: 10px; font-weight: bold; border-radius: 5px;")
        self.btn_guardar.clicked.connect(self.validar_y_aceptar)
        
        layout_acciones.addWidget(self.btn_cancelar)
        layout_acciones.addWidget(self.btn_guardar)
        self.layout_principal.addLayout(layout_acciones)

        # Lista para rastrear los QLineEdits de tareas
        self.inputs_tareas = []
        # Agregar una tarea por defecto
        self.agregar_fila_tarea()

    def agregar_fila_tarea(self):
        """Crea una nueva fila con un input y un botón de eliminar"""
        fila_widget = QWidget()
        fila_layout = QHBoxLayout(fila_widget)
        fila_layout.setContentsMargins(0, 5, 0, 5)

        nuevo_input = QLineEdit()
        nuevo_input.setPlaceholderText("Descripción de la tarea...")
        nuevo_input.setStyleSheet("border: 1px solid #94a3b8; padding: 6px; color: #1e293b; background: white;")
        
        btn_eliminar = QPushButton("✕")
        btn_eliminar.setFixedWidth(30)
        btn_eliminar.setStyleSheet("color: #ef4444; border: none; font-weight: bold;")
        
        # Lógica para eliminar esta fila específica
        btn_eliminar.clicked.connect(lambda: self.eliminar_fila_tarea(fila_widget, nuevo_input))

        fila_layout.addWidget(nuevo_input)
        fila_layout.addWidget(btn_eliminar)
        
        self.layout_tareas.addWidget(fila_widget)
        self.inputs_tareas.append(nuevo_input)

       
    def eliminar_fila_tarea(self, widget, input_ref):
        if len(self.inputs_tareas) > 1: # Mantener al menos una
            self.inputs_tareas.remove(input_ref)
            widget.deleteLater()

    def validar_y_aceptar(self):
        """Valida que el plan tenga nombre y al menos una tarea con texto"""
        if not self.txt_nombre.text().strip():
            QMessageBox.warning(self, "Error", "El nombre del plan es obligatorio.")
            return
        
        tareas_validas = [i.text().strip() for i in self.inputs_tareas if i.text().strip()]
        if not tareas_validas:
            QMessageBox.warning(self, "Error", "Debe agregar al menos una tarea.")
            return
            
        self.accept()

    def obtener_datos(self):
        return {
            "nombre": self.txt_nombre.text().strip(),
            "intervalo": self.spin_horas.value(), # <--- NUEVO
            "id_maquina": self.combo_maquina.currentData(),
            "tareas": [i.text().strip() for i in self.inputs_tareas if i.text().strip()]
        }