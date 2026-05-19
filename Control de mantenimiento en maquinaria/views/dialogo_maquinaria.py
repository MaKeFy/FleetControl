from PySide6.QtWidgets import (QDialog, QDialogButtonBox, QVBoxLayout, QLineEdit, QPushButton, 
                             QLabel, QComboBox, QMessageBox)
from PySide6.QtGui import QDoubleValidator

class DialogoMaquinaria(QDialog):
    def __init__(self, parent=None, datos=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar Maquinaria")
        self.setMinimumWidth(350)
        
        # 1. Definimos el layout principal del diálogo
        self.layout_principal = QVBoxLayout(self)
        
        # 2. Creamos los campos (Asegúrate de que estos nombres coincidan con obtener_datos)
        self.marca = QLineEdit()
        self.marca.setPlaceholderText("Marca (ej. John Deere)")
        
        self.modelo = QLineEdit()
        self.modelo.setPlaceholderText("Modelo (ej. 2026)")
        
        self.vin = QLineEdit()
        self.vin.setPlaceholderText("Número de Serie / VIN")
        self.vin.setMaxLength(17)
        
        self.horas = QLineEdit()
        self.horas.setPlaceholderText("Horas de uso actual")

        # 3. Añadimos los campos al layout
        self.layout_principal.addWidget(QLabel("Marca:"))
        self.layout_principal.addWidget(self.marca)
        self.layout_principal.addWidget(QLabel("Modelo:"))
        self.layout_principal.addWidget(self.modelo)
        self.layout_principal.addWidget(QLabel("Serie/VIN:"))
        self.layout_principal.addWidget(self.vin)
        self.layout_principal.addWidget(QLabel("Horas totales:"))
        self.layout_principal.addWidget(self.horas)

        # 4. Si es EDICIÓN, rellenamos y añadimos el botón de eliminar
        if datos:
            self.setWindowTitle("Editar Maquinaria")
            self.marca.setText(str(datos.get('marca', '')))
            self.modelo.setText(str(datos.get('modelo', '')))
            self.vin.setText(str(datos.get('vin', '')))
            self.horas.setText(str(datos.get('horas_motor_total', 0)))

            self.btn_eliminar = QPushButton("Eliminar Unidad")
            self.btn_eliminar.setStyleSheet("""
                background-color: #ef4444; color: white; padding: 10px; 
                border-radius: 4px; font-weight: bold; margin-top: 15px;
            """)
            self.btn_eliminar.clicked.connect(self.confirmar_eliminacion)
            self.layout_principal.addWidget(self.btn_eliminar)

        # 5. Botones estándar de Guardar/Cancelar
        self.botones = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.botones.accepted.connect(self.accept)
        self.botones.rejected.connect(self.reject)
        self.layout_principal.addWidget(self.botones)

    def obtener_datos(self):
        """Retorna un diccionario con la información de los QLineEdit"""
        return {
            'marca': self.marca.text(),
            'modelo': self.modelo.text(),
            'vin': self.vin.text(),
            'horas': self.horas.text()
        }

    def confirmar_eliminacion(self):
        from PySide6.QtWidgets import QMessageBox
        res = QMessageBox.question(
            self, "Confirmar", "¿Seguro que deseas eliminar esta unidad?",
            QMessageBox.Yes | QMessageBox.No
        )
        if res == QMessageBox.Yes:
            self.done(10) # Código 10 para eliminar
