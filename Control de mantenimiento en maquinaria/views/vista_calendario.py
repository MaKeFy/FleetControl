import calendar
from datetime import date

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton

from database.calendario_dao import CalendarioDAO
from views.dialogo_eventos_dia import DialogoEventosDia


class VistaCalendario(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        hoy = date.today()
        self.anio = hoy.year
        self.mes = hoy.month
        self.dao = CalendarioDAO()
        self.botones_dia = []
        self._setup_ui()
        self.refrescar()

    def _setup_ui(self):
        self.setStyleSheet("background-color: #f8fafc;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(18)

        header = QHBoxLayout()
        self.btn_anterior = QPushButton("<")
        self.btn_siguiente = QPushButton(">")
        self.lbl_titulo = QLabel()
        self.lbl_mes = QLabel()
        titulo_layout = QVBoxLayout()
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        self.lbl_titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #1e293b;")
        self.lbl_mes.setAlignment(Qt.AlignCenter)
        self.lbl_mes.setStyleSheet("font-size: 14px; font-weight: bold; color: #64748b;")
        titulo_layout.addWidget(self.lbl_titulo)
        titulo_layout.addWidget(self.lbl_mes)

        for btn in (self.btn_anterior, self.btn_siguiente):
            btn.setFixedWidth(42)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #ffffff;
                    color: #1e293b;
                    border: 1px solid #cbd5e1;
                    border-radius: 6px;
                    padding: 8px;
                    font-weight: bold;
                }
                QPushButton:hover { background-color: #f1f5f9; }
            """)

        self.btn_anterior.clicked.connect(self.mes_anterior)
        self.btn_siguiente.clicked.connect(self.mes_siguiente)

        header.addWidget(self.btn_anterior)
        header.addLayout(titulo_layout, 1)
        header.addWidget(self.btn_siguiente)
        layout.addLayout(header)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        layout.addLayout(self.grid)
        layout.addStretch()

    def refrescar(self):
        self._limpiar_grid()
        nombres_meses = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]
        self.lbl_titulo.setText(f"Calendario {self.anio}")
        self.lbl_mes.setText(nombres_meses[self.mes - 1].capitalize())

        dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        for col, nombre in enumerate(dias_semana):
            lbl = QLabel(nombre)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("color: #64748b; font-weight: bold;")
            self.grid.addWidget(lbl, 0, col)

        resumen = self.dao.obtener_resumen_mes(self.anio, self.mes)
        calendario = calendar.Calendar(firstweekday=0).monthdatescalendar(self.anio, self.mes)
        hoy = date.today()

        for fila, semana in enumerate(calendario, start=1):
            for col, dia in enumerate(semana):
                total_eventos = resumen.get(dia.day, 0) if dia.month == self.mes else 0
                texto = str(dia.day)
                if total_eventos:
                    texto += f"\n● {total_eventos}"

                btn = QPushButton(texto)
                btn.setFixedSize(118, 82)
                btn.setEnabled(dia.month == self.mes)
                btn.clicked.connect(lambda _, d=dia: self.abrir_dia(d))
                btn.setStyleSheet(self._estilo_dia(dia, total_eventos, hoy))
                self.grid.addWidget(btn, fila, col)
                self.botones_dia.append(btn)

    def abrir_dia(self, dia):
        eventos = self.dao.obtener_eventos_dia(dia)
        DialogoEventosDia(dia, eventos, self).exec()

    def mes_anterior(self):
        self.mes -= 1
        if self.mes == 0:
            self.mes = 12
            self.anio -= 1
        self.refrescar()

    def mes_siguiente(self):
        self.mes += 1
        if self.mes == 13:
            self.mes = 1
            self.anio += 1
        self.refrescar()

    def _limpiar_grid(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.botones_dia = []

    def _estilo_dia(self, dia, total_eventos, hoy):
        if dia.month != self.mes:
            return """
                QPushButton {
                    background-color: #f1f5f9;
                    color: #cbd5e1;
                    border: 1px solid #e2e8f0;
                    border-radius: 8px;
                }
            """

        borde = "#10b981" if total_eventos else "#e2e8f0"
        fondo = "#ecfdf5" if total_eventos else "#ffffff"
        if dia == hoy:
            borde = "#2563eb"
            fondo = "#eff6ff"

        color_evento = "#059669" if total_eventos else "#1e293b"
        return f"""
            QPushButton {{
                background-color: {fondo};
                color: {color_evento};
                border: 2px solid {borde};
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
                text-align: center;
            }}
            QPushButton:hover {{
                background-color: #f1f5f9;
            }}
        """
