from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QTextEdit


class DialogoDetalleOrden(QDialog):
    def __init__(self, parent=None, orden=None, repuestos=None, puede_eliminar=False):
        super().__init__(parent)
        self.orden = orden or {}
        self.repuestos = repuestos or []
        self.accion = "cerrar"
        self.puede_eliminar = puede_eliminar
        self.setWindowTitle(f"Detalle de Orden #{self.orden.get('id_orden', '')}")
        self.setMinimumWidth(620)
        self.setStyleSheet("""
            QDialog { background-color: #ffffff; }
            QLabel { color: #1e293b; }
            QTableWidget {
                background-color: #ffffff;
                color: #1e293b;
                border: 1px solid #e2e8f0;
                gridline-color: #e2e8f0;
            }
            QTextEdit {
                background-color: #f8fafc;
                color: #1e293b;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        titulo = QLabel(f"{self.orden.get('marca', '')} {self.orden.get('modelo', '')}")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #0f172a;")
        layout.addWidget(titulo)

        resumen = QHBoxLayout()
        resumen.addWidget(self._dato("Folio", self.orden.get("folio") or self.orden.get("id_orden", "S/F")))
        resumen.addWidget(self._dato("Tipo", self.orden.get("tipo", "")))
        resumen.addWidget(self._dato("Estado", self.orden.get("estado", "")))
        layout.addLayout(resumen)

        resumen2 = QHBoxLayout()
        resumen2.addWidget(self._dato("Horómetro", f"{self.orden.get('horas_motor_total', 0)} h"))
        resumen2.addWidget(self._dato("Costo total", f"${float(self.orden.get('costo_total') or 0):,.2f}"))
        resumen2.addWidget(self._dato("Fecha cierre", self.orden.get("fecha_cierre") or "Pendiente"))
        layout.addLayout(resumen2)

        layout.addWidget(QLabel("Refacciones utilizadas:"))
        tabla = QTableWidget(len(self.repuestos), 2)
        tabla.setHorizontalHeaderLabels(["Refacción", "Costo"])
        for fila, repuesto in enumerate(self.repuestos):
            tabla.setItem(fila, 0, QTableWidgetItem(str(repuesto.get("nombre", ""))))
            tabla.setItem(fila, 1, QTableWidgetItem(f"${float(repuesto.get('costo') or 0):,.2f}"))
        tabla.resizeColumnsToContents()
        tabla.setMinimumHeight(140)
        layout.addWidget(tabla)

        layout.addWidget(QLabel("Comentarios / descripción:"))
        comentarios = QTextEdit()
        comentarios.setReadOnly(True)
        comentarios.setPlainText(str(self.orden.get("descripcion_falla") or "Sin comentarios"))
        layout.addWidget(comentarios)

        acciones = QHBoxLayout()
        if self.puede_eliminar:
            btn_eliminar = QPushButton("Eliminar Orden")
            btn_eliminar.setStyleSheet("""
                QPushButton {
                    background-color: #ef4444;
                    color: white;
                    padding: 10px 18px;
                    border-radius: 6px;
                    font-weight: bold;
                }
            """)
            btn_eliminar.clicked.connect(self.solicitar_eliminacion)
            acciones.addWidget(btn_eliminar)

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                padding: 10px 18px;
                border-radius: 6px;
                font-weight: bold;
            }
        """)
        btn_cerrar.clicked.connect(self.accept)
        acciones.addWidget(btn_cerrar)
        layout.addLayout(acciones)

    def solicitar_eliminacion(self):
        self.accion = "eliminar"
        self.accept()

    def _dato(self, etiqueta, valor):
        label = QLabel(f"<b>{etiqueta}</b><br>{valor}")
        label.setStyleSheet("""
            QLabel {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        return label
