from PySide6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QTextEdit, QPushButton, QLabel

class DialogoIncidencia(QDialog):
    def __init__(self, maquinas, parent=None):
        # ERROR CORREGIDO: super() solo recibe el parent, NO la lista de máquinas
        super().__init__(parent) 
        self.maquinas = maquinas # Guardamos la lista para usarla después
        self.setWindowTitle("Reportar Incidencia / Falla")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel("Seleccionar Maquinaria:"))
        self.combo_maquina = QComboBox()
        # Llenamos el combo con los datos recibidos
        for m in self.maquinas:
            nombre = f"{m.get('marca')} {m.get('modelo')} (VIN: {m.get('vin')})"
            self.combo_maquina.addItem(nombre, m.get('id_maquina'))
        
        layout.addWidget(self.combo_maquina)
        
        layout.addWidget(QLabel("Descripción de la Falla:"))
        self.txt_falla = QTextEdit()
        self.txt_falla.setPlaceholderText("Describa el problema técnico...")
        layout.addWidget(self.txt_falla)
        
        self.btn_guardar = QPushButton("Registrar Reporte")
        self.btn_guardar.clicked.connect(self.accept)
        layout.addWidget(self.btn_guardar)

    def obtener_datos(self):
        return {
            "id_maquina": self.combo_maquina.currentData(),
            "descripcion": self.txt_falla.toPlainText().strip()
        }