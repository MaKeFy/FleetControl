from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton


class DialogoEventosDia(QDialog):
    def __init__(self, fecha, eventos, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Eventos del {fecha}")
        self.setMinimumWidth(560)
        self.setStyleSheet("""
            QDialog { background-color: #ffffff; }
            QLabel { color: #1e293b; }
            QListWidget {
                background-color: #f8fafc;
                color: #1e293b;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton {
                background-color: #10b981;
                color: white;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(12)

        titulo = QLabel(f"Eventos del {fecha}")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(titulo)

        lista = QListWidget()
        if eventos:
            for evento in eventos:
                fecha_evento = evento.get("fecha_evento")
                hora = fecha_evento.strftime("%H:%M") if hasattr(fecha_evento, "strftime") else str(fecha_evento)
                texto = f"{hora}  |  {evento.get('tipo')}\n{evento.get('descripcion')}"
                item = QListWidgetItem(texto)
                item.setToolTip(texto)
                lista.addItem(item)
        else:
            lista.addItem("Sin eventos registrados para este día.")
        layout.addWidget(lista)

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.accept)
        layout.addWidget(btn_cerrar)
