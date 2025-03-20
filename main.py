from resources import Recursos
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem

class mainwindow(QtWidgets.QMainWindow):
    def __init__(self, rol,usuario_obj):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.hideLabel_3.hide()
        self.latBar = 1
        self.resizableBarButt.clicked.connect(lambda: self.sideBar())
        self.logOutButtIco_3.clicked.connect(self.cerrarSesion)
        self.stackedWidget.setCurrentIndex(0)
        self.usuario_obj = usuario_obj

        self.rol = rol
        if rol != "administrador":
            self.maesButtIcon_3.setVisible(False)
        self.show()

        self.inicButtIco.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.alumButtIco_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))
        self.materButtIco_6.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.maesButtIcon_3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(7))
        self.ayudbuttIco_3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.configButtico_3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))
        #Alumnos inscritos
        self.btnConsultar.clicked.connect(self.mostrarAlumnos)
        self.btnRegresar.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))

        header = self.tablaAlumIns.horizontalHeader()
        header.setStretchLastSection(True)
        for col in range(self.tablaAlumIns.columnCount()):
            self.tablaAlumIns.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)
       
    def sideBar(self):
        if self.latBar == 0:
            self.animation = QPropertyAnimation(self.sidebar, b"maximumWidth")
            self.animation.setDuration(150)
            self.animation.setStartValue(225)
            self.animation.setEndValue(64)
            self.hideLabel_3.hide()
            self.animation.start()
            

            self.animation1= QPropertyAnimation(self.sidebar, b"minimumWidth")
            self.animation1.setDuration(150)
            self.animation1.setStartValue(225)
            self.animation1.setEndValue(64)
            self.animation1.start()
            self.latBar = 1
        else:
            self.animation = QPropertyAnimation(self.sidebar, b"maximumWidth")
            self.animation.setDuration(150)
            self.animation.setStartValue(64)
            self.animation.setEndValue(225)
            self.animation.start()
            self.hideLabel_3.show()

            self.animation1 = QPropertyAnimation(self.sidebar, b"minimumWidth")
            self.animation1.setDuration(150)
            self.animation1.setStartValue(64)
            self.animation1.setEndValue(225)
            self.animation1.start()
            self.latBar = 0

    def cerrarSesion(self):
        self.usuario_obj.cerrarCon()
        self.close()
        from loginWin import LoginC
        self.login = LoginC()
        self.login.show()
    
    def mostrarAlumnos(self):
        grado=self.cbGrado.currentText()
        grupo=self.cbGrupo.currentText()
        if grado == "Seleccione un grado" or grupo == "Seleccione un grupo":
            self.lbError.setText("Por favor, selecciona un grado y un grupo.")
            return
        self.lbError.setText("")

        alumnos = self.usuario_obj.verAlumnos(grado, grupo)
        if alumnos:
            self.tablaAlumIns.setRowCount(0)
            self.tablaAlumIns.setRowCount(len(alumnos))
            for row, alumno in enumerate(alumnos):
                for col, dato in enumerate(alumno):
                    self.tablaAlumIns.setItem(row, col, QTableWidgetItem(str(dato)))
        else:
            self.lbError.setText("No hay alumnos en este grupo.")