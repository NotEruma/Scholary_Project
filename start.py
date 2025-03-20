import sys
from PyQt5.QtWidgets import QApplication
from loginWin import LoginC  # Asegúrate de que 'login.py' es el archivo donde está la clase LoginC

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Inicializar la aplicación PyQt5
    ventana = LoginC()  # Instanciar el login
    ventana.show()  # Mostrar la ventana de login
    sys.exit(app.exec_())