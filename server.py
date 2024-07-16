import random
import socket
import threading
import time
import os
from database import MySQLDatabase  #Importa el manager de la db

clients = []    #Almacena los datos de los usuarios actualmente conectados y logueados

class Server:
    def __init__(self): #Inicia parámetros básicos para conexión via sockets
        self.host = "127.0.0.1"
        self.port = 23162
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5) #Establece cola de clientes
        

    def dbConnection(self): #Inicia conexión con base de datos
        self.db = MySQLDatabase("localhost", "chat_socket", "root", "")
        return self.db.connect()
    
    def HandleUsers(self, client): #Maneja el thread de un usuario
        client.sendall(b"--Servidor: Bienvenido al CHAT. Escribe '/help' para ver la lista de comandos disponibles")


        #if not self.Auth(client): #En caso de error al tratar de logearse, cierra la conexión con el cliente y termina el thread
        #    print("Closing connection with unlogged client {}".format(client))
        #    client.close()
        #    return

        self.user = "Guest{}".format(random.randrange(0, 9999))
        self.password = ''
       
        clientData = {'conn': client, 'name': self.user, 'pass': self.password}

        

        clients.append(clientData)

        #client.sendall(b"--Server: ")
        self.recieve(clientData)

    def login(self, client): #Inicia sesion
        try:
            dbRes = self.db.returnQry('SELECT * FROM users WHERE users.name = %s AND users.password = %s', (self.user, self.password))

            if not dbRes: #Verifica si el usuario ingresado existe en la db
                client.sendall(b'Usuario no encontrado. Intentalo de nuevo')
                self.user = "Guest{}".format(random.randrange(0, 9999))
                self.password = ''
                return

            if not self.isLogged(): #Verifica si el usuario ingresado ya está logeado
                client.sendall(b'Este usuario ya inicio sesion')
                self.user = "Guest{}".format(random.randrange(0, 9999))
                self.password = ''
                return

            client.sendall(b'Inicio Sesion exitosamente')
        except:
            print(f"Hubo un error y no se pudo iniciar sesion. Cliente: {client}")
            return
            
    def isLogged(self): #Verifica si el usuario ingresado se encuentra logeado (el nombre es único)
        for cli in clients:
            if cli['name'] == self.user:
                return False
        return True
                       
    def register(self, client): #Crea un nuevo usuario
        try:
            res = self.db.returnQry('SELECT * FROM users WHERE users.name = %s', (self.user,))

            if len(res) > 0: #Verifica si el nombre de usuario ya existe
                client.sendall(b'Ese nombre de usuario ya esta en uso, elige otro.')
                self.user = "Guest{}".format(random.randrange(0, 9999))
                self.password = ''
                return

            if not self.db.alterQry('INSERT INTO users (name, password) VALUES(%s, %s)', (self.user, self.password)): #En caso de fallo en la conexión con la db, comunica al cliente
                client.sendall(b'No se pudo registrar el usuario, intenta de nuevo mas tarde')
                self.user = "Guest{}".format(random.randrange(0, 9999))
                self.password = ''
                return
           
            client.sendall(b'Usuario registrado exitosamente.')

            self.login(client)

        except:
            return
        
    def recieve(self, client): #Recibe mensajes de usuarios ya logeados
        while True:
            try:
                msg = client['conn'].recv(1024).decode()
                print("{}: {}".format(client['name'], msg))

                if msg.startswith('/'):
                    Smsg = msg.split(" ")

                    if Smsg[0] == "/register":
                        self.user = Smsg[1]
                        self.password = Smsg[2]
                        self.register(client)
                        continue

                    elif Smsg[0] == "/login":
                        self.user = Smsg[1]
                        self.password = Smsg[2]
                        self.login(client)
                        continue

                    elif Smsg[0] == "/logout":
                        self.user = "Guest" # el random
                        self.password = ""
                        #self.register(client) cambiar la varible bandera de logged a no
                        continue

                    elif Smsg[0] == "/exit": #Cierra la sesión del usuario y cierra la conexión socket
                        print(f"Cliente {client['conn']} has left")
                        client['conn'].close()
                        clients.remove(client)
                        break

                    elif Smsg[0] == "/list": #Envía lista de usuarios registrados en la base de datos
                        users = self.db.returnQry("SELECT name FROM users", ())
                   
                        if not users:
                            client["conn"].sendall(b" Could not get client list, try later.")
                            continue
                    
                        bLine = str(os.linesep)

                        strMsg = bLine.join(i['name'] for i in users)
                        client["conn"].sendall(strMsg.encode())
                        continue

                elif msg.startswith("@"): #Manda un mensaje privado a un cliente en concreto, de no existir
                    if not self.send_private_message(msg, client):
                        continue
               
                self.broadcast(msg, client)

            except: #Hubo un error, cierra la conexión y la sesión del cliente
                print(f"There was an error with logged client {client['conn']}, closing connection")
                client["conn"].close()
                clients.remove(client)
                break
    
    def send_private_message(self, msg, client): #Se encarga de enviar mensajes privados
        try:
            target_user, message = msg[1:].split(" ", 1)
            target_client = ""
           
            for cli in clients:          
                if cli['name'] == target_user: #Envía mensaje privado de encontrar al cliente
                   
                    target_client = cli['conn']
                    target_client.sendall(f"Susurro de {client['name']}: {message}".encode())
                   
                    if not self.saveMessage(client['name'], message, ): #Almacena el mensaje privado en la base de datos
                        return False
                   
                    return True
           
            client['conn'].sendall(b"No se pudo mandar el mensaje. Usuario no encontrado.")
            return False #No se encontró el cliente
       
        except Exception as e:  #Hubo un error durante la comunicación
            print(f"Error: {e}")
            return False
        
    def broadcast(self, msg, cli): #Envía mensaje a todos los clientes
        for client in clients:
            if client['conn'] != cli['conn']:
                try:
                    client['conn'].sendall(f"{self.user}: {msg}".encode())
                except:
                    print(f"Error broadcasting client {cli} message")
                    return
                
    def saveMessage(self, org, msg, dest):  #Guarda los mensajes de usuarios logeados en la base de datos
        sql = "INSERT INTO messages (origin_id, message, destination_id) SELECT (SELECT id FROM usuarios WHERE name = %s), %s, (SELECT id FROM usuarios WHERE name = %s)"
       
        if not self.db.alterQry(sql, (org, msg, dest)):
            return False
       
        print(f"Message from {org}")
        return True
    
def startServer(): #Inicia el servidor
    server = Server()

    dbTry = 0
    while True: # Intenta conectar con la DB hasta 5 veces, de no lograrlo cierra el socket
        dbConnected = server.dbConnection()

        dbTry = dbTry + 1
        print("Intento {} de conexion con la DB".format(dbTry))

        if dbConnected:
            break

        if not dbConnected and dbTry > 4: 
            print("No se pudo conectar a la Base de Datos luego de varios intentos, apagando servidor...")
            server.sock.close()
            return
        
        time.sleep(1.5)
   
    print("Servidor escuchando en {}:{}".format(server.host, server.port))

    while True: #Acepta nuevas conexiones (clientes)
        client, address = server.sock.accept()
        print("Nueva conexion de: {}".format(address))
        client_thread = threading.Thread(target=server.HandleUsers, args=(client,))
        client_thread.start()

if __name__ == "__main__":
    startServer()