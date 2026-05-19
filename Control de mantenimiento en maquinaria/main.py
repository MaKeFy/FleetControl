import sys
from PySide6.QtWidgets import QApplication
from views.main_window import MainWindow
from views.login_view import LoginView

def main():
    app = QApplication(sys.argv)
    login = LoginView()
    if login.exec() != LoginView.Accepted:
        sys.exit(0)

    window = MainWindow(usuario=login.usuario_autenticado)
    
    # Lanzar en pantalla completa (Maximizada con barra de tareas visible)
    window.showFullScreen() 
    
    # Si prefieres pantalla completa total (sin barra de tareas), usa:
    # window.showFullScreen()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
