from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QTextEdit, QPushButton, QDoubleSpinBox, QScrollArea, QWidget, QMessageBox)
from PySide6.QtCore import Qt

class DialogoCierreOrden(QDialog):
    def __init__(self, parent=None, datos_orden=None, puede_eliminar=False):
        super().__init__(parent)
        self.datos = datos_orden
        self.accion = "cerrar"
        self.motivo = self._obtener_motivo(datos_orden)
        self.setWindowTitle(f"Cierre de Orden: {datos_orden.get('folio', 'S/F')}")
        self.setMinimumWidth(500)
        self.setStyleSheet("background-color: #0f172a; color: #f8fafc;")
        
        self.lista_repuestos_widgets = [] # Para rastrear las filas de repuestos

        layout_principal = QVBoxLayout(self)
        
        # 1. Info General
        unidad = f"{datos_orden.get('marca', '')} {datos_orden.get('modelo', '')}".strip()
        header = QLabel(f"Unidad: {unidad}\nMotivo: {self.motivo}")
        header.setStyleSheet("color: #38bdf8; font-weight: bold; font-size: 16px;")
        layout_principal.addWidget(header)

        # 2. Datos Operativos (Horas)
        layout_principal.addWidget(QLabel("Horómetro final del servicio (h):"))
        self.spn_horas = QDoubleSpinBox()
        self.spn_horas.setRange(0, 1000000)
        self.spn_horas.setValue(datos_orden.get('horas_motor_total', 0))
        self.spn_horas.setStyleSheet("background: #1e293b; padding: 8px; border-radius: 4px;")
        layout_principal.addWidget(self.spn_horas)

        # 3. SECCIÓN DE REPUESTOS (Dinámica)
        layout_principal.addWidget(QLabel("REPUESTOS Y REFACCIONES UTILIZADAS:"))
        
        self.scroll_repuestos = QScrollArea()
        self.scroll_repuestos.setWidgetResizable(True)
        self.scroll_repuestos.setFixedHeight(150)
        self.scroll_repuestos.setStyleSheet("background: #1e293b; border: 1px solid #334155; border-radius: 4px;")
        
        self.container_repuestos = QWidget()
        self.layout_repuestos = QVBoxLayout(self.container_repuestos)
        self.layout_repuestos.setAlignment(Qt.AlignTop)
        self.scroll_repuestos.setWidget(self.container_repuestos)
        layout_principal.addWidget(self.scroll_repuestos)

        btn_add_repuesto = QPushButton("+ Añadir Repuesto")
        btn_add_repuesto.setStyleSheet("background: #334155; color: #38bdf8; font-weight: bold; padding: 5px;")
        btn_add_repuesto.clicked.connect(self.agregar_fila_repuesto)
        layout_principal.addWidget(btn_add_repuesto)

        # 4. Costo Mano de Obra y Total
        layout_mano_obra = QHBoxLayout()
        layout_mano_obra.addWidget(QLabel("Costo Mano de Obra ($):"))
        self.spn_mano_obra = QDoubleSpinBox()
        self.spn_mano_obra.setRange(0, 1000000)
        self.spn_mano_obra.setStyleSheet("background: #1e293b; padding: 5px;")
        layout_mano_obra.addWidget(self.spn_mano_obra)
        layout_principal.addLayout(layout_mano_obra)

        # 5. Observaciones opcionales
        layout_principal.addWidget(QLabel("Observación adicional (Opcional):"))

        self.txt_notas = QTextEdit()
        self.txt_notas.setPlaceholderText("Agregue observaciones adicionales si aplica...")
        self.txt_notas.setStyleSheet("background: #1e293b; border: 1px solid #334155;")
        layout_principal.addWidget(self.txt_notas)

        # Botones de Acción
        btns = QHBoxLayout()
        self.btn_confirmar = QPushButton("CONFIRMAR Y CERRAR")
        self.btn_confirmar.setStyleSheet("background: #10b981; color: white; font-weight: bold; padding: 12px;")
        self.btn_confirmar.clicked.connect(self.validar_y_aceptar)
        btns.addWidget(self.btn_confirmar)

        if puede_eliminar:
            self.btn_eliminar = QPushButton("ELIMINAR ORDEN")
            self.btn_eliminar.setStyleSheet("background: #ef4444; color: white; font-weight: bold; padding: 12px;")
            self.btn_eliminar.clicked.connect(self.solicitar_eliminacion)
            btns.addWidget(self.btn_eliminar)
        
        self.btn_cancelar = QPushButton("CANCELAR")
        self.btn_cancelar.clicked.connect(self.reject)
        btns.addWidget(self.btn_cancelar)
        layout_principal.addLayout(btns)

    def agregar_fila_repuesto(self):
        fila = QHBoxLayout()
        txt_nombre = QLineEdit()
        txt_nombre.setPlaceholderText("Nombre del repuesto")
        txt_nombre.setStyleSheet("background: #0f172a;")
        
        spn_precio = QDoubleSpinBox()
        spn_precio.setRange(0, 100000)
        spn_precio.setPrefix("$")
        spn_precio.setStyleSheet("background: #0f172a;")
        
        btn_del = QPushButton("X")
        btn_del.setFixedWidth(30)
        btn_del.setStyleSheet("background: #ef4444; color: white;")
        
        fila.addWidget(txt_nombre)
        fila.addWidget(spn_precio)
        fila.addWidget(btn_del)
        
        widget_fila = QWidget()
        widget_fila.setLayout(fila)
        self.layout_repuestos.addWidget(widget_fila)
        
        # Guardar referencia para extraer datos luego
        fila_data = {"widget": widget_fila, "nombre": txt_nombre, "precio": spn_precio}
        self.lista_repuestos_widgets.append(fila_data)
        
        btn_del.clicked.connect(lambda: self.eliminar_fila_repuesto(fila_data))

    def eliminar_fila_repuesto(self, fila_data):
        fila_data["widget"].deleteLater()
        self.lista_repuestos_widgets.remove(fila_data)

    def validar_y_aceptar(self):
        self.accion = "cerrar"
        self.accept()

    def solicitar_eliminacion(self):
        self.accion = "eliminar"
        self.accept()

    def get_datos_cierre(self):
        repuestos = []
        total_repuestos = 0
        for r in self.lista_repuestos_widgets:
            nombre = r["nombre"].text().strip()
            precio = r["precio"].value()
            if nombre:
                repuestos.append({"nombre": nombre, "costo": precio})
                total_repuestos += precio
        
        notas = f"Motivo: {self.motivo}"
        observacion = self.txt_notas.toPlainText().strip()
        if observacion:
            notas += f"\nObservación: {observacion}"

        return {
            "horas_cierre": self.spn_horas.value(),
            "costo_total": total_repuestos + self.spn_mano_obra.value(),
            "notas": notas,
            "repuestos": repuestos
        }

    def _obtener_motivo(self, datos_orden):
        if not datos_orden:
            return "incidencia"

        if datos_orden.get("tipo") == "correctivo":
            return "incidencia"

        nombre_plan = datos_orden.get("nombre_plan")
        if nombre_plan:
            return str(nombre_plan)

        descripcion = str(datos_orden.get("descripcion_falla") or "")
        if "plan '" in descripcion:
            return descripcion.split("plan '", 1)[1].split("'", 1)[0]
        return "incidencia"
