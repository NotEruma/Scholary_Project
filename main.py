from resources import Recursos
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget
from PyQt5.QtCore import Qt

import sesion

class mainwindow(QtWidgets.QMainWindow):
    def __init__(self, rol,usuario_obj, tipo_Usu):
        super().__init__()
        uic.loadUi("interfaces/main.ui", self) #Hice una carpeta aparte para las interfaces
        self.hideLabel_3.hide()
        self.latBar = 1
        self.resizableBarButt.clicked.connect(lambda: self.sideBar())
        self.logOutButtIco_3.clicked.connect(self.cerrarSesion)
        self.stackedWidget.setCurrentIndex(0)
        self.usuario_obj = usuario_obj
        self.tipoUsu=tipo_Usu
        

        #Comprobar el rol y ocultar botones
        self.rol = rol
        if rol != "administrador":
            self.maesButtIcon_3.setVisible(False)
        self.show()
        
        #Botones de la barra lateral
        self.inicButtIco.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.alumButtIco_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))
        self.materButtIco_6.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.maesButtIcon_3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(7))
        self.ayudbuttIco_3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.configButtico_3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        
        #Botones Alumnos inscritos
        self.btnConsultarAlumnIns.clicked.connect(self.mostrarAlumnos)
        self.ActuAlumnIns.clicked.connect(self.actualizarAlumno)
        self.btnRegresarAlumnIns.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        
        #Botón para Admin: registrar alumno
        self.RegAlumn.clicked.connect(self.abrirRegistrarAlumno)


        #Distribuir uniformemente las columnas de la tabla
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
        grado=self.cbGradoAlumnIns.currentText()
        grupo=self.cbGrupoAlumnIns.currentText()
        if grado == "Seleccione un grado" or grupo == "Seleccione un grupo":
            self.lbErrorAlumnIns.setText("Por favor, selecciona un grado y un grupo.")
            return
        self.lbErrorAlumnIns.setText("")

        alumnos = self.usuario_obj.verAlumnos(grado, grupo)
        if alumnos:
            self.tablaAlumIns.setRowCount(0)
            self.tablaAlumIns.setRowCount(len(alumnos))
            for row, alumno in enumerate(alumnos):
                for col, dato in enumerate(alumno):
                    item = QTableWidgetItem(str(dato))
                    item.setFlags(item.flags() | Qt.ItemIsEditable)  # Hacer la celda editable
                    self.tablaAlumIns.setItem(row, col, item)
        else:
            self.lbErrorAlumnIns.setText("No hay alumnos en este grupo.")
    def actualizarAlumno(self):
        filaSeleccionada = self.tablaAlumIns.currentRow()
        if filaSeleccionada == -1:  # Si no se ha seleccionado ninguna fila
            self.lbErrorAlumnIns.setText("Por favor, selecciona un alumno para editar.")
            return
        id_alumno = self.tablaAlumIns.item(filaSeleccionada, 0).text()  # Columna 0 para ID
        nombre = self.tablaAlumIns.item(filaSeleccionada, 1).text()  # Columna 1 para nombre
        apellidop = self.tablaAlumIns.item(filaSeleccionada, 2).text()  # Columna 2 para apellido paterno
        apellidom = self.tablaAlumIns.item(filaSeleccionada, 3).text()  # Columna 3 para apellido materno
        grado = self.cbGradoAlumnIns.currentText()  # cb para grado
        grupo = self.cbGrupoAlumnIns.currentText()  # cb para grupo
        telefono = self.tablaAlumIns.item(filaSeleccionada, 4).text()  # Columna 6 para teléfono
        
        if self.tipoUsu:
            resultado=self.tipoUsu.editarAlumno(id_alumno, nombre, apellidop, apellidom, grado, grupo, telefono)
            if resultado:
                self.lbErrorAlumnIns.setText("Alumno actualizado correctamente.")
            else:
                self.lbErrorAlumnIns.setText("Error al actualizar el alumno.")
#Funciones para registrar Alumno:
    def abrirRegistrarAlumno(self):
        self.registrarAl=uic.loadUi("interfaces/regAlumn.ui")
        self.registrarAl.btnRegistrar.clicked.connect(self.registrarAlumno)
        self.registrarAl.btnRegresarRA.clicked.connect(self.regresarAl)
        self.registrarAl.show()
    def registrarAlumno(self):
        nombre=self.registrarAl.LNombre.text()
        apellidop=self.registrarAl.LApellidoP.text()
        apellidom=self.registrarAl.LApellidoM.text()
        grado=self.registrarAl.cbGrado.currentText()
        grupo=self.registrarAl.cbGrupo.currentText()
        telefono=self.registrarAl.LTelefono.text()
        if not nombre or not apellidop or not apellidom or not grado or not grupo:
            self.registrarAl.lbError.setText("Los campos con * son obligatorios.")  
            return
        try:
            grado = int(grado)
        except ValueError:
            print("El grado debe ser un número entero")
        
        if self.tipoUsu:
            resultado=self.tipoUsu.registrarAlumno(nombre, apellidop, apellidom, grado, grupo, telefono)
            if resultado:
                self.registrarAl.lbError.setText("")
                self.registrarAl.lbError.setText("Alumno registrado exitosamente.")
            else: 
                self.registrarAl.lbError.setText("")
                self.registrarAl.lbError.setText("No se realizó la acción.")
        else:
            print('No existe el administrador.')
    def regresarAl(self):
        self.registrarAl.hide()

