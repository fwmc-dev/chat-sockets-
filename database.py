import mysql.connector as mysql
#import traceback

class MySQLDatabase():
    def __init__(self, sv, db, us, pw): #Establece campos básicos para la conexion
        self.server = sv
        self.database = db
        self.username = us
        self.password = pw
        if self.password is None:
            self.password = ""

    def connect(self):  #Inicia la conexión, en caso de error devuelve falso
        try:
            self.conn = mysql.connect(user=self.username, password=self.password, host=self.server, database=self.database)
            self.cursor = self.conn.cursor(dictionary=True)
            return True
        except:
            #print("Hubo un error en la conección con la base de datos:\n" + traceback.format_exc())
            return False

    def returnQry(self, qry, params):   #Para consultas que devuelvan un valor, como SELECT. En caso de error devuelve falso
        try:
            self.cursor.execute(qry, params)
            res = self.cursor.fetchall()
            return res
        except:
            #print("Hubo un error al ejecutar consulta\n" + traceback.format_exc())
            return False
        

    def alterQry(self, qry, params):    #Para consultas que no devuelvan un valor, como INSERT. En caso de error devuelve falso
        try:
            self.cursor.execute(qry, params)
            self.conn.commit()  #Asegura cambios en el servidor
            return True
        except:
            #print("Hubo un error al ejecutar consulta\n" + traceback.format_exc())
            return False
        
    def closeConn(self):    #Cierra la conexión y libera recursos del cursor
        self.cursor.close()
        self.conn.close()