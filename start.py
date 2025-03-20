import sys
from PyQt5.QtWidgets import QApplication
from loginWin import LoginC

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = LoginC()
    ventana.show()
    sys.exit(app.exec_())