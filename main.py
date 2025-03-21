from resources import Recursos
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtWidgets, uic, QtCore
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
        self.logOutButtIco.clicked.connect(self.cerrarSesion)
        self.stackedWidget.setCurrentIndex(0)
        self.usuario_obj = usuario_obj
        self.tipoUsu=tipo_Usu
        

        #Comprobar el rol y ocultar botones
        self.rol = rol
        if rol != "administrador":
            self.userButtIcon.setVisible(False)
        if rol == "administrador":
            #Ocultar botones de registrar calificación al admin
            self.btnRegisCalif.setVisible(False)
        self.show()
        
        #Botones de la barra lateral
        self.inicButtIco.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.userButtIcon.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.materButtIco.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.alumButtIcon.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.califbuttIco.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.ayudbuttIco.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.configButtico.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        #Botones Alumnos inscritos
        self.btnConsultarAlumnIns.clicked.connect(self.mostrarAlumnos)
        
        self.btnRegresarAlumnIns.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        
        #Botón para Admin: registro de alumnos
        self.RegAlumn.clicked.connect(self.abrirRegistrarAlumno)
        self.ActuAlumnIns.clicked.connect(self.actualizarAlumno)
        self.ElimnAlumnIns.clicked.connect(self.bajaAlumno)
        
        #Botón para Maestro: registrar calificación
        self.btnRegisCalif.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))
        self.btnConsultarCalif_2.clicked.connect(self.maestroMostCalif)
        self.cargarMatMaestro()


        #Distribuir uniformemente las columnas de la tabla
        header = self.tablausers.horizontalHeader()
        header.setStretchLastSection(True)
        for col in range(self.tablausers.columnCount()):
            self.tablausers.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)

        header = self.tablamater.horizontalHeader()
        header.setStretchLastSection(True)
        for col in range(self.tablamater.columnCount()):
            self.tablamater.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)
        
        header = self.tablaAlumIns.horizontalHeader()
        header.setStretchLastSection(True)
        for col in range(self.tablaAlumIns.columnCount()):
            self.tablaAlumIns.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)

        header = self.tablaCalif.horizontalHeader()
        header.setStretchLastSection(True)
        for col in range(self.tablaCalif.columnCount()):
            self.tablaCalif.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)

        header = self.tablaRegCalif.horizontalHeader()
        header.setStretchLastSection(True)
        for col in range(self.tablaRegCalif.columnCount()):
            self.tablaRegCalif.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)
       
    def sideBar(self):
        if self.latBar == 0:
            self.animation = QPropertyAnimation(self.sidebar, b"maximumWidth")
            self.animation.setDuration(150)
            self.animation.setStartValue(225)
            self.animation.setEndValue(55)
            self.hideLabel_3.hide()
            self.animation.start()
            

            self.animation1= QPropertyAnimation(self.sidebar, b"minimumWidth")
            self.animation1.setDuration(150)
            self.animation1.setStartValue(225)
            self.animation1.setEndValue(55)
            self.animation1.start()
            self.latBar = 1
        else:
            self.animation = QPropertyAnimation(self.sidebar, b"maximumWidth")
            self.animation.setDuration(150)
            self.animation.setStartValue(55)
            self.animation.setEndValue(225)
            self.animation.start()
            self.hideLabel_3.show()

            self.animation1 = QPropertyAnimation(self.sidebar, b"minimumWidth")
            self.animation1.setDuration(150)
            self.animation1.setStartValue(55)
            self.animation1.setEndValue(225)
            self.animation1.start()
            self.latBar = 0
#Funciones para stacked de alumno
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
        self.lbErrorAlumnIns.setText("")
    def actualizarAlumno(self):
        filaSeleccionada = self.tablaAlumIns.currentRow()
        if filaSeleccionada == -1:  # Si no se ha seleccionado ninguna fila
            self.lbErrorAlumnIns.setText("Por favor, selecciona un alumno para editar.")
            return
        self.lbErrorAlumnIns.setText("")
        id_alumno = self.tablaAlumIns.item(filaSeleccionada, 0).text()  # Columna 0 para ID
        nombre = self.tablaAlumIns.item(filaSeleccionada, 1).text()  # Columna 1 para nombre
        apellidop = self.tablaAlumIns.item(filaSeleccionada, 2).text()  # Columna 2 para apellido paterno
        apellidom = self.tablaAlumIns.item(filaSeleccionada, 3).text()  # Columna 3 para apellido materno
        grado = self.cbGradoAlumnIns.currentText()  # cb para grado
        grupo = self.cbGrupoAlumnIns.currentText()  # cb para grupo
        telefono = self.tablaAlumIns.item(filaSeleccionada, 4).text()  # Columna 6 para teléfono
        estado = self.tablaAlumIns.item(filaSeleccionada, 5).text()
        
        if self.tipoUsu:
            resultado=self.tipoUsu.editarAlumno(id_alumno, nombre, apellidop, apellidom, grado, grupo, telefono, estado)
            if resultado:
                self.lbErrorAlumnIns.setText("Alumno actualizado correctamente.")
            else:
                self.lbErrorAlumnIns.setText("Error al actualizar el alumno.")
        self.lbErrorAlumnIns.setText("")
    def bajaAlumno(self):
        filaSeleccionada = self.tablaAlumIns.currentRow()
        if filaSeleccionada == -1:  # Si no se ha seleccionado ninguna fila
            self.lbErrorAlumnIns.setText("Por favor, selecciona un alumno para editar.")
            return
        self.lbErrorAlumnIns.setText("")
        id_alumno = self.tablaAlumIns.item(filaSeleccionada, 0).text()
        if self.tipoUsu:
            resultado=self.tipoUsu.eliminarAlumno(id_alumno)
            if resultado:
                self.lbErrorAlumnIns.setText("Alumno dado de baja.")
            else:
                self.lbErrorAlumnIns.setText("Error al dar de baja al alumno.")
        self.lbErrorAlumnIns.setText("")
        
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
            self.registrarAl.lbError.setText("Los campos son obligatorios.")  
            return
        try:
            grado = int(grado)
        except ValueError:
            print("El grado debe ser un número entero")
        self.registrarAl.lbError.setText("")  
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

    def maestroMostCalif(self):
        id_alumno = self.IDRegCalif.text()  
        id_asignatura = self.cbMateriaCalif_2.currentText() 
        #Falta arreglar esto:
        if not id_alumno and not id_asignatura:
            self.lbErrorCalif_2.setText("Ingrese el ID del alumno y de la materia.")
            return
        elif not id_alumno:
            self.lbErrorCalif_2.setText("Ingrese ID del alumno.")
            return
        elif not id_asignatura:
            self.lbErrorCalif_2.setText("Ingrese ID de la materia.")
            return
        self.lbErrorCalif_2.setText("")
        
        
        if self.tipoUsu:
            resultado=self.tipoUsu.verificarAl(id_alumno, id_asignatura)
            if resultado == "El alumno no está inscrito en esta materia.":
                self.lbErrorCalif_2.setText(resultado)
                return
            else: 
                calificaciones=self.tipoUsu.verificarCalif(id_alumno, id_asignatura)
                if calificaciones:
                    alumno, asignatura = self.tipoUsu.consultarAlumno(id_alumno, id_asignatura)
                    if alumno and asignatura:
                        self.tablaRegCalif.setRowCount(0)  
                        posicion_f = self.tablaRegCalif.rowCount()
                        self.tablaRegCalif.insertRow(posicion_f)
                        nombre_completo = f"{alumno[1]} {alumno[2]} {alumno[3]}"

                        self.tablaRegCalif.setItem(posicion_f, 0, QtWidgets.QTableWidgetItem(str(alumno[0])))  # ID Alumno
                        self.tablaRegCalif.setItem(posicion_f, 1, QtWidgets.QTableWidgetItem(nombre_completo))  # Nombre Alumno
                        self.tablaRegCalif.setItem(posicion_f, 2, QtWidgets.QTableWidgetItem(asignatura[1]))  # Nombre Asignatura
                        self.tablaRegCalif.setItem(posicion_f, 3, QtWidgets.QTableWidgetItem(str(calificaciones[0])))
                        self.tablaRegCalif.setItem(posicion_f, 4, QtWidgets.QTableWidgetItem(str(calificaciones[1])))
                        self.tablaRegCalif.setItem(posicion_f, 5, QtWidgets.QTableWidgetItem(str(calificaciones[2])))
                else:
                    alumno, asignatura = self.tipoUsu.consultarAlumno(id_alumno, id_asignatura)
                    if alumno and asignatura:
                        self.tablaRegCalif.setRowCount(0)  
                        posicion_f = self.tablaRegCalif.rowCount()
                        self.tablaRegCalif.insertRow(posicion_f)
                        nombre_completo = f"{alumno[1]} {alumno[2]} {alumno[3]}"

                        self.tablaRegCalif.setItem(posicion_f, 0, QtWidgets.QTableWidgetItem(str(alumno[0])))  # ID Alumno
                        self.tablaRegCalif.setItem(posicion_f, 1, QtWidgets.QTableWidgetItem(nombre_completo))  # Nombre Alumno
                        self.tablaRegCalif.setItem(posicion_f, 2, QtWidgets.QTableWidgetItem(asignatura[1]))  # Nombre Asignatura
                    for col in range(3, 6):
                        item = QtWidgets.QTableWidgetItem("")
                        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                        self.tablaRegCalif.setItem(posicion_f, col, item)
                self.lbErrorCalif_2.setText("")
    #Aun no esta funcionando correctamente, solo entra al else, resultado regresa vacio
            """elif resultado:
                alumno, asignatura = self.tipoUsu.consultarAlumno(id_alumno, id_asignatura)
                if alumno and asignatura:
                    self.tablaRegCalif.setRowCount(0)  
                    posicion_f = self.tablaRegCalif.rowCount()
                    self.tablaRegCalif.insertRow(posicion_f)
                    nombre_completo = f"{alumno[1]} {alumno[2]} {alumno[3]}"

                    self.tablaRegCalif.setItem(posicion_f, 0, QtWidgets.QTableWidgetItem(str(alumno[0])))  # ID Alumno
                    self.tablaRegCalif.setItem(posicion_f, 1, QtWidgets.QTableWidgetItem(nombre_completo))  # Nombre Alumno
                    self.tablaRegCalif.setItem(posicion_f, 2, QtWidgets.QTableWidgetItem(asignatura[1]))  # Nombre Asignatura
                    self.tablaRegCalif.setItem(posicion_f, 3, QtWidgets.QTableWidgetItem(str(resultado[0])))"""
                
    def cargarMatMaestro(self):
        datos=self.tipoUsu.obtenerMaterias()
        self.cbMateriaCalif_2.clear()
        self.cbMateriaCalif_2.addItems(datos)

    def registrarCal(self):
        pass
