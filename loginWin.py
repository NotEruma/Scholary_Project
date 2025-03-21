
from resources import Recursos
from PyQt5 import QtWidgets, uic
from main import mainwindow
import sesion

class LoginC(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("interfaces/Login01.ui", self)
        self.button_ingresar.clicked.connect(self.iniciarSesion)
        self.error_label.setVisible(False)
        self.main = None

    def clear(self, event):
        self.input_usuario.clear()
        self.input_contrasenna.clear()
        super().showEvent(event)

    def iniciarSesion(self):
        from functions import Administrador, Maestro
        from functions import Usuario
        usuario = self.input_usuario.text()
        contrasenna = self.input_contrasenna.text()
        
        if not usuario and not contrasenna:
            self.ErrMsg("Ingrese el usuario y la contraseña.")
            return
        if not usuario:
            self.ErrMsg("Ingrese un usuario.")
            return
        if not contrasenna:
            self.ErrMsg("Ingrese una contraseña.")
            return

        usuario_obj = Usuario(usuario, contrasenna)
        if usuario_obj.iniciarSesion():
            rol = usuario_obj.obtenerRol()
            if rol == "maestro":
                sesion.maestro_actual=Maestro(usuario, contrasenna)
                sesion.maestro_actual.iniciarSesion()
                self.close()
                self.main = mainwindow(rol, usuario_obj, sesion.maestro_actual)
                self.main.show()
            else:
                sesion.administrador_actual=Administrador(usuario, contrasenna)
                sesion.administrador_actual.iniciarSesion()
                self.close()
                self.main = mainwindow(rol, usuario_obj, sesion.administrador_actual)
                self.main.show()
            
        else:
            self.ErrMsg("Usuario o contraseña incorrectos")

    def ErrMsg(self, mensaje):
        self.error_label.setText(mensaje)
        self.error_label.setStyleSheet("color: red; font-weight: bold; padding: 5px; border-radius: 5px; background-color: rgba(255, 0, 0, 0.1);")
        self.error_label.setVisible(True)