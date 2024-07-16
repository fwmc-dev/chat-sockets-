import socket
import threading

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.c2s = False   #Para verificar si el cliente ya se encuentra conectado al servidor

    def receive_messages(self): #Recibe los mensajes del servidor, en caso de error se termina el loop y el thread.
        while True:
            try:
                msg = self.sock.recv(1024).decode()
                print(msg)
            except:
                #print("Connection closed by the server.")
                self.c2s = False
                break

    def connectSelf(self):  #Establece socket de comunicación con el servidor
        if self.c2s:
            print("Ya te encuentras conectado al servidor")
            return
       
        try:
           self.sock.connect((self.host, self.port))
           self.c2s = True
           
           recv_thread = threading.Thread(target=self.receive_messages)    
           recv_thread.start() #Inicia thread para recibir mensajes del servidor

           print("Conectado al servidor.")
           print("Escribe /help para más información")

           return True
        except:
           print("No se pudo conectar al servidor, intenta de nuevo más tarde.")
           self.c2s = False
           return False
        
    def send_message(self, message): #Envía el mensaje al servidor, en caso de error el programa sigue.
        try:
            self.sock.sendall(message.encode())
        except:
            print("No se pudo mandar el mensaje al servidor")

    # Esto lo voy a hacer del lado del servidor
    def run(self):
        while True: #Captura inputs del usuario
            message = input("Yo: ")  
           
            if message.lower() == "cerrar":     #Cierra la conexión con el servidor
                self.send_message("CERRAR")
                self.sock.close()
                break
            elif message.lower() == "/help":    #Muestra lista de comandos
                self.help()
                continue
            elif message.lower() == "conn":     #Inicia nuevamente conexión con el servidor
                self.connectSelf()
                continue

            self.send_message(message)

    def help(self): #Lista los comandos disponibles
        print("Enter your credentials like: USER/PASSWORD")    #Formato del mensaje de inicio de sesión
        print("To register a new user, use: REGIS:USER/PASSWORD")   #Formato del mensaje para registrarse
        print("To send a private message, type: @USERNAME MESSAGE") #Formato del mensaje para enviar susurro a un usuario en concreto
        print("To close your current session, type: CERRAR")    #Cerrar sesión actual
        print("To reconnect to server, try with: CONN") #Volver a establecer conexión con el servidor

def startClient():  #Inicia el programa
    client = Client("127.0.0.1", 23162)
   
    client.connectSelf()
    client.run()

if __name__ == "__main__": #No inicia en caso de ser importado
    startClient()