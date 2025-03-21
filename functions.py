import mysql.connector
from PyQt5.QtWidgets import QApplication
from loginWin import LoginC

class Usuario:
    def __init__(self, usuario, contrasenna):
        self.usuario=usuario
        self.contrasenna=contrasenna
        self.baseDatos="informacion"
        self.host="localhost"
        self.auth_plugin='caching_sha2_password'
        self.conn=None
        self.cursor=None
    def iniciarSesion(self):
        try:
            self.conn=mysql.connector.connect(
                host=self.host,
                user=self.usuario,
                password=self.contrasenna,
                database=self.baseDatos,
                auth_plugin=self.auth_plugin
            )
            self.cursor=self.conn.cursor()
            sql="SELECT * FROM usuario WHERE identificador=%s AND contraseña=%s AND estado='Activo'"
            self.cursor.execute(sql,(self.usuario, self.contrasenna ))
            resultado=self.cursor.fetchone()
            if resultado:
                print("Inicio de sesión correcto.")
                return True
        except mysql.connector.Error as err:
            print(f"Error al conectar: {err}")
            if err.errno==1045:
                print("Error de autenticación.")
            return False
    def consultarAlumno(self, id_alumno, id_asignatura):
        if self.cursor:
            sqlAlumno="SELECT * FROM alumno WHERE id_alumno = %s"
            self.cursor.execute(sqlAlumno, (id_alumno,))
            alumno= self.cursor.fetchall()
            if alumno:
                sqlAsignatura='''
                SELECT a.id_asignatura, a.nombre
                FROM alumno_asignatura aa
                INNER JOIN asignatura a ON aa.id_asignatura = a.id_asignatura
                WHERE aa.id_alumno = %s AND aa.id_asignatura = %s
                '''
                self.cursor.execute(sqlAsignatura, (id_alumno, id_asignatura))
                asignatura = self.cursor.fetchall()
                if asignatura:
                    return alumno[0], asignatura[0]
        else:
            print("No se puede obtener el alumno.")
    def obtenerRol(self):
        if self.cursor:
            sql="SELECT rol FROM usuario WHERE identificador=%s"
            self.cursor.execute(sql, (self.usuario,))
            resultado=self.cursor.fetchone()
            if resultado:
                self.rol=resultado[0]
                return self.rol
        return None
    def obtenerIdM(self):
        if self.rol == 'maestro':
            if self.cursor:
                sql="SELECT id_maestro FROM maestro WHERE id_usuario = (SELECT id_usuario FROM usuario WHERE identificador = %s)"
                self.cursor.execute(sql, (self.usuario,))
                resultado=self.cursor.fetchone()
                if resultado:
                    return resultado[0]
                else: return None
    def verAlumnos(self, grado, grupo):
        if self.cursor:
            self.conn.commit()
            sql = "SELECT id_alumno, nombre, apellidop, apellidom, telefono, estado FROM alumno WHERE grado = %s AND grupo = %s"
            self.cursor.execute(sql, (grado, grupo))
            alumnos = self.cursor.fetchall()
            return alumnos

    def cerrarCon(self):
        if self.conn:
            self.conn.close()

class Administrador(Usuario):
    def __init__(self, usuario, contrasenna):
        super().__init__(usuario, contrasenna)
    def registrarMateria(self, id_asignatura, nombre, grado):
        if self.cursor:
            print(f"Registrando materia: {nombre}")
            sql="INSERT INTO asignatura(id_asignatura, nombre, grado) VALUES (%s, %s, %s)"
            valores=(id_asignatura, nombre, grado)
            self.cursor.execute(sql, valores)
            self.conn.commit()
            return True
        else:
            print("No se puede conectar a la base de datos.")
            return False
    def eliminarMateria(self, id_asignatura):
        if self.cursor:
            sql="DELETE FROM asignatura WHERE id_asignatura = %s"
            self.cursor.execute(sql, (id_asignatura,))
            self.conn.commit()
            print(f"La materia con el ID: {id_asignatura} ha sido eliminada.")
        else:
            print("No se pudo eliminar la materia.")
    def editarMateria(self, id_asignatura, nombre, grado):
        if not id_asignatura or not nombre or not grado:
            print("Datos inválidos para la actualización.")
            return False
        if self.cursor:
            try:
                sql = """UPDATE asignatura SET nombre = %s, grado = %s WHERE id_asignatura = %s"""
                valores = (nombre, grado, id_asignatura)
                self.cursor.execute(sql, valores)
                self.conn.commit()
                return True
            except Exception as e:
                print(f"Error al actualizar la materia: {e}")
                return False
        else:
            print("No se puede conectar a la base de datos.")
            return False
    def verMaterias(self):
        if self.cursor:
            self.conn.commit() 
            sql = "SELECT id_asignatura, nombre, grado FROM asignatura"
            self.cursor.execute(sql)
            materias = self.cursor.fetchall()
            return materias
    def registrarAlumno(self, nombre, apellidop, apellidom, grado, grupo, telefono):
        if self.cursor:
            print(f"Registrando alumno: {nombre} {apellidop} {apellidom}, Grado: {grado}, Grupo: {grupo}, Tel: {telefono}")
            sql="INSERT INTO alumno(nombre, apellidop, apellidom, grado, grupo, telefono) VALUES (%s, %s, %s, %s, %s,%s)"
            valores=(nombre, apellidop, apellidom, grado, grupo, telefono)
            self.cursor.execute(sql, valores)
            self.conn.commit()
            return True
        else:
            print("No se puede conectar a la base de datos.")
            return False
    def editarAlumno(self, id_alumno, nombre, apellidop, apellidom, grado, grupo, telefono, estado):
        if self.cursor:
            sql = """UPDATE alumno SET nombre = %s, apellidop = %s, apellidom = %s, grado = %s, grupo = %s, telefono = %s, estado =%s
                    WHERE id_alumno = %s"""
            valores = (nombre, apellidop, apellidom, grado, grupo, telefono, estado, id_alumno)
            self.cursor.execute(sql, valores)
            self.conn.commit()
            return True
        else:
            print("No se puede conectar a la base de datos.")
            return False
    def eliminarAlumno(self, idAlumno):
        if self.cursor:
            sql="UPDATE alumno SET estado= 'Inactivo' WHERE id_alumno = %s"
            self.cursor.execute(sql, (idAlumno,))
            self.conn.commit()
            print(f"El alumno con el ID: {idAlumno} ha sido eliminado.")
            return True
        else:
            print("No se pudo eliminar el alumno.")
            return False
    def registrarMaestro(self,nMaestro, nContrasenna, nombre):
        if self.cursor:
            try:
                self.cursor.execute(f"CREATE USER '{nMaestro}'@'localhost' IDENTIFIED BY '{nContrasenna}'")
                self.cursor.execute(f"GRANT SELECT, INSERT, UPDATE, DELETE ON {self.baseDatos}.calificacion TO '{nMaestro}'@'localhost'")
                self.cursor.execute(f"GRANT SELECT ON {self.baseDatos}.alumno TO '{nMaestro}'@'localhost'")
                self.cursor.execute(f"GRANT SELECT ON {self.baseDatos}.asignatura TO '{nMaestro}'@'localhost'")
                self.cursor.execute(f"GRANT SELECT, INSERT, UPDATE, DELETE ON {self.baseDatos}.doc_calificaciones TO '{nMaestro}'@'localhost'")
                self.cursor.execute(f"GRANT SELECT ON {self.baseDatos}.usuario TO '{nMaestro}'@'localhost'")
                self.cursor.execute(f"GRANT SELECT ON {self.baseDatos}.maestro TO '{nMaestro}'@'localhost'")
                self.cursor.execute(f"GRANT SELECT ON {self.baseDatos}.alumno_asignatura TO '{nMaestro}'@'localhost'")
                self.cursor.execute(f"GRANT EXECUTE ON PROCEDURE {self.baseDatos}.GenerarDoc_Calificaciones TO '{nMaestro}'@'localhost'")
                self.cursor.execute("FLUSH PRIVILEGES")

                sql="INSERT INTO usuario(identificador, contraseña, rol) VALUES (%s, %s, 'maestro')"
                valores=(nMaestro, nContrasenna)
                self.cursor.execute(sql, valores)
                self.conn.commit()

                id_usuario=self.cursor.lastrowid
                sql_maestro="INSERT INTO maestro (id_usuario, nombre) VALUES (%s, %s)"
                valores_maestro=(id_usuario, nombre)
                self.cursor.execute(sql_maestro, valores_maestro)
                self.conn.commit()
                print(f"Maestro {nMaestro} ingresado correctamente.")
            except mysql.connector.Error as err:
                print(f"Error al registrar maestro: {err}")
        else:
            print("No se puede conectar a la base de datos.")
    def verMaestros(self):
        if self.cursor:
            self.conn.commit() 
            sql = "SELECT id_maestro, nombre, estado FROM maestro"
            self.cursor.execute(sql)
            maestros = self.cursor.fetchall()
            return maestros
    def actualizarMaestro(self, id_maestro, nuevoMaestro, nuevaContrasenna, nuevoNombre=None): #Nuevo método
        if self.cursor:
            try:
                sql_obtener_maestro = """
                    SELECT u.identificador, u.id_usuario
                    FROM usuario u
                    JOIN maestro m ON u.id_usuario = m.id_usuario 
                    WHERE m.id_maestro = %s
                """
                self.cursor.execute(sql_obtener_maestro, (id_maestro,))
                maestro_data = self.cursor.fetchone()
                if not maestro_data:
                    print(f"No se encontró un maestro con ID: {id_maestro}.")
                    return
                antiguoMaestro, id_usuario = maestro_data

                self.cursor.execute(f"RENAME USER '{antiguoMaestro}'@'localhost' TO '{nuevoMaestro}'@'localhost'")
                self.cursor.execute(f"ALTER USER '{nuevoMaestro}'@'localhost' IDENTIFIED BY '{nuevaContrasenna}'")
                self.cursor.execute("FLUSH PRIVILEGES")

                sql_usuario = "UPDATE usuario SET identificador = %s, contraseña = %s WHERE id_usuario = %s"
                valores_usuario = (nuevoMaestro, nuevaContrasenna, id_usuario)
                self.cursor.execute(sql_usuario, valores_usuario)
                self.conn.commit()

                if nuevoNombre:
                    sql_maestro = "UPDATE maestro SET nombre = %s WHERE id_maestro = %s"
                    valores_maestro = (nuevoNombre, id_maestro)
                    self.cursor.execute(sql_maestro, valores_maestro)
                    self.conn.commit()
                    print(f"El nombre del maestro ha sido cambiado a {nuevoNombre}.")

                print(f"El maestro {antiguoMaestro} ha sido actualizado correctamente a {nuevoMaestro}.")

            except Exception as err:
                print(f"Error al actualizar el maestro: {err}")
    def registrarAdmin(self, nAdmin, nContrasenna, nombre):
        if self.cursor:
            self.cursor.execute(f"CREATE USER '{nAdmin}'@'localhost' IDENTIFIED BY '{nContrasenna}'")
            self.cursor.execute(f"GRANT ALL PRIVILEGES ON *.* TO '{nAdmin}'@'localhost'")
            self.cursor.execute(f"GRANT GRANT OPTION ON *.* TO '{nAdmin}'@'localhost';")
            self.cursor.execute(f"GRANT CREATE USER ON *.* TO '{nAdmin}'@'localhost';")
            self.cursor.execute("FLUSH PRIVILEGES")

            sql="INSERT INTO usuario(identificador, contraseña, rol) VALUES (%s, %s, 'administrador')"
            valores=(nAdmin, nContrasenna)
            self.cursor.execute(sql, valores)
            self.conn.commit()

            id_usuario=self.cursor.lastrowid
            sql_admin="INSERT INTO administrador (id_usuario, nombre) VALUES (%s, %s)"
            valores_admin=(id_usuario, nombre)
            self.cursor.execute(sql_admin, valores_admin)
            self.conn.commit()
            print(f"Administrador {nAdmin} ingresado correctamente.")
    def actualizarAdmin(self, id_admin, nuevoAdmin, nuevaContrasenna, nuevoNombre=None):  #Nuevo método
        if self.cursor:
            try:
                sql_get_admin = """
                    SELECT u.identificador, u.id_usuario
                    FROM usuario u
                    JOIN administrador a ON u.id_usuario = a.id_usuario 
                    WHERE a.id_administrador = %s
                """
                self.cursor.execute(sql_get_admin, (id_admin,))
                admin_data = self.cursor.fetchone()
                if not admin_data:
                    print(f"No se encontró un administrador con ID: {id_admin}.")
                    return
                antiguoAdmin, id_usuario = admin_data

                self.cursor.execute(f"RENAME USER '{antiguoAdmin}'@'localhost' TO '{nuevoAdmin}'@'localhost'")
                self.cursor.execute(f"ALTER USER '{nuevoAdmin}'@'localhost' IDENTIFIED BY '{nuevaContrasenna}'")
                self.cursor.execute("FLUSH PRIVILEGES")

                sql_usuario = "UPDATE usuario SET identificador = %s, contraseña = %s WHERE id_usuario = %s"
                valores_usuario = (nuevoAdmin, nuevaContrasenna, id_usuario)
                self.cursor.execute(sql_usuario, valores_usuario)
                self.conn.commit()

                if nuevoNombre:
                    sql_admin = "UPDATE administrador SET nombre = %s WHERE id_administrador = %s"
                    valores_admin = (nuevoNombre, id_admin)
                    self.cursor.execute(sql_admin, valores_admin)
                    self.conn.commit()
                    print(f"El nombre del administrador ha sido cambiado a {nuevoNombre}.")

                print(f"El administrador {antiguoAdmin} ha sido actualizado correctamente a {nuevoAdmin}.")

            except Exception as err:
                print(f"Error al actualizar el administrador: {err}")

    def desactivarUsuario(self, usuario):
        if self.cursor:
            self.cursor.execute(f"UPDATE usuario SET estado='Inactivo' WHERE identificador=%s", (usuario,))
            self.conn.commit()
            print(f"Usuario {usuario} marcado como 'Inactivo'.")
        else:
            print("No se pudo realizar la acción.")
    def asignarAsignaturasAlumno(self, id_alumno, id_asig1, id_asig2, id_asig3, id_asig4, id_asig5, id_asig6, id_asig7): #Nuevo método
        if self.cursor:
            try:
                sql_verificar_alumno = """
                    SELECT grado FROM alumno WHERE id_alumno = %s
                """
                self.cursor.execute(sql_verificar_alumno, (id_alumno,))
                resultado_alumno = self.cursor.fetchone()
                if not resultado_alumno:
                    print(f"No se encontró un alumno con ID: {id_alumno}.")
                    return
                grado_alumno = resultado_alumno[0]

                asignaturas = [id_asig1, id_asig2, id_asig3, id_asig4, id_asig5, id_asig6, id_asig7]

                for id_asignatura in asignaturas:
                    sql_verificar_asignatura = """
                        SELECT grado FROM asignatura WHERE id_asignatura = %s
                    """
                    self.cursor.execute(sql_verificar_asignatura, (id_asignatura,))
                    resultado_asignatura = self.cursor.fetchone()
                    if not resultado_asignatura:
                        print(f"No se encontró una asignatura con ID: {id_asignatura}.")
                        continue
                    grado_asignatura = resultado_asignatura[0]

                    if grado_alumno != grado_asignatura:
                        print(f"El alumno no puede inscribirse en la asignatura {id_asignatura} porque no pertenece a su grado.")
                        continue

                    sql_insert = "INSERT INTO alumno_asignatura(id_alumno, id_asignatura) VALUES (%s, %s)"
                    valores = (id_alumno, id_asignatura)
                    self.cursor.execute(sql_insert, valores)
                self.conn.commit()
                print(f"El alumno {id_alumno} ha sido inscrito en las asignaturas correctamente.")
            except Exception as err:
                print(f"Error al asignar las asignaturas al alumno: {err}")
    def asignarAsignaturasMaestro(self, id_maestro, id_asig1, id_asig2, id_asig3): #Nuevo método
        if self.cursor:
            try:
                sql_verificar_maestro = """
                    SELECT id_maestro FROM maestro WHERE id_maestro = %s
                """
                self.cursor.execute(sql_verificar_maestro, (id_maestro,))
                resultado_maestro = self.cursor.fetchone()
                if not resultado_maestro:
                    print(f"No se encontró un maestro con ID: {id_maestro}.")
                    return
                
                asignaturas = [id_asig1, id_asig2, id_asig3]

                for id_asignatura in asignaturas:
                    sql_verificar_asignatura = """
                        SELECT id_asignatura FROM asignatura WHERE id_asignatura = %s
                    """
                    self.cursor.execute(sql_verificar_asignatura, (id_asignatura,))
                    resultado_asignatura = self.cursor.fetchone()
                    if not resultado_asignatura:
                        print(f"No se encontró una asignatura con ID: {id_asignatura}.")
                        continue

                    sql_insert = "INSERT INTO maestro_asignatura (id_maestro, id_asignatura) VALUES (%s, %s)"
                    valores = (id_maestro, id_asignatura)
                    self.cursor.execute(sql_insert, valores)
                self.conn.commit()
                print(f"El maestro {id_maestro} ha sido asignado a las asignaturas correctamente.")
            
            except Exception as err:
                print(f"Error al asignar las asignaturas al maestro: {err}")
    def actualizarAsignaturasMaestro(self, id_maestro, id_asig1, id_asig2, id_asig3): #Nuevo método
        if self.cursor:
            try:
                sql_verificar_maestro = "SELECT id_maestro FROM maestro WHERE id_maestro = %s"
                self.cursor.execute(sql_verificar_maestro, (id_maestro,))
                resultado_maestro = self.cursor.fetchone()

                if not resultado_maestro:
                    print(f"No se encontró un maestro con ID: {id_maestro}.")
                    return

                sql_update = """
                    UPDATE maestro_asignatura 
                    SET id_asignatura = CASE 
                        WHEN id_asignatura = %s THEN %s 
                        WHEN id_asignatura = %s THEN %s 
                        WHEN id_asignatura = %s THEN %s 
                        ELSE id_asignatura END
                    WHERE id_maestro = %s
                """
                valores = (id_asig1, id_asig1, id_asig2, id_asig2, id_asig3, id_asig3, id_maestro)
                self.cursor.execute(sql_update, valores)
                self.conn.commit()
                print(f"Las asignaturas del maestro {id_maestro} han sido actualizadas correctamente.")
            except Exception as err:
                print(f"Error al actualizar las asignaturas del maestro: {err}")
                
    #Usé un DELETE e INSERT a diferencia del maestro que usa UPDATE, porque un maestro puede seguir dando las misma materias,
    #pero un alumno no puede cursarlas a menos que repruebe y así, además de que en este caso hay que verificar que el grado sea el mismo.
    def actualizarAsignaturasAlumno(self, id_alumno, id_asig1, id_asig2, id_asig3, id_asig4, id_asig5, id_asig6, id_asig7):
        if self.cursor:
            try:
                sql_verificar_alumno = "SELECT id_alumno FROM alumno WHERE id_alumno = %s"
                self.cursor.execute(sql_verificar_alumno, (id_alumno,))
                resultado_alumno = self.cursor.fetchone()
                if not resultado_alumno:
                    print(f"No se encontró un alumno con ID: {id_alumno}.")
                    return
                asignaturas = [id_asig1, id_asig2, id_asig3, id_asig4, id_asig5, id_asig6, id_asig7]
                
                sql_borrarA = "DELETE FROM alumno_asignatura WHERE id_alumno = %s"
                self.cursor.execute(sql_borrarA, (id_alumno,))

                for id_asignatura in asignaturas:
                    sql_verificar_asignatura = "SELECT grado FROM asignatura WHERE id_asignatura = %s"
                    self.cursor.execute(sql_verificar_asignatura, (id_asignatura,))
                    resultado_asignatura = self.cursor.fetchone()
                    if not resultado_asignatura:
                        print(f"No se encontró una asignatura con ID: {id_asignatura}.")
                        continue
                    
                    grado_asignatura = resultado_asignatura[0]
                    sql_verificar_grado_alumno = "SELECT grado FROM alumno WHERE id_alumno = %s"
                    self.cursor.execute(sql_verificar_grado_alumno, (id_alumno,))
                    resultado_grado_alumno = self.cursor.fetchone()
                    grado_alumno = resultado_grado_alumno[0]

                    if grado_alumno != grado_asignatura:
                        print(f"El alumno no puede inscribirse en la asignatura {id_asignatura} porque no pertenece a su grado.")
                        continue
                    
                    sql_insert = "INSERT INTO alumno_asignatura(id_alumno, id_asignatura) VALUES (%s, %s)"
                    valores = (id_alumno, id_asignatura)
                    self.cursor.execute(sql_insert, valores)
                self.conn.commit()
                print(f"Las asignaturas del alumno {id_alumno} han sido actualizadas correctamente.")
            except Exception as err:
                print(f"Error al actualizar las asignaturas del alumno: {err}")

class Maestro(Usuario):
    def __init__(self, usuario, contrasenna):
        super().__init__(usuario, contrasenna)
        self.id_maestro= None
    def iniciarSesion(self):
        if super().iniciarSesion():
            self.obtenerRol()
            if self.rol=='maestro':
                self.id_maestro=self.obtenerIdM()
                if self.id_maestro:
                    return True
                else: return False
    def verificarAl(self, id_alumno, materia):
        if self.id_maestro:
            if self.cursor:
                sql_check_inscripcion = """
                    SELECT COUNT(*) FROM alumno_asignatura 
                    WHERE id_alumno = %s AND id_asignatura = %s
                        """
                self.cursor.execute(sql_check_inscripcion, (id_alumno, materia))
                resultado_inscripcion = self.cursor.fetchone()

                if not resultado_inscripcion or resultado_inscripcion[0] == 0:
                    print("Error: El alumno no está inscrito en esta materia.")
                    return "El alumno no está inscrito en esta materia."
    def verificarCalif(self, id_alumno, materia):
        if self.id_maestro and self.cursor:
            sql_check_calificacion = "SELECT valor, valor2, valor3 FROM calificacion WHERE id_alumno = %s AND  materia = %s "
            self.cursor.execute(sql_check_calificacion, (id_alumno, materia))
            resultado = self.cursor.fetchall()
            print(resultado)
            return resultado[0]

    def obtenerMaterias(self):
        if self.id_maestro:
            if self.cursor:
                sql="SELECT id_asignatura FROM maestro_asignatura WHERE id_maestro=%s"
                self.cursor.execute(sql, (self.id_maestro,))
                resultado =[fila[0] for fila in self.cursor.fetchall()]
                return resultado
    def verMaterias(self):
        if self.id_maestro and self.cursor:
            self.conn.commit()
            sql = """
                SELECT a.id_asignatura, a.nombre, a.grado
                FROM asignatura a
                JOIN maestro_asignatura ma ON a.id_asignatura = ma.id_asignatura
                WHERE ma.id_maestro = %s
            """
            self.cursor.execute(sql, (self.id_maestro,))
            materias = self.cursor.fetchall()
            return materias
    def registrarCalificacion(self, id_alumno, valor1, valor2, valor3, materia):
        if self.id_maestro:
            if self.cursor:
                sql= "INSERT INTO calificacion(id_alumno, id_maestro, valor, valor2, valor3, fecha,  materia) VALUES (%s, %s, %s, %s, %s, CURRENT_DATE, %s);"
                valores=(id_alumno, self.id_maestro, valor1, valor2, valor3, materia)
                self.cursor.execute(sql, valores)
                self.conn.commit()
                print("Calificación ingresada correctamente.")
                return True
    def editarCalificacion(self, id_alumno, valor1, valor2, valor3, materia):
        if self.id_maestro:
            if self.cursor:
                sql="UPDATE calificacion SET valor=%s, valor2=%s, valor3=%s, fecha=CURRENT_DATE WHERE id_alumno=%s AND materia=%s"
                self.cursor.execute(sql,(valor1, valor2, valor3, id_alumno, materia))
                self.conn.commit()
                print(f"Calificación actualizada para el alumno {id_alumno} en la materia {materia}.")
            else:
                print(f"Error: La calificación para el alumno {id_alumno} en la materia {materia} no existe.")

    def generarDoc(self, grado, grupo, id_asignatura):
        if self.cursor:
            self.conn.commit()
            self.cursor.callproc('GenerarDoc_Calificaciones', [grado, grupo, id_asignatura])
            self.conn.commit()
            self.cursor.execute("SELECT * FROM doc_calificaciones")
            resultado=self.cursor.fetchall()
            return resultado
        else: print("No se pudo crear el documento.")

#Por alguna razon deja de ejecutar bien si se importa desde otro script idk
if __name__ == "__main__":
    app = QApplication([])
    login_window = LoginC()
    login_window.show()
    app.exec_()