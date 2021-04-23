import threading
import sys
import socket
import pickle
import platform
import os


class Message():
    def __init__(self, username, msg):
        self.username = '<' + str(username) + '>'
        self.msg = msg

class Cliente():

    # def __init__(self, host = '10.34.84.147', port=61000):
    def __init__(self, host=input("Escriba la IP: "), port=input("Escriba el puerto: ")):
        self.sock = socket.socket()
        self.username = input('Username: ')
        self.sock.connect((str(host), int(port)))
        hilo_recv_mensaje = threading.Thread(target=self.recibir)
        hilo_recv_mensaje.daemon = True
        hilo_recv_mensaje.start()

        # for thread in threading.enumerate():
        # 	print("Hilo: " + thread.name + "\n" + "Proceso PID: "+ str(os.getpid()) + "\n" + "Daemon: " + str(thread.daemon) +  "\n")
        # print("Hilos totales: " + str(threading.activeCount()-1))
        message = Message(self.username, "se ha conectado")
        self.enviar(message)  # "<" + self.username + "> se ha conectado"
        print('\n !sendconfig == enviar información del PC ** !url30 (la_url)/ !url300 (la_url)/ !url3000 (la_url)/ !url30000 (la_url) == para ataques \n')
        while True:
            msg = input("\n>>\n")
            if msg != 'Q':
                self.enviar(Message(self.username, msg))
            else:
                print(" ****LOGOUT****")
                self.sock.close()
                sys.exit()

    def recibir(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if data:
                    print((pickle.loads(data)).username, (pickle.loads(data)).msg)
            except:
                pass

    def enviar(self, msg):
        if msg.msg == '!sendconfig':
            data = pickle.dumps(Message(self.username, str(platform.uname())))
    
        else:
            data = pickle.dumps(msg)
        self.sock.send(data)


        # if data:
        # 	print(pickle.loads(data))
c = Cliente()

