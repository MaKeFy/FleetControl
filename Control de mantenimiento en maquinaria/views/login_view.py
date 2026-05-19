from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)

from database.auth_dao import AuthDAO


class LoginView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.usuario_autenticado = None
        self.auth = AuthDAO()
        self.setWindowTitle("Inicio de sesion")
        self.setFixedWidth(360)
        self.setStyleSheet("""
            QDialog { background-color: #f8fafc; }
            QLabel { color: #1e293b; font-weight: bold; }
            QLineEdit {
                padding: 10px;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                background-color: white;
                color: #0f172a;
            }
            QPushButton {
                background-color: #10b981;
                color: white;
                padding: 11px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #059669; }
        """)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(12)

        titulo = QLabel("FleetControl")
        titulo.setStyleSheet("font-size: 24px; color: #10b981;")
        layout.addWidget(titulo)

        layout.addWidget(QLabel("Usuario:"))
        self.txt_usuario = QLineEdit()
        self.txt_usuario.setPlaceholderText("admin")
        layout.addWidget(self.txt_usuario)

        layout.addWidget(QLabel("Contrasena:"))
        self.txt_password = QLineEdit()
        self.txt_password.setPlaceholderText("admin123")
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_password.returnPressed.connect(self.intentar_login)
        layout.addWidget(self.txt_password)

        self.btn_login = QPushButton("Ingresar")
        self.btn_login.clicked.connect(self.intentar_login)
        layout.addWidget(self.btn_login)

        ayuda = QLabel("Usuario inicial: admin / admin123")
        ayuda.setStyleSheet("color: #64748b; font-weight: normal; font-size: 11px;")
        layout.addWidget(ayuda)

    def intentar_login(self):
        usuario = self.txt_usuario.text().strip()
        password = self.txt_password.text()
        if not usuario or not password:
            QMessageBox.warning(self, "Datos requeridos", "Ingrese usuario y contrasena.")
            return

        autenticado = self.auth.autenticar(usuario, password)
        if not autenticado:
            QMessageBox.warning(self, "Acceso denegado", "Credenciales incorrectas.")
            return

        self.usuario_autenticado = autenticado
        self.accept()
