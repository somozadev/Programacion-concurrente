import threading
import sys
import socket
import requests
import pickle
import os
import platform
import prettytable as pt

class Cliente():

    def __init__(self, host=input("Intoduzca la IP del servidor ?  "), port=int(input("Intoduzca el PUERTO del servidor ?  "))):
        self.s = socket.socket()
        self.buffer = 1024
        self.s.connect((host, int(port)))
        print('\n\tProceso con PID = ',os.getpid(), '\n\tHilo PRINCIPAL con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tTotal Hilos activos en este punto del programa =', threading.active_count())
        threading.Thread(target=self.recibir, daemon=True).start()


        while True:
            msg = input('\nEscriba texto ?   ** Enviar = ENTER   ** Salir Chat = 1  ** Enviar configuracoión  = !sendconfig \n')
            
            if msg=='1':
                print(" **** Me piro vampiro; cierro socket y mato al CLIENTE con PID = ", os.getpid())
                self.s.close()
                sys.exit()
            
            elif msg=='!sendconfig':
                # print("ENTRO")

                # print(self.sysData())                
                self.enviar(self.sysData())
            elif msg =="!buffer":
                if self.buffer == 1024:
                    self.buffer = 2048
                elif self.buffer == 2048:
                    self.buffer = 1024
                print("new buffer size : " , self.buffer)
            
            else:
                self.enviar(msg)


    def recibir(self):
        print('\nHilo RECIBIR con ID =',threading.currentThread().getName(), '\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
        while True:
            try:
                data = self.s.recv(self.buffer)
                if data: print(pickle.loads(data))
            except: pass

    def enviar(self, msg):
        # print("prePick:",msg)
        # print("postPick:",pickle.dumps(msg))
        self.s.send(pickle.dumps(msg))



    def sysData(self):
        if self.buffer >= 2048: 
            return self.sysInfo()
        else:
            return str(platform.uname())
            
    def sysInfo(self):
        table = pt.PrettyTable()
        table.field_names = ["Question", "Result Type", "Method", "Result"]
        table.add_rows([
            ["A", "Procesador", "platform.processor()", platform.processor()],
            ["B", "Machine", "platform.machine()", platform.machine()],
            ["C", "Release", "platform.release()", platform.release()],
            ["D", "Version", "platform.version()", platform.version()],
            ["E", "Node", "platform.node()", platform.node()],
            ["F", "System", "platform.system()", platform.system()],
            ["G", "Cores físicos", "os.cpu_count()/2", os.cpu_count()/2],
            ["H", "Ipv4", "socket.gethostbyname(socket.gethostname())", socket.gethostbyname(
                socket.gethostname())],
        ])
        return table.get_string()




arrancar = Cliente()

        